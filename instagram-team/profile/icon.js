// プロフィールアイコン(1080x1080)を生成する。円形に切り抜かれても収まるよう中央に配置。
// 使い方: node icon.js <fontDir> <outFile>
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const [fontDir, out] = process.argv.slice(2);
const f = w => `data:font/woff2;base64,${require('fs').readFileSync(path.join(fontDir, `noto-sans-jp-japanese-${w}-normal.woff2`)).toString('base64')}`;
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: N; font-weight: 900; src: url(${f(900)}); }
* { margin: 0; box-sizing: border-box; }
body { width: 1080px; height: 1080px; background: #FBF7F0; display: flex; align-items: center; justify-content: center; font-family: N; }
.c { width: 1080px; height: 1080px; border: 34px solid #2F7D7A; border-radius: 50%; background: #FBF7F0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; }
.t { font-weight: 900; font-size: 128px; color: #2B2B2B; line-height: 1.15; text-align: center; }
.t span { color: #2F7D7A; }
</style></head><body><div class="c">
<svg viewBox="0 0 200 170" width="300" height="255">
  <path d="M40 60 h120 l-12 100 h-96 z" fill="#E8A23B"/>
  <path d="M70 60 v-18 a30 30 0 0 1 60 0 v18" fill="none" stroke="#2B2B2B" stroke-width="12" stroke-linecap="round"/>
  <path d="M75 108 l18 18 l34 -38" fill="none" stroke="#FBF7F0" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
<div class="t">くらしの<br><span>買い物ノート</span></div>
</div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
  await p.setContent(html, { waitUntil: 'load' });
  await p.evaluate(async () => { await document.fonts.load('900 128px N', 'くらしの買い物ノート'); await document.fonts.ready; });
  await p.screenshot({ path: out });
  await b.close();
})();
