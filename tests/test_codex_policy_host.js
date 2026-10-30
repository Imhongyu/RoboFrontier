const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const {capacityFailure} = require('../scripts/codex_rpc');

function fixture(t, onDispatch, {unsettled=false,nativeCompaction=false,compactionSignal='thread/compacted',readStatuses=[]}={}) {
  const run = fs.mkdtempSync(path.join(os.tmpdir(), 'robofrontier-host-'));
  t.after(() => fs.rmSync(run, {recursive:true, force:true}));
  for (const directory of ['private/inputs', 'private/outputs', 'private/state/connections', 'public/inputs'])
    fs.mkdirSync(path.join(run, directory), {recursive:true});
  const write = (name, value) => fs.writeFileSync(path.join(run, name), JSON.stringify(value));
  write('private/inputs/codex.json', {args:[], model:'test-model', provider:'test-provider', effort:'max'});
  write('private/inputs/manifest.json', {model_requested:'test-model', effort_requested:'max'});
  write('private/inputs/task.json', {run_protocol:{total_wall_limit_s:86400}});
  write('private/inputs/harness.json', {startup_protocol:'direct_controller_v2'});
  write('private/state/connections/Meta.json', {url:'http://local-test-only'});
  write('public/inputs/roles.json', {roles:{Meta:{kind:'manager'}, worker:{kind:'robot'}}});
  const calls = [], administration = [], physicalCalls = [];
  let handlers, closed = false;
  const native={status:'idle',latestTurn:null},timers=[];
  t.after(()=>timers.forEach(clearTimeout));
  const rpc = {
    initialize:async () => {},
    close:async () => {closed = true;},
    call:async (method, params) => {
      calls.push({method, params});
      if (method === 'thread/start') return {thread:{id:'policy-thread'}};
      if (method === 'thread/read') return {thread:{id:'policy-thread', status:{type:readStatuses.shift()||native.status}}};
      if (method === 'thread/turns/list') return {data:native.latestTurn?[native.latestTurn]:[]};
      if (method === 'turn/start') return {turn:{id:'initial-turn', status:'inProgress'}};
      if (method === 'thread/compact/start') {
        if(nativeCompaction) {
          native.status='active';
          native.latestTurn={id:'compaction-turn',status:'inProgress'};
        }
        handlers.onEvent({method:compactionSignal,params:{threadId:params.threadId,
          ...(compactionSignal==='item/completed'?{item:{type:'contextCompaction'}}:{})}});
        if(nativeCompaction) timers.push(setTimeout(()=>{
          native.status='idle';
          native.latestTurn={id:'compaction-turn',status:'completed'};
          handlers.onEvent({method:'turn/completed',params:{threadId:params.threadId,turn:native.latestTurn}});
        },30));
      }
      return {};
    },
  };
  const childProcess = {
    execFile:(command, args, options, callback) => {
      if (args.includes('robofrontier.runtime_cli')) administration.push(args[args.indexOf('--run-dir') + 2]);
      if (args.includes('robofrontier.pipeline_client')) physicalCalls.push(args[args.indexOf('--call-id') + 2]);
      callback(null, args.includes('request-start') ? '{"started":true}' : args.includes('-c') ? JSON.stringify(unsettled) : '{}', '');
    },
    exec:() => {throw new Error('Unexpected shell command in fixture');},
    spawn:() => ({exitCode:null, on:() => {}}),
  };
  const module = {exports:{}};
  const dependencies = {
    'node:child_process':childProcess,
    'node:util':{promisify:fn=>(...args)=>new Promise((resolve,reject)=>
      fn(...args,(error,stdout,stderr)=>error?reject(error):resolve({stdout,stderr})))},
    './codex_rpc':{capacityFailure, CodexRpc:{create:async (args, options) => {handlers = options; return rpc;}}},
    './meta_dispatcher':{runMetaDispatcher:async options => onDispatch(options, emit)},
  };
  const source = fs.readFileSync(path.join(__dirname, '../scripts/codex_policy_host.js'), 'utf8');
  vm.runInNewContext(source, {
    require:name => dependencies[name] || require(name), module,
    console, process, Buffer, setTimeout, clearTimeout,setInterval,clearInterval,
  }, {filename:'codex_policy_host.js'});
  const host = new module.exports.PolicyHost(run, run, 'fake-python');
  function emit(error, id='failed-turn') {
    if(nativeCompaction)native.latestTurn={id,status:'failed',error};
    handlers.onEvent({method:'turn/completed', params:{threadId:'policy-thread',
      turn:{id, status:'failed', error}}});
  }
  return {host, run, calls, administration, physicalCalls, emit, closed:() => closed};
}

