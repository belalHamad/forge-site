# forge-site

The website for Forge on **forgeyourhabit.com**, built with Astro (static) and deployed to GitHub Pages by
GitHub Actions (`.github/workflows/deploy.yml`, plus a daily rebuild for countdowns and seasons).

- EN at `/`, Arabic at `/ar/` (right-to-left), Turkish at `/tr/`. Strings: `src/i18n/{en,ar,tr}.json`
  (the build fails if AR or TR misses a key).
- `/android/`: the Android waitlist (switches to the Play button when `androidState` is `live`).
- `/join/?g=<id>&s=<c|f>&n=<name>&l=<en|ar|tr>`: the group invite page. Old `/join/<token>` paths are forwarded by
  `404.html`. `/.well-known/apple-app-site-association` is generated from `src/data/site.json`
  (`assetlinks.json` too, once the Android signing fingerprint is set).
- Prices come only from `src/data/pricing.json`; store states and links from `src/data/site.json`.
- The legacy pages keep their URLs: `support.html`, `privacy.html` (+ `-ar`), `mosque-data.html`, `data/`
  (now under `public/`). Regenerate the privacy and support pages from the app repo as before.

## One-time setup (Bilal)
1. Repo Settings → Pages → Source: **GitHub Actions** (instead of "Deploy from a branch").
2. MailerLite: create the form and put its POST URL in `site.json` → `waitlistAction`.

## Local
`npm ci && npm run build` → `dist/`. `npm run dev` for a live preview.
