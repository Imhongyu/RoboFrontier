// Explicitly invoked paid connectivity test, separate from scored robot trials.
const fs=require('node:fs'),path=require('node:path');
const {CodexRpc}=require('./codex_rpc');
const {robotTool}=require('./codex_policy_host');
async function preflight(folder, Rpc=CodexRpc, {smokeOnly=false}={}) {
  const launch=JSON.parse(fs.readFileSync(path.join(folder,'launch.json')));
  const waits=new Map();
  let resolveCompact;
  const compacted=new Promise(r=>resolveCompact=r);
  const tools=new Map(),checks=new Map(); let compact=false,id,childId;
  const serverLog=fs.openSync(path.join(folder,'server.log'),'a');
  const handlers={stderr:serverLog,
    onEvent:m=>{
      if(m.method==='turn/completed') waits.get(m.params.threadId)?.(m.params.turn);
      if(m.method==='thread/compacted' || m.method==='item/completed' && m.params?.item?.type==='contextCompaction') {compact=true;resolveCompact(true);}
      if(m.method==='error' && !m.params?.willRetry)resolveCompact(false);
    },onRequest:async(m,p)=>{
      if(m!=='item/tool/call' || p.tool!=='protocol_check')throw new Error('Unsupported preflight request');
      const a=typeof p.arguments==='string'?JSON.parse(p.arguments):p.arguments;
      const stage=checks.get(p.threadId)||0;
      const [left,right]=stage?['blue','yellow']:['red','blue'];
      const valid=a.left===left&&a.right===right&&a.data?.note==='protocol-check'
        &&a.data?.colors?.left===left&&a.data?.colors?.right===right;
      tools.set(p.threadId,valid&&stage>0);
      if(valid)checks.set(p.threadId,stage+1);
      if(valid&&stage===0)return {success:true,contentItems:[
        {type:'inputText',text:'Initial image check passed. Inspect the NEW tool-returned image and call protocol_check again with its left/right colors and the same nested data structure. Then reply VISION_TOOL_OK.'},
        {type:'inputImage',imageUrl:'data:image/png;base64,'+fs.readFileSync(path.join(folder,'colors-tool.png')).toString('base64')}]};
      return {success:valid,contentItems:[{type:'inputText',text:valid?'VISION_TOOL_OK':'Incorrect image colors or nested data'}]};
    }};
  const rpc=await (Rpc.create?Rpc.create(launch.args,handlers):new Rpc(launch.args,handlers));
  fs.closeSync(serverLog);
  let report={passed:false,model:launch.model,provider:launch.provider,effort:launch.effort,
    actual_provider_model_verified:false,context_window:launch.context_window,
    auto_compact_token_limit:launch.auto_compact_token_limit,context_stress_tested:false,
    automatic_compaction_tested:false,smoke_only:smokeOnly,
    scope:smokeOnly?'Small real API input-image and tool-output-image/function round trip; no robot trial or run qualification':
      'Small real API input-image/tool-output-image/function/manual-compaction/fork test; no robot trial'};
  const deadline=(promise,ms)=>new Promise((resolve,reject)=>{
    const t=setTimeout(()=>reject(new Error('Preflight deadline exceeded')),ms);
    promise.then(v=>{clearTimeout(t);resolve(v);},e=>{clearTimeout(t);reject(e);});
  });
  const nextTurn=thread=>new Promise(resolve=>waits.set(thread,resolve));
  try {
    await rpc.initialize();
    const a=await rpc.call('thread/start',{cwd:folder,model:launch.model,modelProvider:launch.provider,
      approvalPolicy:'never',sandbox:'read-only',dynamicTools:[{type:'function',name:'protocol_check',
        description:'Submit the two dominant image colors from left to right.',inputSchema:{type:'object',
        properties:{left:{type:'string'},right:{type:'string'},data:robotTool.inputSchema.properties.data},
        required:['left','right','data']}}]});id=a.thread.id;
    await rpc.call('thread/name/set',{threadId:id,name:'API preflight · '+launch.model});
    const finished=nextTurn(id);
    await rpc.call('turn/start',{threadId:id,model:launch.model,effort:launch.effort,input:[
      {type:'text',text:'Inspect the attached image. Call protocol_check with the dominant color in the left half and the right half, using lowercase English color names. Also include data with note "protocol-check" and colors containing the same left and right values, to check nested robot parameter transport. Then reply with the tool result. Do not use shell or other tools.'},
      {type:'localImage',path:path.join(folder,'colors.png')} ]});
    const turn=await deadline(finished,180000);
    if(turn.status!=='completed' || !tools.get(id))throw new Error('Parent image/tool turn failed: '+JSON.stringify(turn.error));
    if(smokeOnly) {
      report={...report,passed:true,vision_and_function:true,robot_payload:true,tool_image_round_trip:true,thread_id:id};
      return report;
    }
    await rpc.call('thread/compact/start',{threadId:id});
    if(!await deadline(compacted,180000))throw new Error('Compaction failed');
    const fork=await rpc.call('thread/fork',{threadId:id,cwd:folder,model:launch.model,
      modelProvider:launch.provider,excludeTurns:true,ephemeral:false});
    childId=fork.thread.id;
    checks.set(childId,1);
    if(fork.thread.forkedFromId!==id)throw new Error('Fork parent mismatch');
    const childFinished=nextTurn(childId);
    await rpc.call('turn/start',{threadId:childId,model:launch.model,effort:launch.effort,input:[
      {type:'text',text:'Using the image and tool result from our prior conversation, call protocol_check again with the same left and right colors and the same nested data payload. Do not use shell or other tools.'}]});
    const child=await deadline(childFinished,180000);
    if(child.status!=='completed' || !tools.get(childId))throw new Error('Fork did not inherit usable image history and tool');
    report={...report,passed:true,vision_and_function:true,robot_payload:true,tool_image_round_trip:true,compaction:compact,
      fork_parent_verified:true,fork_history_and_tool:true,thread_id:id,child_thread_id:childId};
  } catch(e) {report.error=e.message;}
  finally {
    for(const thread of [childId,id])if(thread)try{await rpc.call('thread/archive',{threadId:thread});}catch{}
    await rpc.close();
    fs.writeFileSync(path.join(folder,'report.json'),JSON.stringify(report,null,2)+'\n');
  }
  return report;
}
if(require.main===module)preflight(path.resolve(process.argv[2]),CodexRpc,{smokeOnly:process.argv.includes('--smoke-only')})
  .then(r=>{console.log(JSON.stringify(r));process.exitCode=r.passed?0:1;});
module.exports={preflight};
