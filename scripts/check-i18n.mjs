// Fails the build when a language file misses a key that English has.
import { readFileSync } from 'node:fs';
const load = (l) => JSON.parse(readFileSync(new URL(`../src/i18n/${l}.json`, import.meta.url)));
const flat = (o, p = '') => Object.entries(o).flatMap(([k, v]) =>
  v && typeof v === 'object' && !Array.isArray(v) ? flat(v, `${p}${k}.`) : [`${p}${k}`]);
const en = new Set(flat(load('en')));
let bad = 0;
for (const l of ['ar', 'tr']) {
  const keys = new Set(flat(load(l)));
  for (const k of en) if (!keys.has(k)) { console.error(`i18n: ${l} is missing ${k}`); bad++; }
}
if (bad) process.exit(1);
console.log('i18n: all keys present');
