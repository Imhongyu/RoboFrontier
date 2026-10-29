const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {preflight}=require('../scripts/codex_preflight');
function fakeRpc({badParent=false,badChild=false,badImage=false,badData=false,noFork=false,skipToolImage=false,schemaOnlyData=false}={}) {
  return class {
    constructor(args,handlers){this.handlers=handlers;}
    async initialize(){}
    async close(){}
    async call(method,p={}) {
      if(method==='thread/start'){
        this.colorSchema=p.dynamicTools[0].inputSchema.properties.data?.properties?.colors;
        return {thread:{id:'parent'}};
      }
      if(noFork && ['thread/fork','thread/compact/start'].includes(method))throw new Error('Smoke must not fork/compact');
      if(method==='thread/fork')return {thread:{id:'child',forkedFromId:badParent?'other':'parent'}};
      if(method==='thread/compact/start') {
        this.handlers.onEvent({method:'thread/compacted',params:{threadId:'parent'}});return {};
      }
      if(method==='turn/start') {
        const child=p.threadId==='child';
        for(const [left,right] of child?[['blue','yellow']]:skipToolImage?[['red','blue']]:[['red','blue'],['blue','yellow']]) {
          await this.handlers.onRequest('item/tool/call',{tool:'protocol_check',threadId:p.threadId,
            arguments:JSON.stringify({left:badImage||child&&badChild?'green':left,right,
              data:badData?{}:{note:'protocol-check',colors:schemaOnlyData&&this.colorSchema?.type!=='object'?[left,right]:{left,right}}})});
        }
        this.handlers.onEvent({method:'turn/completed',params:{threadId:p.threadId,turn:{status:'completed'}}});
        return {};
      }
      return {};
    }
  };
}
async function run(opts,mode={}) {
  const folder=fs.mkdtempSync(path.join(os.tmpdir(),'rf-preflight-'));
  try {
    fs.writeFileSync(path.join(folder,'launch.json'),JSON.stringify({args:[],model:'sample',provider:'sample',effort:'high',context_window:272000,auto_compact_token_limit:245000}));
    fs.writeFileSync(path.join(folder,'colors-tool.png'),'synthetic image fixture');
    return await preflight(folder,fakeRpc(opts),mode);
  } finally {fs.rmSync(folder,{recursive:true,force:true});}
}
test('preflight verifies fork parent and inherited tool result',async()=>{
  const result=await run();assert.equal(result.passed,true);assert.equal(result.fork_history_and_tool,true);
  assert.equal(result.automatic_compaction_tested,false);assert.equal(result.context_stress_tested,false);
  assert.equal(result.tool_image_round_trip,true);
});
test('preflight fails closed on incorrect fork parent',async()=>{
  const result=await run({badParent:true});assert.equal(result.passed,false);assert.match(result.error,/parent mismatch/);
});
test('preflight fails closed when child cannot recover image colors',async()=>{
  const result=await run({badChild:true});assert.equal(result.passed,false);assert.match(result.error,/inherit/);
});
test('smoke checks vision and tools without compaction or fork qualification',async()=>{
  const result=await run({noFork:true},{smokeOnly:true});
  assert.equal(result.passed,true);assert.equal(result.smoke_only,true);
  assert.equal(result.fork_history_and_tool,undefined);
});
test('smoke rejects incorrect image interpretation',async()=>{
  const result=await run({badImage:true},{smokeOnly:true});assert.equal(result.passed,false);
});
test('preflight rejects a provider that returns colors but loses the robot payload',async()=>{
  const result=await run({badData:true},{smokeOnly:true});
  assert.equal(result.passed,false);
});
test('preflight rejects a provider that stops before reading the tool-returned image',async()=>{
  const result=await run({skipToolImage:true},{smokeOnly:true});
  assert.equal(result.passed,false);
});
test('preflight declares nested colors as an object so schema-driven callers can complete the probe',async()=>{
  const result=await run({schemaOnlyData:true});assert.equal(result.passed,true);
});
