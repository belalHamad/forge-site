# forge-site

Public web pages for the Forge habit tracker, served by GitHub Pages on **forgeyourhabit.com**
(`CNAME`; DNS at Cloudflare, "DNS only"). Old `belalhamad.github.io/forge-site/…` links redirect
to the same page on the domain.

- **Home:** https://forgeyourhabit.com/ (`index.html`; the App Store Marketing URL)
- **Privacy policy:** https://forgeyourhabit.com/privacy.html (Arabic: `privacy-ar.html`)
- **Support:** https://forgeyourhabit.com/support.html (Arabic: `support-ar.html`; the App Store Support URL)
- **Mosque data (ODbL):** https://forgeyourhabit.com/mosque-data.html (the OpenStreetMap-derived
  `data/WorldMosques.bin` and `data/build_mosque_index.py`, offered under ODbL 1.0; source in the app repo)
- **Email:** support@forgeyourhabit.com (forwarded by Cloudflare)

The app links to these addresses (`AppLinks` in the app repo), so keep the file names the same.

## Updating the policy and the support page

The sources live in the (private) Forge app repo: `PRIVACY_POLICY.md` / `PRIVACY_POLICY.ar.md` and
`SUPPORT.md` / `SUPPORT.ar.md`. Update each language pair together. Change them there, regenerate the
pages with `scripts/build_privacy_page.py` (instructions at the top of that script), update the
policy's effective date, and commit the new HTML here. Don't edit the generated pages by hand; the next
regeneration would overwrite the change.
