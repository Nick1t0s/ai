// UI-копия как есть + API-копия через app.graphToPrompt() настоящего фронтенда ComfyUI.
import fs from 'node:fs';
import path from 'node:path';
import { openPage, waitFor } from './cdp.mjs';

const [listPath, outRoot, reportPath] = process.argv.slice(2);
const items = JSON.parse(fs.readFileSync(listPath, 'utf8'));
const page = await openPage('http://127.0.0.1:8199/');
await waitFor(page, `!!(window.app && window.app.graph && window.app.graphToPrompt)`);
await new Promise(r => setTimeout(r, 3000));

const report = [];
for (const it of items) {
  const uiDir = path.join(outRoot, it.cat, 'ui');
  const apiDir = path.join(outRoot, it.cat, 'api');
  fs.mkdirSync(uiDir, { recursive: true });
  fs.mkdirSync(apiDir, { recursive: true });
  const raw = fs.readFileSync(it.api_src || it.src, 'utf8');
  fs.copyFileSync(it.src, path.join(uiDir, it.name + '.json'));
  page.logs.length = 0;
  const rec = { ...it, ok: false };
  try {
    const out = await page.evaluate(`(async () => {
      const wf = ${raw};
      await app.loadGraphData(wf, true, false, null, { skipAssetScans: true, silentAssetErrors: true, deferWarnings: true });
      const p = await app.graphToPrompt();
      return JSON.stringify(p.output);
    })()`);
    let api = JSON.parse(out);
    if (Object.keys(api).length === 0) {   // первая загрузка иногда отдаёт пустой граф: повторяем
      await new Promise(r => setTimeout(r, 3000));
      api = JSON.parse(await page.evaluate(`(async () => {
        await app.loadGraphData(${raw}, true, false, null, { skipAssetScans: true, silentAssetErrors: true, deferWarnings: true });
        return JSON.stringify((await app.graphToPrompt()).output);
      })()`));
      rec.retried = true;
    }
    fs.writeFileSync(path.join(apiDir, it.name + '.json'), JSON.stringify(api, null, 1));
    rec.ok = true;
    rec.nodes = Object.keys(api).length;
  } catch (e) {
    rec.error = String(e.message || e).slice(0, 500);
  }
  rec.logs = page.logs.filter(l => !/legacy queue|internal module|deprecated/i.test(l)).slice(0, 8);
  report.push(rec);
  console.log((rec.ok ? 'OK  ' : 'FAIL') + ` ${it.cat}/${it.name}` + (rec.ok ? ` (${rec.nodes} nodes)` : ' ' + rec.error));
}
fs.writeFileSync(reportPath, JSON.stringify(report, null, 1));
await page.close();
