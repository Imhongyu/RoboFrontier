// OpenRouter providers differ in support for multimodal function results.
// Keep tool text as a string and deliver the unchanged media as user input.
const http=require('node:http');
const fs=require('node:fs');
const {Readable,Transform}=require('node:stream');

function normalizeRequest(body,{maxOutputTokens}={}) {
  const normalized={...body};
  if(maxOutputTokens)normalized.max_output_tokens=Math.min(body.max_output_tokens??maxOutputTokens,maxOutputTokens);
  if(body.tools) normalized.tools=body.tools.filter(tool=>tool.type==='function');
  if(!Array.isArray(body.input)) return normalized;
  const input=[],media=[];
  const flush=()=>{
    for(const {callId,parts} of media) input.push({type:'message',role:'user',content:[
      {type:'input_text',text:'Media returned by tool call '+callId+':'},...parts]});
    media.length=0;
  };
  for(const item of body.input) {
    if(item.type!=='function_call_output') flush();
    if(item.type==='function_call_output' && Array.isArray(item.output)) {
      input.push({...item,output:item.output.filter(part=>part.type==='input_text').map(part=>part.text).join('\n')});
      const parts=item.output.filter(part=>part.type!=='input_text');
      if(parts.length) media.push({callId:item.call_id,parts});
    } else input.push(item);
  }
  flush();
  normalized.input=input;
  return normalized;
}

async function createBridge(baseUrl,{maxOutputTokens,auditPath,holdPath,stopPath}={}) {
  let sequence=0;
  const audit=record=>{if(auditPath)fs.appendFileSync(auditPath,JSON.stringify({at:Date.now()/1000,...record})+'\n');};
  const server=http.createServer(async(request,response)=>{
    const abort=new AbortController();
    const requestNumber=++sequence,started=Date.now();
    response.on('close',()=>{if(!response.writableFinished)abort.abort();});
    try {
      const chunks=[];
      for await(const chunk of request) chunks.push(chunk);
      const body=normalizeRequest(JSON.parse(Buffer.concat(chunks).toString()),{maxOutputTokens});
      while(holdPath && fs.existsSync(holdPath)) {
        if(abort.signal.aborted || stopPath && fs.existsSync(stopPath))throw new Error('Request cancelled during spend guard hold');
        await new Promise(resolve=>setTimeout(resolve,100));
      }
      if(stopPath && fs.existsSync(stopPath))throw new Error('Run stopped before request');
      audit({event:'request',request_number:requestNumber,model:body.model,
        reasoning_effort:body.reasoning?.effort,max_output_tokens:body.max_output_tokens});
      const upstream=await fetch(baseUrl.replace(/\/$/,'')+request.url,{
        method:'POST',headers:{'content-type':'application/json',
          authorization:request.headers.authorization},body:JSON.stringify(body),signal:abort.signal});
      const headers={'content-type':upstream.headers.get('content-type')||'application/json'};
      if(upstream.headers.has('retry-after'))headers['retry-after']=upstream.headers.get('retry-after');
      response.writeHead(upstream.status,headers);
      const source=Readable.fromWeb(upstream.body);
      source.on('error',()=>response.destroy());
      if(!auditPath){source.pipe(response);return;}
      let pending='',terminal=false;
      const decoder=new TextDecoder();
      // Inspect terminal metadata only; forward original bytes without buffering the response.
      const inspector=new Transform({transform(chunk,encoding,done){
        pending+=decoder.decode(chunk,{stream:true});
        let newline;
        while((newline=pending.indexOf('\n'))>=0){
          const line=pending.slice(0,newline).trim();pending=pending.slice(newline+1);
          if(!line.startsWith('data:'))continue;
          let event;try{event=JSON.parse(line.slice(5));}catch{continue;}
          if(!['response.completed','response.incomplete','response.failed'].includes(event.type))continue;
          const r=event.response||{},u=r.usage||{};terminal=true;
          audit({event:'response',request_number:requestNumber,http_status:upstream.status,
            duration_ms:Date.now()-started,response_id:r.id,model:r.model,provider:r.provider,
            status:r.status,reason:r.incomplete_details?.reason,error_code:r.error?.code,
            input_tokens:u.input_tokens,cached_input_tokens:u.input_tokens_details?.cached_tokens,
            output_tokens:u.output_tokens,reasoning_tokens:u.output_tokens_details?.reasoning_tokens});
        }
        done(null,chunk);
      }});
      response.on('close',()=>{if(!terminal)audit({event:'response',request_number:requestNumber,
        http_status:upstream.status,duration_ms:Date.now()-started,status:upstream.ok?'stream_closed':'http_error'});});
      source.pipe(inspector).pipe(response);
    } catch(error) {
      audit({event:'transport_error',request_number:requestNumber,duration_ms:Date.now()-started,error_type:error.name});
      if(!response.headersSent) {
        response.writeHead(502,{'content-type':'application/json'});
        response.end(JSON.stringify({error:{message:'OpenRouter transport: '+error.message}}));
      } else response.destroy();
    }
  });
  await new Promise((resolve,reject)=>{
    server.once('error',reject);server.listen(0,'127.0.0.1',resolve);
  });
  return {url:'http://127.0.0.1:'+server.address().port,
    close:()=>new Promise(resolve=>{server.close(resolve);server.closeAllConnections();})};
}

module.exports={normalizeRequest,createBridge};
