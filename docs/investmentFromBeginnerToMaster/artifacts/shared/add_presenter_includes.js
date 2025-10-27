// filepath: artifacts/shared/add_presenter_includes.js
// Node.js script to batch-insert shared presenter controls into lesson_ppt.html files
// Usage: cd artifacts && node shared/add_presenter_includes.js

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..'); // artifacts

function walk(dir) {
  const res = [];
  const files = fs.readdirSync(dir, { withFileTypes: true });
  for (const f of files) {
    const p = path.join(dir, f.name);
    if (f.isDirectory()) {
      res.push(...walk(p));
    } else if (f.isFile() && f.name === 'lesson_ppt.html') {
      res.push(p);
    }
  }
  return res;
}

function ensureIncludes(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  const cssInclude = '<link rel="stylesheet" href="../../shared/presenter_controls.css">';
  const jsInclude = '<script src="../../shared/presenter_controls.js"></script>';

  let changed = false;

  if (!content.includes('presenter_controls.css')) {
    // insert css include into head: after first <head> or before </head>
    if (content.includes('</head>')) {
      content = content.replace('</head>', cssInclude + '\n</head>');
    } else if (content.includes('<head>')) {
      content = content.replace('<head>', '<head>\n' + cssInclude);
    } else {
      // fallback: prepend
      content = cssInclude + '\n' + content;
    }
    changed = true;
  }

  if (!content.includes('presenter_controls.js')) {
    // insert JS before </body>
    if (content.includes('</body>')) {
      content = content.replace('</body>', jsInclude + '\n</body>');
    } else {
      // append
      content = content + '\n' + jsInclude;
    }
    changed = true;
  }

  if (changed) {
    fs.writeFileSync(filePath, content, 'utf8');
  }
  return changed;
}

(function main() {
  console.log('Scanning artifacts for lesson_ppt.html...');
  const pptFiles = walk(root);
  console.log('Found', pptFiles.length, 'lesson_ppt.html files');
  const modified = [];
  for (const f of pptFiles) {
    try {
      const did = ensureIncludes(f);
      if (did) modified.push(f);
    } catch (e) {
      console.error('Failed to process', f, e.message);
    }
  }
  console.log('Modified', modified.length, 'files');
  if (modified.length) console.log(modified.join('\n'));
})();

