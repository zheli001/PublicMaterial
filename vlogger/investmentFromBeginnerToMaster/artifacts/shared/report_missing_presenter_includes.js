// filepath: artifacts/shared/report_missing_presenter_includes.js
// Scans artifacts tree for lesson_ppt.html files and reports which ones lack presenter_controls includes
const fs = require('fs');
const path = require('path');

function walk(dir) {
  let results = [];
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const stat = fs.statSync(p);
    if (stat.isDirectory()) results = results.concat(walk(p));
    else if (stat.isFile() && name === 'lesson_ppt.html') results.push(p);
  }
  return results;
}

const root = path.resolve(__dirname, '..');
const files = walk(root);
const missing = [];
for (const f of files) {
  const txt = fs.readFileSync(f, 'utf8');
  if (!txt.includes('presenter_controls.css') || !txt.includes('presenter_controls.js')) missing.push(f);
}
console.log('Total lesson_ppt.html files:', files.length);
console.log('Files missing presenter includes:', missing.length);
missing.forEach(m => console.log(m));

