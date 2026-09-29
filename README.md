# forge-site

Public web pages for the Forge habit tracker, served by GitHub Pages:

- **Privacy policy:** https://belalhamad.github.io/forge-site/privacy.html

The Forge app's Settings → Privacy Policy row opens that address, so keep the file name the same.

## Updating the policy

The source text lives in the (private) Forge app repo as `PRIVACY_POLICY.md`. Change it there, then
regenerate the page with `scripts/build_privacy_page.py` (instructions at the top of that script),
update the effective date, and commit the new `privacy.html` here. Don't edit `privacy.html` by hand;
the next regeneration would overwrite the change.
