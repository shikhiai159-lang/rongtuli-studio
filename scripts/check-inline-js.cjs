const fs = require('node:fs');
const { spawnSync } = require('node:child_process');
const html = fs.readFileSync('www/index.html', 'utf8');
const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)];
if (!scripts.length) throw new Error('No inline script blocks found');
let checked = 0;
let allJs = '';
for (let i = 0; i < scripts.length; i++) {
  const attrs = scripts[i][1] || '';
  const body = scripts[i][2] || '';
  if (/\bsrc\s*=/.test(attrs) || !body.trim()) continue;
  const result = spawnSync(process.execPath, ['--check', '-'], { input: body, encoding: 'utf8' });
  if (result.status !== 0) {
    process.stderr.write(`Inline script ${i + 1} failed syntax check:\n${result.stderr}`);
    process.exit(result.status || 1);
  }
  allJs += body + '\n';
  checked++;
}
if (!checked) throw new Error('No inline JavaScript was checked');

// service worker syntax
const sw = spawnSync(process.execPath, ['--check', 'www/sw.js'], { encoding: 'utf8' });
if (sw.status !== 0) {
  process.stderr.write(`www/sw.js failed syntax check:\n${sw.stderr}`);
  process.exit(sw.status || 1);
}

// every $('id') used in the script must exist as an element id in the HTML
// (the only id created from script is none; the onion canvas lives in the markup)
const htmlOnly = html.replace(/<script\b[\s\S]*?<\/script\s*>/gi, '');
const ids = new Set([...htmlOnly.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]));
const used = new Set([...allJs.matchAll(/\$\('([^']+)'\)/g)].map(m => m[1]));
const missing = [...used].filter(id => !ids.has(id));
if (missing.length) {
  process.stderr.write(`Script uses element ids that do not exist in the HTML: ${missing.join(', ')}\n`);
  process.exit(1);
}
console.log(`JavaScript syntax OK (${checked} inline script block(s)); ${used.size} element ids resolved; sw.js OK.`);
