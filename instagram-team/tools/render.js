// リールのスライド画像(1080x1920)を spec.json から生成する。
// 使い方: node render.js <fontDir> <reelDir>   (reelDir/spec.json を読み、reelDir/slides/ に出力)
// フォント: @fontsource/noto-sans-jp(OFL)。npm install @fontsource/noto-sans-jp@5.0.19 で取得し、その files/ を fontDir に渡す
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const [fontDir, reelDir] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(path.join(reelDir, 'spec.json'), 'utf8'));
const outDir = path.join(reelDir, 'slides');
fs.mkdirSync(outDir, { recursive: true });

const b64 = (sub, w) => fs.readFileSync(path.join(fontDir, `noto-sans-jp-${sub}-${w}-normal.woff2`)).toString('base64');
const faces = [500, 700, 900].flatMap(w => [
  `@font-face { font-family: N; font-weight: ${w}; src: url(data:font/woff2;base64,${b64('japanese', w)}); }`,
  `@font-face { font-family: N; font-weight: ${w}; src: url(data:font/woff2;base64,${b64('latin', w)}); unicode-range: U+0000-00FF; }`,
]).join('\n');

const C = { bg: '#FBF7F0', ink: '#2B2B2B', sub: '#6B6459', teal: '#2F7D7A', tealSoft: '#DCEDEB', warm: '#E8A23B', warmSoft: '#FBEBD0', warmInk: '#A86A0C', line: '#E6DED1', red: '#B4442F', redSoft: '#F7E1DC' };

const css = `${faces}
* { box-sizing: border-box; margin: 0; }
body { width: 1080px; height: 1920px; background: ${C.bg}; font-family: N, sans-serif; color: ${C.ink}; }
.safe { position: absolute; left: 90px; right: 90px; top: 260px; bottom: 420px; display: flex; flex-direction: column; }
.page { position: absolute; right: 90px; top: 180px; font-weight: 700; font-size: 34px; color: ${C.sub}; }
.kicker { font-weight: 700; font-size: 40px; color: ${C.teal}; letter-spacing: 2px; }
.h1 { font-weight: 900; font-size: 112px; line-height: 1.25; }
.h2 { font-weight: 900; font-size: 88px; line-height: 1.22; }
.lead { font-weight: 700; font-size: 50px; line-height: 1.5; }
.note { font-weight: 500; font-size: 32px; line-height: 1.5; color: ${C.sub}; }
.mark { color: ${C.teal}; }
.box { background: #fff; border: 3px solid ${C.line}; border-radius: 28px; padding: 30px 36px; }
.tag { display: flex; align-items: center; gap: 28px; }
.tag b { flex: none; font-weight: 900; font-size: 40px; padding: 10px 24px; border-radius: 16px; background: ${C.tealSoft}; color: ${C.teal}; }
.tag b.w { background: ${C.warmSoft}; color: ${C.warmInk}; }
.tag span { font-weight: 700; font-size: 48px; line-height: 1.35; }
.item { font-weight: 700; font-size: 48px; line-height: 1.45; display: flex; gap: 20px; }
.item i { font-style: normal; color: ${C.teal}; flex: none; }
.formula { background: ${C.tealSoft}; border-radius: 28px; padding: 44px 36px; font-weight: 900; font-size: 60px; line-height: 1.5; color: ${C.teal}; text-align: center; }
.warn .box { border-color: ${C.red}; background: ${C.redSoft}; }
.warn .h2 { color: ${C.red}; }
.warn .item i { color: ${C.red}; }
`;

const html = (i, n, body, cls = '') => `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head>
<body class="${cls}">${i ? `<div class="page">${i + 1}/${n}</div>` : ''}<div class="safe">${body}</div></body></html>`;

const opt = (v, f) => (v ? f(v) : '');
const noteAtBottom = s => opt(s.note, v => `<div class="note" style="margin-top:auto; padding-top:24px">${v}</div>`);

const render = {
  cover: s => `
    ${opt(s.kicker, v => `<div class="kicker">${v}</div>`)}
    <div class="h1" style="margin-top:40px">${s.title}</div>
    ${opt(s.sub, v => `<div class="lead" style="margin-top:60px; color:${C.sub}">${v}</div>`)}`,
  bullets: s => `
    ${opt(s.kicker, v => `<div class="kicker" style="margin-bottom:20px">${v}</div>`)}
    <div class="h2">${s.title}</div>
    ${opt(s.lead, v => `<div class="lead" style="margin-top:36px">${v}</div>`)}
    <div class="box" style="margin-top:56px; display:flex; flex-direction:column; gap:28px">
      ${s.items.map(t => `<div class="item"><i>${s.icon || '●'}</i><div>${t}</div></div>`).join('')}
    </div>
    ${noteAtBottom(s)}`,
  formula: s => `
    ${opt(s.kicker, v => `<div class="kicker" style="margin-bottom:20px">${v}</div>`)}
    <div class="h2">${s.title}</div>
    <div class="formula" style="margin-top:64px">${s.formula}</div>
    ${opt(s.lead, v => `<div class="lead" style="margin-top:48px">${v}</div>`)}
    ${noteAtBottom(s)}`,
  tags: s => `
    ${opt(s.kicker, v => `<div class="kicker" style="margin-bottom:20px">${v}</div>`)}
    <div class="h2">${s.title}</div>
    ${opt(s.lead, v => `<div class="lead" style="margin-top:28px; color:${C.sub}">${v}</div>`)}
    <div style="margin-top:60px; display:flex; flex-direction:column; gap:26px">
      ${s.tags.map(([k, v, w]) => `<div class="box tag"><b class="${w ? 'w' : ''}">${k}</b><span>${v}</span></div>`).join('')}
    </div>
    ${noteAtBottom(s)}`,
  cta: s => `
    <div style="margin-top:120px; display:flex; justify-content:center">
      <svg viewBox="0 0 200 260" width="200" height="260"><path d="M30 20 h140 v220 l-70 -50 l-70 50 z" fill="${C.teal}"/></svg>
    </div>
    <div class="h2" style="margin-top:80px; text-align:center">${s.title}</div>`,
};

(async () => {
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  const n = spec.slides.length;
  for (const [i, s] of spec.slides.entries()) {
    await p.setContent(html(i, n, render[s.type](s), s.warn ? 'warn' : ''), { waitUntil: 'load' });
    await p.evaluate(async () => { await document.fonts.load('900 10px N', 'あA1'); await document.fonts.ready; });
    await p.screenshot({ path: path.join(outDir, `slide${i + 1}.png`) });
  }
  await browser.close();
})();
