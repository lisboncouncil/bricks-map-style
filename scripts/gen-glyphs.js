// Generate MapLibre glyph PBFs from a TTF.
// Usage: node scripts/gen-glyphs.js <font.ttf> "<Font Stack Name>" <outdir>
// MIT licence, The Lisbon Council 2026.
const fontnik = require('fontnik'); const fs = require('fs'); const path = require('path');
const [ttf, name, out] = process.argv.slice(2);
const buf = fs.readFileSync(ttf);
const dir = path.join(out, name); fs.mkdirSync(dir, { recursive: true });
let n = 0, nonEmpty = 0;
const next = (s) => {
  if (s > 65280) { console.log(name, n, 'files', nonEmpty, 'non-trivial'); return; }
  fontnik.range({ font: buf, start: s, end: s + 255 }, (err, data) => {
    if (err) throw err;
    fs.writeFileSync(path.join(dir, `${s}-${s + 255}.pbf`), data); n++; if (data.length > 60) nonEmpty++;
    next(s + 256);
  });
};
next(0);
