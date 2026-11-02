const test=require('node:test'),assert=require('node:assert/strict');
const {CodexRpc,STARTUP_ACK_MS,capacityFailure,requireNoMcpServers}=require('../scripts/codex_rpc');
const {PolicyHost,robotTool}=require('../scripts/codex_policy_host');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
test('native subscription tool admission rejects inherited MCP before a model turn',async()=>{
  for(const config of [{mcp_servers:{personal:{command:'unused'}}},
                       {mcp_servers:{personal:{enabled:true}}}]) {
    const calls=[];
    await assert.rejects(requireNoMcpServers({call:async(method)=>{
      calls.push(method);return {config};}}),/MCP servers/);
    assert.deepEqual(calls,['config/read']);
  }
});
test('native subscription tool admission accepts empty or disabled MCP configuration',async()=>{
  for(const config of [{},{mcp_servers:{personal:{enabled:false}}}])
    await requireNoMcpServers({call:async()=>({config})});
  await assert.rejects(requireNoMcpServers({call:async()=>({})}),/could not be verified/);
});
test('capacity retry distinguishes quota/auth/permanent errors',()=>{
  for(const message of ['model_capacity_limit','429 Too Many Requests','server_overloaded'])assert.equal(capacityFailure({message}),true);
  for(const message of ['insufficient_quota 429','invalid_api_key','Bad Request 400'])assert.equal(capacityFailure({message}),false);
});
test('an active turn cannot be steered by the scheduler',async()=>{
  let called=false;
  await assert.rejects(PolicyHost.prototype.send.call({observe:async()=>({thread:{status:{type:'active'}}}),rpc:{call:()=>{called=true;}}},'t','wake'),/active/);
  assert.equal(called,false);
});
test('robot transport cannot select another role connection',()=>{
  assert.equal(robotTool.name,'robot');
  assert.equal(robotTool.inputSchema.properties.connection,undefined);
});
test('direct bootstrap names shared rules and does not promise all drop counters',()=>{
  const prompt=PolicyHost.prototype.bootstrap.call({run:'/tmp/test-run',wallLimit:300},'Controller');
  assert.match(prompt,/policy-rules\.md/);
  assert.match(prompt,/Supported process events follow their task-specific detection rules/);
  assert.match(prompt,/do not automatically veto completion/);
  assert.match(prompt,/without waiting for another START/);
});
test('frozen legacy roles retain the readiness barrier and read their work after wake',()=>{
  const prompt=PolicyHost.prototype.bootstrap.call({run:'/tmp/test-run',wallLimit:36000},'A','ready_barrier_v1');
  assert.match(prompt,/call robot ready/);
  assert.match(prompt,/call robot work/);
  assert.doesNotMatch(prompt,/The experiment has STARTED and the task clock is running/);
});
test('capacity recovery resumes a started task without a READY barrier',async()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'capacity-retry-'));
  try {
    const fakePython=path.join(dir,'python');
    fs.writeFileSync(fakePython,'#!/bin/sh\nprintf "false\\n"\n',{mode:0o755});
    const prompts=[];
    const host={stopped:false,began:Date.now(),run:dir,cwd:dir,python:fakePython,
      actors:new Map([['thread','Controller']]),failures:new Map([['thread:turn',Date.now()-11000]]),retries:new Set(),
      admin:async()=>({paused:false,lifecycle:'running'}),
      observe:async()=>({thread:{status:{type:'systemError'}},latestTurn:{id:'turn',status:'failed',error:{message:'429 Too Many Requests'}}}),
      send:async(id,prompt)=>prompts.push(prompt),event:()=>{}};
    await PolicyHost.prototype.retryCapacity.call(host);
    assert.equal(prompts.length,1);
    assert.match(prompts[0],/The experiment has started/);
    assert.match(prompts[0],/continue without waiting for another START/);
    assert.doesNotMatch(prompts[0],/legacy startup barrier has not opened/);
    await PolicyHost.prototype.retryCapacity.call(host);
    assert.equal(prompts.length,1);
  } finally {fs.rmSync(dir,{recursive:true,force:true});}
});
test('initialize waits for the startup acknowledgement limit unless told otherwise',async()=>{
  let waited;const fake={call:async(method,params,timeoutMs)=>{waited=timeoutMs;return {};},write(){}};
  await CodexRpc.prototype.initialize.call(fake);assert.equal(waited,STARTUP_ACK_MS);assert.equal(STARTUP_ACK_MS,180000);
  await CodexRpc.prototype.initialize.call(fake,5000);assert.equal(waited,5000);
});
