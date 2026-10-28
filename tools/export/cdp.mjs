// Минимальный CDP-клиент: открывает вкладку с фронтендом ComfyUI и выполняет в ней JS.
const DEVTOOLS = 'http://127.0.0.1:9333';

export async function openPage(url) {
  const r = await fetch(`${DEVTOOLS}/json/new?${encodeURIComponent(url)}`, { method: 'PUT' });
  const info = await r.json();
  const ws = new WebSocket(info.webSocketDebuggerUrl);
  await new Promise((ok, err) => { ws.onopen = ok; ws.onerror = err; });
  let id = 0;
  const pending = new Map();
  const logs = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
    else if (m.method === 'Runtime.consoleAPICalled' && ['error', 'warning'].includes(m.params.type)) {
      logs.push(m.params.type + ': ' + m.params.args.map(a => a.value ?? a.description ?? '').join(' ').slice(0, 300));
    } else if (m.method === 'Runtime.exceptionThrown') {
      logs.push('exception: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 300));
    }
  };
  const send = (method, params = {}) => new Promise((ok) => { const i = ++id; pending.set(i, ok); ws.send(JSON.stringify({ id: i, method, params })); });
  await send('Runtime.enable');
  const evaluate = async (expression) => {
    const m = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true, timeout: 120000 });
    if (m.error) throw new Error(JSON.stringify(m.error));
    if (m.result.exceptionDetails) throw new Error(m.result.exceptionDetails.exception?.description || m.result.exceptionDetails.text);
    return m.result.result.value;
  };
  const close = async () => { ws.close(); await fetch(`${DEVTOOLS}/json/close/${info.id}`); };
  return { evaluate, close, logs };
}

export async function waitFor(page, expr, ms = 120000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    try { if (await page.evaluate(expr)) return true; } catch (e) { /* страница ещё грузится */ }
    await new Promise(r => setTimeout(r, 500));
  }
  throw new Error('timeout waiting for ' + expr);
}
