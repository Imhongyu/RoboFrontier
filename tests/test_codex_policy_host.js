const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const {capacityFailure} = require('../scripts/codex_rpc');

function fixture(t, onDispatch) {
  const run = fs.mkdtempSync(path.join(os.tmpdir(), 'robofrontier-host-'));
  t.after(() => fs.rmSync(run, {recursive:true, force:true}));
  for (const directory of ['private/inputs', 'private/outputs', 'private/state/connections', 'public/inputs'])
    fs.mkdirSync(path.join(run, directory), {recursive:true});
  const write = (name, value) => fs.writeFileSync(path.join(run, name), JSON.stringify(value));
  write('private/inputs/codex.json', {args:[], model:'test-model', provider:'test-provider', effort:'max'});
  write('private/inputs/manifest.json', {model_requested:'test-model', effort_requested:'max'});
  write('private/state/connections/Meta.json', {url:'http://local-test-only'});
  write('public/inputs/roles.json', {roles:{Meta:{kind:'manager'}, worker:{kind:'robot'}}});
  const calls = [], administration = [], physicalCalls = [];
  let handlers, closed = false;
  const rpc = {
    initialize:async () => {},
    close:async () => {closed = true;},
    call:async (method, params) => {
      calls.push({method, params});
      if (method === 'thread/start') return {thread:{id:'policy-thread'}};
      if (method === 'thread/read') return {thread:{id:'policy-thread', status:{type:'idle'}}};
      if (method === 'thread/turns/list') return {data:[]};
      if (method === 'turn/start') return {turn:{id:'initial-turn', status:'inProgress'}};
      return {};
    },
  };
  const childProcess = {
    execFile:(command, args, options, callback) => {
      if (args.includes('robofrontier.runtime_cli')) administration.push(args[args.indexOf('--run-dir') + 2]);
      if (args.includes('robofrontier.pipeline_client')) physicalCalls.push(args[args.indexOf('--call-id') + 2]);
      callback(null, '{}', '');
    },
    exec:() => {throw new Error('Unexpected shell command in fixture');},
    spawn:() => ({exitCode:null, on:() => {}}),
  };
  const module = {exports:{}};
  const dependencies = {
    'node:child_process':childProcess,
    './codex_rpc':{capacityFailure, CodexRpc:{create:async (args, options) => {handlers = options; return rpc;}}},
    './meta_dispatcher':{runMetaDispatcher:async options => onDispatch(options, emit)},
  };
  const source = fs.readFileSync(path.join(__dirname, '../scripts/codex_policy_host.js'), 'utf8');
  vm.runInNewContext(source, {
    require:name => dependencies[name] || require(name), module,
    console, process, Buffer, setTimeout, clearTimeout,
  }, {filename:'codex_policy_host.js'});
  const host = new module.exports.PolicyHost(run, run, 'fake-python');
  function emit(error) {
    handlers.onEvent({method:'turn/completed', params:{threadId:'policy-thread',
      turn:{id:'failed-turn', status:'failed', error}}});
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
    assert.deepEqual(context.administration, ['seal']);
    assert.equal(context.closed(), true);
    assert.equal(context.calls.filter(call => call.method === 'turn/start').length, 1,
      'only the initial turn may start; permanent failures must not trigger a retry');
    assert.deepEqual(context.physicalCalls, ['bind'], 'sealing must not replay any physical actions');
  });
}

test('capacity failures keep the existing wait classification without immediately stopping', async t => {
  for (const message of ['429 Too Many Requests', 'server_overloaded']) {
    const context = fixture(t, async () => {});
    await context.host.startServer();
    context.emit({message});
    assert.equal(context.host.stopped, false);
    assert.ok(context.host.failures.has('policy-thread:failed-turn'));
    const events = fs.readFileSync(path.join(context.run, 'private/outputs/codex-host.jsonl'), 'utf8')
      .trim().split('\n').map(line => JSON.parse(line));
    assert.ok(events.some(event => event.event === 'capacity_wait'));
    assert.equal(fs.existsSync(path.join(context.run, 'private/outputs/model-failure.json')), false);
    assert.equal(context.calls.filter(call => call.method === 'turn/start').length, 0);
    await context.host.rpc.close();
  }
});
