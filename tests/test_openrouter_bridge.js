const test = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const {normalizeRequest, createBridge} = require('../scripts/openrouter_bridge');

const image = {type:'input_image', image_url:'data:image/png;base64,AAECAwQFBgcICQ==', detail:'original'};
const file = {type:'input_file', filename:'observation.txt', file_data:'data:text/plain;base64,b2JzZXJ2YXRpb24='};

test('tool result text stays text and image/file bytes stay in native user content', () => {
  const normalized = normalizeRequest({model:'test-model', input:[
    {type:'function_call', call_id:'call-observe', name:'robot', arguments:'{}'},
    {type:'function_call_output', call_id:'call-observe', output:[
      {type:'input_text', text:'camera observation'}, image,
      {type:'input_text', text:'attached record'}, file,
    ]},
  ]});
  assert.equal(normalized.input[1].call_id, 'call-observe');
  assert.equal(normalized.input[1].output, 'camera observation\nattached record');
  assert.equal(normalized.input[2].role, 'user');
  assert.deepEqual(normalized.input[2].content.filter(part => part.type !== 'input_text'), [image, file]);
  assert.ok(!normalized.input[1].output.includes('AAECAwQFBgcICQ=='));
  assert.ok(!normalized.input[1].output.includes('b2JzZXJ2YXRpb24='));
});

test('parallel tool outputs remain adjacent before their ordered media message', () => {
  const secondImage = {...image, image_url:'data:image/png;base64,CgsMDQ4PEA=='};
  const nextMessage = {role:'user', content:[{type:'input_text', text:'continue'}]};
  const normalized = normalizeRequest({input:[
    {type:'function_call_output', call_id:'left', output:[{type:'input_text', text:'left'}, image]},
    {type:'function_call_output', call_id:'right', output:[{type:'input_text', text:'right'}, secondImage]},
    nextMessage,
    {type:'function_call_output', call_id:'later', output:'unchanged output'},
  ]});
  assert.deepEqual(normalized.input.slice(0, 2), [
    {type:'function_call_output', call_id:'left', output:'left'},
    {type:'function_call_output', call_id:'right', output:'right'},
  ]);
  const continuationIndex = normalized.input.findIndex(item => item.role === 'user' && item.content?.some(part => part.text === 'continue'));
  assert.ok(continuationIndex > 2);
  const mediaMessages = normalized.input.slice(2, continuationIndex);
  assert.ok(mediaMessages.length > 0);
  assert.ok(mediaMessages.every(item => item.role === 'user'));
  assert.deepEqual(mediaMessages.flatMap(item => item.content).filter(part => part.type !== 'input_text'), [image, secondImage]);
  assert.deepEqual(normalized.input[continuationIndex + 1], {type:'function_call_output', call_id:'later', output:'unchanged output'});
});

test('tool table keeps the robot function and removes unsupported tool types', () => {
  const robot = {type:'function', name:'robot', parameters:{type:'object', properties:{command:{type:'string'}}}};
  const normalized = normalizeRequest({model:'test-model', input:'hello', tools:[
    {type:'custom', name:'freeform'}, robot,
    {type:'namespace', name:'functions', tools:[{type:'function', name:'nested'}]},
  ]});
  assert.deepEqual(normalized.tools, [robot]);
  assert.equal(normalized.input, 'hello');
  assert.equal(normalized.model, 'test-model');
});

async function upstream(t, handler) {
  const server = http.createServer(handler);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => server.close(resolve)));
  return `http://127.0.0.1:${server.address().port}/api/v1`;
}

async function readBody(req) {
  const parts = [];
  for await (const part of req) parts.push(part);
  return JSON.parse(Buffer.concat(parts).toString());
}

test('HTTP bridge normalizes requests, forwards authentication, and streams SSE without waiting for completion', async t => {
  let release;
  const gate = new Promise(resolve => {release = resolve;});
  t.after(() => release());
  let received;
  const first = 'event: response.output_text.delta\ndata: {"delta":"hello"}\n\n';
  const last = 'event: response.completed\ndata: {"id":"done"}\n\n';
  const baseUrl = await upstream(t, async (req, res) => {
    received = {path:req.url, authorization:req.headers.authorization, body:await readBody(req)};
    res.writeHead(201, {'content-type':'text/event-stream', 'x-upstream':'preserved'});
    res.write(first);
    await gate;
    res.end(last);
  });
  const bridge = await createBridge(baseUrl);
  t.after(() => bridge.close());
  const response = await fetch(`${bridge.url}/responses`, {
    method:'POST', headers:{'content-type':'application/json', authorization:'Bearer local-test-token'},
    body:JSON.stringify({model:'test-model', stream:true, input:[
      {type:'function_call_output', call_id:'observe', output:[{type:'input_text', text:'view'}, image]},
    ]}),
  });
  assert.equal(response.status, 201);
  assert.equal(response.headers.get('content-type'), 'text/event-stream');
  const reader = response.body.getReader();
  const chunk = await reader.read();
  assert.equal(Buffer.from(chunk.value).toString(), first);
  release();
  const rest = [];
  for (;;) {
    const chunk = await reader.read();
    if (chunk.done) break;
    rest.push(chunk.value);
  }
  assert.equal(Buffer.concat(rest).toString(), last);
  assert.equal(received.path, '/api/v1/responses');
  assert.equal(received.authorization, 'Bearer local-test-token');
  assert.equal(received.body.input[0].output, 'view');
  assert.equal(received.body.input[1].role, 'user');
  assert.deepEqual(received.body.input[1].content.filter(part => part.type !== 'input_text'), [image]);
});

test('HTTP bridge preserves upstream error status and response bytes', async t => {
  const errorBody = '{"error":{"message":"provider quota exceeded","code":429}}';
  const baseUrl = await upstream(t, async (req, res) => {
    await readBody(req);
    res.writeHead(429, {'content-type':'application/json', 'retry-after':'30'});
    res.end(errorBody);
  });
  const bridge = await createBridge(baseUrl);
  t.after(() => bridge.close());
  const response = await fetch(`${bridge.url}/responses`, {
    method:'POST', headers:{'content-type':'application/json'}, body:JSON.stringify({input:[]}),
  });
  assert.equal(response.status, 429);
  assert.equal(response.headers.get('retry-after'), '30');
  assert.equal(await response.text(), errorBody);
});
