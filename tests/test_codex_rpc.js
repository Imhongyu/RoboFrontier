const test=require('node:test'),assert=require('node:assert/strict');
const {capacityFailure}=require('../scripts/codex_rpc');
const {PolicyHost,robotTool}=require('../scripts/codex_policy_host');
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
for(const duringObservation of [false,true])test('a stopped host cannot start a paid turn'+(duringObservation?' after observation':''),async()=>{
  let calls=0;
  const host={stopped:!duringObservation,launch:{model:'local-test',effort:'medium'},observe:async()=>{
    host.stopped=true;return {thread:{status:{type:'idle'}}};
  },rpc:{call:async()=>{calls++;return {turn:{id:'unexpected'}};}},turns:new Map()};
  await assert.rejects(PolicyHost.prototype.send.call(host,'thread','wake'),/stopped/);
  assert.equal(calls,0);
});
