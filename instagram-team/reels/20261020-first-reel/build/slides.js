// 1本目のスライド画像(1080x1920)を生成する。
// 使い方: node slides.js <fontDir> <outDir>
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const [fontDir, outDir] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const font = (w, sub = 'japanese') => `file://${path.join(fontDir, `noto-sans-jp-${sub}-${w}-normal.woff2`)}`;

const C = { bg: '#FBF7F0', ink: '#2B2B2B', sub: '#6B6459', teal: '#2F7D7A', tealSoft: '#DCEDEB', warm: '#E8A23B', warmSoft: '#FBEBD0', line: '#E6DED1' };

const css = `
@font-face { font-family: N; font-weight: 500; src: url(${font(500)}); }
@font-face { font-family: N; font-weight: 700; src: url(${font(700)}); }
@font-face { font-family: N; font-weight: 900; src: url(${font(900)}); }
@font-face { font-family: N; font-weight: 500; src: url(${font(500, 'latin')}); unicode-range: U+0000-00FF; }
@font-face { font-family: N; font-weight: 700; src: url(${font(700, 'latin')}); unicode-range: U+0000-00FF; }
@font-face { font-family: N; font-weight: 900; src: url(${font(900, 'latin')}); unicode-range: U+0000-00FF; }
* { box-sizing: border-box; margin: 0; }
body { width: 1080px; height: 1920px; background: ${C.bg}; font-family: N, 'IPAPGothic', sans-serif; color: ${C.ink}; }
.safe { position: absolute; left: 90px; right: 90px; top: 260px; bottom: 420px; display: flex; flex-direction: column; }
.kicker { font-weight: 700; font-size: 40px; color: ${C.teal}; letter-spacing: 2px; }
.h1 { font-weight: 900; font-size: 112px; line-height: 1.25; }
.h2 { font-weight: 900; font-size: 96px; line-height: 1.2; }
.lead { font-weight: 700; font-size: 52px; line-height: 1.5; color: ${C.ink}; }
.note { font-weight: 500; font-size: 32px; color: ${C.sub}; }
.page { position: absolute; right: 90px; top: 180px; font-weight: 700; font-size: 34px; color: ${C.sub}; }
.tag { display: flex; align-items: center; gap: 28px; background: #fff; border: 3px solid ${C.line}; border-radius: 28px; padding: 30px 36px; }
.tag b { flex: none; font-weight: 900; font-size: 40px; padding: 10px 24px; border-radius: 16px; background: ${C.tealSoft}; color: ${C.teal}; }
.tag b.w { background: ${C.warmSoft}; color: #A86A0C; }
.tag span { font-weight: 700; font-size: 50px; }
.mark { color: ${C.teal}; }
`;

const page = (n, body) => `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head>
<body>${n ? `<div class="page">${n}/8</div>` : ''}<div class="safe">${body}</div></body></html>`;

// 方式ごとの簡易図解(SVG)
const icons = {
  steam: `<svg viewBox="0 0 400 300" width="400" height="300"><rect x="110" y="140" width="180" height="130" rx="28" fill="${C.teal}"/><rect x="150" y="180" width="100" height="16" rx="8" fill="${C.tealSoft}"/>
    <path d="M160 120 q-20 -30 0 -60 q20 -30 0 -60" stroke="${C.warm}" stroke-width="14" fill="none" stroke-linecap="round"/>
    <path d="M200 120 q-20 -30 0 -60 q20 -30 0 -60" stroke="${C.warm}" stroke-width="14" fill="none" stroke-linecap="round"/>
    <path d="M240 120 q-20 -30 0 -60 q20 -30 0 -60" stroke="${C.warm}" stroke-width="14" fill="none" stroke-linecap="round"/></svg>`,
  vapor: `<svg viewBox="0 0 400 300" width="400" height="300"><circle cx="100" cy="150" r="70" fill="none" stroke="${C.teal}" stroke-width="14"/>
    <path d="M100 150 l0 -55 M100 150 l48 28 M100 150 l-48 28" stroke="${C.teal}" stroke-width="14" stroke-linecap="round"/>
    <path d="M190 120 h50 M190 150 h50 M190 180 h50" stroke="${C.sub}" stroke-width="10" stroke-linecap="round"/>
    <rect x="260" y="60" width="70" height="180" rx="14" fill="${C.tealSoft}" stroke="${C.teal}" stroke-width="10"/>
    <path d="M275 90 v120 M295 90 v120 M315 90 v120" stroke="${C.teal}" stroke-width="6"/></svg>`,
  ultra: `<svg viewBox="0 0 400 300" width="400" height="300"><rect x="130" y="170" width="140" height="100" rx="26" fill="${C.teal}"/>
    <path d="M150 150 q50 -30 100 0 M130 115 q70 -45 140 0 M110 80 q90 -60 180 0" stroke="${C.warm}" stroke-width="12" fill="none" stroke-linecap="round"/>
    <circle cx="170" cy="30" r="9" fill="${C.sub}"/><circle cx="210" cy="18" r="9" fill="${C.sub}"/><circle cx="250" cy="34" r="9" fill="${C.sub}"/></svg>`,
  hybrid: `<svg viewBox="0 0 400 300" width="400" height="300"><circle cx="90" cy="150" r="66" fill="none" stroke="${C.warm}" stroke-width="14"/>
    <path d="M90 150 l0 -50 M90 150 l44 26 M90 150 l-44 26" stroke="${C.warm}" stroke-width="14" stroke-linecap="round"/>
    <path d="M180 120 q20 -12 40 0 t40 0 M180 150 q20 -12 40 0 t40 0 M180 180 q20 -12 40 0 t40 0" stroke="${C.warm}" stroke-width="10" fill="none" stroke-linecap="round"/>
    <rect x="280" y="60" width="70" height="180" rx="14" fill="${C.tealSoft}" stroke="${C.teal}" stroke-width="10"/>
    <path d="M295 90 v120 M315 90 v120 M335 90 v120" stroke="${C.teal}" stroke-width="6"/></svg>`,
};

