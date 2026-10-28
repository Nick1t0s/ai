// Как фронтенд раскладывает widgets_values у свежесозданной ноды: имена виджетов и значения по умолчанию.
import { openPage, waitFor } from './cdp.mjs';
const types = process.argv.slice(2);
const page = await openPage('http://127.0.0.1:8199/');
await waitFor(page, `!!(window.app && window.app.graph && window.app.graphToPrompt)`);
await page.evaluate(`app.loadGraphData({nodes: [], links: [], version: 0.4}, true, false)`);
for (const t of types) {
  const r = await page.evaluate(`(async () => {
    const n = LiteGraph.createNode(${JSON.stringify(t)});
    app.graph.add(n);
    await new Promise(r => setTimeout(r, 1500));
    const s = n.serialize();
    return JSON.stringify({ widgets: n.widgets.map(w => [w.name, w.type, w.options?.serialize, w.serialize]), values: s.widgets_values });
  })()`);
  console.log(t, r);
}
await page.close();