for (const [name, error] of [
  ['max_output_tokens', {message:'The max_output_tokens value exceeds the provider maximum',
    code:'max_output_tokens', rawResponse:'SENSITIVE_RESPONSE_NOT_FOR_SUMMARY', request:{prompt:'SENSITIVE_PROMPT_NOT_FOR_SUMMARY'}}],
  ['permanent model error', {message:'Bad Request 400: unsupported tool format', code:'invalid_request_error'}],
]) {
  test(`${name} stops the host and seals without retrying the failed model turn`, async t => {
    let stoppedAtDispatch;
    const context = fixture(t, async (options, emit) => {
      emit(error);
      stoppedAtDispatch = options.stopRequested();
      return {status:'stopped'};
    });
    await context.host.runTask();
    assert.equal(stoppedAtDispatch, true, 'a permanent model failure must stop the dispatcher');
    assert.equal(context.host.stopped, true);
    const file = path.join(context.run, 'private/outputs/model-failure.json');
    assert.ok(fs.existsSync(file), 'a permanent model failure needs a persistent safe diagnostic');
    const summary = JSON.parse(fs.readFileSync(file, 'utf8'));
    assert.equal(summary.thread_id, 'policy-thread');
    assert.equal(summary.turn_id, 'failed-turn');
    assert.equal(summary.reason, name === 'max_output_tokens' ? 'output_limit' : 'model_error');
    assert.equal(summary.error.message, name === 'max_output_tokens' ?
      'Model response reached max_output_tokens' : 'Model turn failed');
    assert.ok(!JSON.stringify(summary).includes('SENSITIVE_RESPONSE_NOT_FOR_SUMMARY'));
    assert.ok(!JSON.stringify(summary).includes('SENSITIVE_PROMPT_NOT_FOR_SUMMARY'));
    assert.deepEqual(context.administration, ['request-start','seal']);
    assert.equal(context.closed(), true);
    assert.equal(context.calls.filter(call => call.method === 'turn/start').length, 1,
      'only the initial turn may start; permanent failures must not trigger a retry');
    assert.deepEqual(context.physicalCalls, ['bind'], 'sealing must not replay any physical actions');
  });
}

test('capacity failures keep the existing wait classification without immediately stopping', async t => {
  for (const message of ['429 Too Many Requests', 'server_overloaded','stream disconnected: error sending request']) {
    const context = fixture(t, async () => {});
    await context.host.startServer();
    context.emit({message});
    assert.equal(context.host.stopped, false);
    assert.ok(context.host.failures.has('policy-thread:failed-turn'));
    const events = fs.readFileSync(path.join(context.run, 'private/outputs/codex-host.jsonl'), 'utf8')
      .trim().split('\n').map(line => JSON.parse(line));
    assert.ok(events.some(event => event.event === (message.startsWith('stream')?'transport_wait':'capacity_wait')));
    assert.equal(fs.existsSync(path.join(context.run, 'private/outputs/model-failure.json')), false);
    assert.equal(context.calls.filter(call => call.method === 'turn/start').length, 0);
    await context.host.rpc.close();
  }
});

test('temporary network failure continues the existing world without sealing it',async t=>{
  let context;
  context=fixture(t,async(options,emit)=>{
    emit({message:'stream disconnected: error sending request'});
    context.host.failures.set('policy-thread:failed-turn',Date.now()-11000);
    await context.host.retryCapacity();
    assert.equal(options.stopRequested(),false);
    assert.equal(context.calls.filter(c=>c.method==='turn/start').length,2);
    assert.equal(context.administration.includes('seal'),false);
  });
  await context.host.runTask();
  assert.deepEqual(context.physicalCalls,['bind']);
});

test('continue-until-terminal profile does not terminate at the old output retry count',async t=>{
  let context;
  context=fixture(t,async(options,emit)=>{
    for(let n=0;n<3;n++){
      emit({message:'Response incomplete: max_output_tokens'},'limited-'+n);
      context.host.failures.set('policy-thread:limited-'+n,Date.now()-11000);
      assert.equal(options.stopRequested(),false);
      await context.host.retryCapacity();
    }
    assert.equal(context.calls.filter(c=>c.method==='turn/start').length,4);
    assert.equal(context.administration.includes('seal'),false);
  });
  context.host.launch.profile={recover_output_limits:true};
  await context.host.runTask();
  assert.deepEqual(context.physicalCalls,['bind']);
});

test('configured output recovery compacts and continues the same world twice, then seals', async t => {
  let context;
  context = fixture(t, async (options, emit) => {
    for(let attempt=1;attempt<=2;attempt++) {
      emit({message:'Response incomplete: max_output_tokens'},'limited-'+attempt);
      assert.equal(options.stopRequested(),false);
      context.host.failures.set('policy-thread:limited-'+attempt,Date.now()-11000);
      await context.host.retryCapacity();
      await context.host.retryCapacity();
      assert.equal(context.calls.filter(c=>c.method==='thread/compact/start').length,attempt);
      assert.equal(context.calls.filter(c=>c.method==='turn/start').length,attempt+1);
      assert.equal(context.closed(),false);
      assert.equal(context.administration.includes('seal'),false);
    }
    emit({message:'Response incomplete: max_output_tokens'},'limited-3');
    assert.equal(options.stopRequested(),true);
  });
  context.host.launch.profile={output_limit_retries:2};
  await context.host.runTask();
  assert.deepEqual(context.physicalCalls,['bind']);
  assert.deepEqual(context.administration,['request-start','snapshot','snapshot','snapshot','snapshot','seal']);
  assert.equal(context.calls.filter(c=>c.method==='thread/start').length,1);
});