const method = (n, name, how, icon, tags) => page(n, `
  <div class="kicker">方式 ${n - 2} / 4</div>
  <div class="h2" style="margin-top:20px">${name}</div>
  <div class="lead" style="margin-top:28px">${how}</div>
  <div style="margin:50px 0; display:flex; justify-content:center">${icons[icon]}</div>
  <div style="display:flex; flex-direction:column; gap:26px">${tags.map(([k, v, w]) => `<div class="tag"><b class="${w ? 'w' : ''}">${k}</b><span>${v}</span></div>`).join('')}</div>
  <div class="note" style="margin-top:auto; padding-top:24px">※特徴は一般的な傾向です。機種によって異なります</div>`);

const slides = [
  page(0, `
    <div class="kicker">買う前に30秒</div>
    <div class="h1" style="margin-top:40px">加湿器、<br><span class="mark">「方式」</span>で<br>選んでますか?</div>
    <div class="lead" style="margin-top:60px; color:${C.sub}">4方式の違いを比較</div>`),
  page(2, `
    <div class="h2">加湿器は<br>大きく<span class="mark">4方式</span></div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:24px; margin-top:56px">
      ${['スチーム式', '気化式', '超音波式', 'ハイブリッド式'].map(t => `<div class="tag" style="justify-content:center"><span>${t}</span></div>`).join('')}
    </div>
    <div class="lead" style="margin-top:90px">見るのはこの3つ</div>
    <div style="display:flex; gap:20px; margin-top:28px">${['電気代', '加湿力', 'お手入れ'].map(t => `<div class="tag" style="flex:1; justify-content:center; background:${C.tealSoft}; border-color:${C.tealSoft}"><span style="color:${C.teal}">${t}</span></div>`).join('')}</div>`),
  method(3, 'スチーム式', 'お湯を沸かして<br>蒸気で加湿', 'steam', [['加湿力', '高め'], ['電気代', '高め'], ['注意', '吹き出し口が熱い', 1]]),
  method(4, '気化式', '濡れたフィルターに<br>風を当てて加湿', 'vapor', [['電気代', '安め(ヒーターなし)'], ['注意', '運転音・本体が大きめ', 1]]),
  method(5, '超音波式', '振動で水を<br>細かい霧にして加湿', 'ultra', [['電気代', '安め'], ['注意', 'こまめなお手入れが必要', 1]]),
  method(6, 'ハイブリッド式', '温風でフィルターの<br>水を気化して加湿', 'hybrid', [['加湿力', '気化式より高め'], ['電気代', 'そのぶん、かかる', 1]]),
  page(7, `
    <div class="h2">迷ったら</div>
    <div style="display:flex; flex-direction:column; gap:24px; margin-top:56px">
      ${[['電気代を抑えたい', '気化式'], ['しっかり加湿したい', 'スチーム式'], ['手軽に始めたい', '超音波式'], ['バランス重視', 'ハイブリッド式']]
        .map(([k, v]) => `<div class="tag" style="justify-content:space-between"><span style="font-size:44px; color:${C.sub}">${k}</span><span class="mark">${v}</span></div>`).join('')}
    </div>
    <div class="lead" style="margin-top:56px">＋部屋の広さ(適用畳数)も確認</div>
    <div class="note" style="margin-top:20px">小さな子どもがいる家は、スチーム式の置き場所に注意</div>`),
  page(8, `
    <div style="margin-top:120px; display:flex; justify-content:center">
      <svg viewBox="0 0 200 260" width="200" height="260"><path d="M30 20 h140 v220 l-70 -50 l-70 50 z" fill="${C.teal}"/></svg>
    </div>
    <div class="h2" style="margin-top:80px; text-align:center">買う前に<br>見返せるよう<br><span class="mark">保存</span>しておいてね</div>`),
];

(async () => {
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [i, html] of slides.entries()) {
    await p.setContent(html, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(outDir, `slide${i + 1}.png`) });
  }
  await browser.close();
})();
