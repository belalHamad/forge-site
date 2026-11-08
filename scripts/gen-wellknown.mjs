// Writes the app-link files GitHub Pages serves from /.well-known/ (needs .nojekyll).
import { readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
const site = JSON.parse(readFileSync(new URL('../src/data/site.json', import.meta.url)));
const dir = new URL('../public/.well-known/', import.meta.url);
mkdirSync(dir, { recursive: true });
const appID = `${site.teamId}.${site.bundleId}`;
const aasa = { applinks: { details: [{ appIDs: [appID], components: [{ '/': '/join/*', comment: 'Group invites' }] }] } };
writeFileSync(new URL('apple-app-site-association', dir), JSON.stringify(aasa, null, 2) + '\n');
const al = new URL('assetlinks.json', dir);
if (site.androidSha256.length) {
  writeFileSync(al, JSON.stringify([{ relation: ['delegate_permission/common.handle_all_urls'],
    target: { namespace: 'android_app', package_name: site.androidPackage, sha256_cert_fingerprints: site.androidSha256 } }], null, 2) + '\n');
} else { rmSync(al, { force: true }); }
console.log('well-known: AASA for', appID, site.androidSha256.length ? '+ assetlinks' : '(no assetlinks yet)');
