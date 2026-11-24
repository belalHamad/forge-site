const base = 'https://forgeyourhabit.com';
const groups: string[][] = [
  ['/', '/ar/', '/tr/'],
  ['/android/', '/ar/android/', '/tr/android/'],
];
const singles = ['/privacy.html', '/privacy-ar.html', '/support.html', '/support-ar.html'];
const langOf = (p: string) => (p.startsWith('/ar/') ? 'ar' : p.startsWith('/tr/') ? 'tr' : 'en');

export function GET() {
  const today = new Date().toISOString().slice(0, 10);
  const urls = groups.flatMap((g) =>
    g.map((p) => {
      const alts = g.map((q) => `<xhtml:link rel="alternate" hreflang="${langOf(q)}" href="${base}${q}"/>`).join('');
      const xd = `<xhtml:link rel="alternate" hreflang="x-default" href="${base}${g[0]}"/>`;
      return `<url><loc>${base}${p}</loc><lastmod>${today}</lastmod>${alts}${xd}</url>`;
    }),
  ).concat(singles.map((p) => `<url><loc>${base}${p}</loc></url>`));
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${urls.join('')}</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
