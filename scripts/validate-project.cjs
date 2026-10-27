const fs = require('node:fs');
const path = require('node:path');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
const cap = JSON.parse(fs.readFileSync('capacitor.config.json', 'utf8'));
const required = ['www/index.html', 'www/manifest.json', 'www/sw.js', '.github/workflows/android.yml', 'scripts/patch-android.py', 'resources/mipmap-xxxhdpi/ic_launcher_foreground.png'];
for (const file of required) if (!fs.existsSync(file)) throw new Error(`Required file missing: ${file}`);
JSON.parse(fs.readFileSync('www/manifest.json', 'utf8'));
if (!cap.appId || !/^[a-zA-Z][\w]*(\.[a-zA-Z][\w]*)+$/.test(cap.appId)) throw new Error('Invalid Capacitor appId');
if (!cap.appName || cap.webDir !== 'www') throw new Error('Invalid Capacitor appName/webDir');
const deps = pkg.dependencies || {};
for (const d of ['@capacitor/core', '@capacitor/android', '@capacitor/filesystem', '@capacitor/share']) {
  if (!deps[d]) throw new Error(`Dependency missing in package.json: ${d}`);
}
if (!pkg.devDependencies?.['@capacitor/cli']) throw new Error('@capacitor/cli missing');
const html = fs.readFileSync(path.join(cap.webDir, 'index.html'), 'utf8');
if (!/<html\b/i.test(html) || !/<\/html>/i.test(html) || !/<script\b/i.test(html)) throw new Error('Main HTML looks incomplete');
console.log('Project configuration and required files validated.');