test('output recovery does not start another turn while a physical result is unresolved', async t => {
  let context;
  context=fixture(t,async(options,emit)=>{
    emit({message:'Response incomplete: max_output_tokens'});
    context.host.failures.set('policy-thread:failed-turn',Date.now()-11000);
    await context.host.retryCapacity();
    assert.equal(options.stopRequested(),false);
    assert.equal(context.calls.filter(c=>c.method==='thread/compact/start').length,0);
    assert.equal(context.calls.filter(c=>c.method==='turn/start').length,1);
  },{unsettled:true});
  context.host.launch.profile={output_limit_retries:2};
  await context.host.runTask();
  assert.deepEqual(context.physicalCalls,['bind']);
});

for(const signal of ['thread/compacted','item/completed']) {
  test(`output recovery survives ${signal} arriving before the native session becomes idle`,async t=>{
    let context;
    context=fixture(t,async(options,emit)=>{
      emit({message:'Response incomplete: max_output_tokens'});
      context.host.failures.set('policy-thread:failed-turn',Date.now()-11000);
      // The dispatcher catches a busy-read error and polls again, as in the real host.
      await context.host.retryCapacity().catch(()=>{});
      await new Promise(resolve=>setTimeout(resolve,40));
      await context.host.retryCapacity().catch(()=>{});
      await context.host.retryCapacity().catch(()=>{});
      const compacted=await context.host.observe('policy-thread');
      assert.equal(compacted.thread.status.type,'idle');
      assert.equal(context.calls.filter(call=>call.method==='turn/start').length,2,
        'completion of the compaction turn must not lose the pending continuation');
      assert.equal(context.calls.filter(call=>call.method==='thread/compact/start').length,1);
      assert.ok(context.calls.filter(call=>call.method==='turn/start').every(call=>call.params.threadId==='policy-thread'));
      assert.equal(options.stopRequested(),false);
      assert.equal(context.closed(),false);
      assert.equal(context.administration.includes('seal'),false);
      assert.deepEqual(context.physicalCalls,['bind']);
    },{nativeCompaction:true,compactionSignal:signal});
    context.host.launch.profile={recover_output_limits:true};
    await context.host.runTask();
  });
}

test('a busy pre-send read leaves recovery eligible for a later idle poll',async t=>{
  let context;
  const readStatuses=[];
  context=fixture(t,async(options,emit)=>{
    emit({message:'stream disconnected: error sending request'});
    context.host.failures.set('policy-thread:failed-turn',Date.now()-11000);
    readStatuses.push('idle','active');
    await context.host.retryCapacity().catch(()=>{});
    await context.host.retryCapacity().catch(()=>{});
    await context.host.retryCapacity().catch(()=>{});
    assert.equal(context.calls.filter(call=>call.method==='turn/start').length,2,
      'a rejected busy-state check must not consume the only continuation attempt');
    assert.equal(options.stopRequested(),false);
    assert.equal(context.administration.includes('seal'),false);
    assert.deepEqual(context.physicalCalls,['bind']);
  },{readStatuses});
  await context.host.runTask();
});

test('an unknown continuation acknowledgement is recorded and never sent again',async t=>{
  let context;
  context=fixture(t,async(options,emit)=>{
    emit({message:'stream disconnected: error sending request'});
    context.host.failures.set('policy-thread:failed-turn',Date.now()-11000);
    const call=context.host.rpc.call;
    context.host.rpc.call=async(method,params)=>{
      const result=await call(method,params);
      if(method==='turn/start')throw new Error('Connection lost before acknowledgement');
      return result;
    };
    await assert.rejects(context.host.retryCapacity(),/acknowledgement/);
    await context.host.retryCapacity();
    assert.equal(context.calls.filter(call=>call.method==='turn/start').length,2);
    assert.equal(context.host.pendingRecoveries.size,0);
    const events=fs.readFileSync(path.join(context.run,'private/outputs/codex-host.jsonl'),'utf8')
      .trim().split('\n').map(line=>JSON.parse(line));
    assert.equal(events.filter(event=>event.event==='recovery_start_unconfirmed').length,1);
    assert.equal(events.filter(event=>event.event==='transport_retry').length,0);
    assert.equal(options.stopRequested(),false);
    assert.deepEqual(context.physicalCalls,['bind']);
  });
  await context.host.runTask();
});
