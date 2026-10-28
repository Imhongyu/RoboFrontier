// OpenRouter providers differ in support for multimodal function results.
// Keep tool text as a string and deliver the unchanged media as user input.
const http=require('node:http');
const {Readable}=require('node:stream');

function normalizeRequest(body) {
  const normalized={...body};
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

async function createBridge(baseUrl) {
  const server=http.createServer(async(request,response)=>{
    const abort=new AbortController();
    response.on('close',()=>{if(!response.writableFinished)abort.abort();});
    try {
      const chunks=[];
      for await(const chunk of request) chunks.push(chunk);
      const body=normalizeRequest(JSON.parse(Buffer.concat(chunks).toString()));
      const upstream=await fetch(baseUrl.replace(/\/$/,'')+request.url,{
        method:'POST',headers:{'content-type':'application/json',
          authorization:request.headers.authorization},body:JSON.stringify(body),signal:abort.signal});
      const headers={'content-type':upstream.headers.get('content-type')||'application/json'};
      if(upstream.headers.has('retry-after'))headers['retry-after']=upstream.headers.get('retry-after');
      response.writeHead(upstream.status,headers);
      Readable.fromWeb(upstream.body).on('error',()=>response.destroy()).pipe(response);
    } catch(error) {
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
