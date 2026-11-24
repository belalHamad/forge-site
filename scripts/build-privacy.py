"""Builds public/privacy.html and privacy-ar.html from ForgeNative's PRIVACY_POLICY(.ar).md."""
import re, sys, markdown
src_en, src_ar, date_en, date_ar = sys.argv[1:5]
tpl_head = open('public/privacy-ar.html').read()
style = re.search(r'<style>.*?</style>', tpl_head, re.S).group(0)
def build(src, out, lang, title, desc, date, other, other_label, other_lang):
    md = open(src).read().replace('{{EFFECTIVE_DATE}}', date)
    lines = md.split('\n')
    # meta lines (bold label lines right after the h1) become p.meta
    body = markdown.markdown(md, extensions=['extra', 'sane_lists'])
    body = re.sub(r'<h1>.*?</h1>\s*', '', body, count=1, flags=re.S)
    meta = re.match(r'\s*<p>(.*?)</p>', body, re.S)
    if meta:
        parts = [x.strip() for x in meta.group(1).split('\n') if x.strip()]
        body = body[meta.end():]
        metas = ''.join(f'<p class="meta">{p}</p>\n' for p in parts)
    else:
        metas = ''
    body = re.sub(r'(?<![">])(support@forgeyourhabit\.com)', r'<a href="mailto:\1">\1</a>', body)
    metas = re.sub(r'(?<![">])(support@forgeyourhabit\.com)', r'<a href="mailto:\1">\1</a>', metas)
    d = 'rtl' if lang == 'ar' else 'ltr'
    html = f'''<!doctype html>
<html lang="{lang}" dir="{d}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://forgeyourhabit.com/{out.split('/')[-1]}">
<link rel="alternate" hreflang="{other_lang}" href="https://forgeyourhabit.com/{other}">
{style}
</head>
<body>
<main>
<nav class="lang"><a href="{other}" hreflang="{other_lang}">{other_label}</a></nav>
<h1>{title}</h1>
{metas}{body}
</main>
</body>
</html>
'''
    open(out, 'w').write(html)
build(src_en, 'public/privacy.html', 'en', 'Forge Privacy Policy', 'How the Forge app handles your data.', date_en, 'privacy-ar.html', 'العربية', 'ar')
build(src_ar, 'public/privacy-ar.html', 'ar', 'سياسة الخصوصية لتطبيق Forge', 'كيف يتعامل تطبيق Forge مع بياناتك.', date_ar, 'privacy.html', 'English', 'en')
