# Deploying summitspringpartners.com

This is a plain static site. No build step, no dependencies, nothing to
install. Deploying means copying files to a web host.

## What to upload

Upload these files and folders, keeping the exact same structure:

```
index.html
approach.html
ai-partner.html
coaching.html
about.html
404.html
favicon.ico
robots.txt
sitemap.xml
assets/          (all files)
css/             (all files)
fonts/           (all files)
```

Do NOT upload: `copy/`, `DEPLOY.md`, or the `.git` folder. They are
source material, not the site. (Most hosts ignore `.git` automatically;
if you are FTPing by hand, just don't select it.)

Everything must land in the web root (often called `public_html`, `www`,
or `htdocs`) so that `index.html` sits at the top level. The homepage
must be reachable at `https://summitspringpartners.com/` — if you see it
at `/site/index.html` or similar, the files are one folder too deep.

## Host-specific notes

**Netlify / Vercel / Cloudflare Pages** — drag the folder in or point
them at this git repo with no build command and this directory as the
publish root. All three serve `404.html` for missing pages automatically.
This is the easiest option.

**GitHub Pages** — push this repo to GitHub, enable Pages on the `main`
branch, root folder. `404.html` works automatically. Set the custom
domain to `summitspringpartners.com` in the Pages settings and follow
its DNS instructions.

**Classic shared hosting (Apache/cPanel)** — upload via the file manager
or SFTP into `public_html`. For the 404 page to work, add a file named
`.htaccess` in the web root containing:

```
ErrorDocument 404 /404.html
```

## After deploying, check these

1. `https://summitspringpartners.com/` loads the home page with the
   serif headline and navy background (if it's white with default fonts,
   `css/` or `fonts/` didn't upload).
2. Click through all five nav items; each page loads and the current
   page's nav label shows in the warm accent color.
3. On a phone, the Menu button opens the navigation.
4. "Start a Conversation" opens an email to zane@summitspringpartners.com
   with the subject "Conversation".
5. Visit a nonsense URL like `/xyz` — the styled 404 page should appear.
6. The browser tab shows the peak favicon.
7. Paste the site URL into a LinkedIn post draft or a text message —
   the navy share card with the logo and name should appear as preview.
   (LinkedIn caches previews; use https://www.linkedin.com/post-inspector/
   to refresh it after changes.)

## HTTPS and the domain

Serve over HTTPS (every host above provides free certificates —
usually one click or automatic). Pick one canonical form of the domain,
`summitspringpartners.com` without `www`, and have the host redirect
`www.summitspringpartners.com` to it; every host above has a setting
for this. The sitemap and Open Graph URLs assume the non-www form.

## Making content changes later

The five page files are plain HTML — edit text directly in them; the
copy source of record lives in `copy/website-copy.md`, so update that
too when wording changes. Sitewide colors, spacing, and the mobile
layout live in `css/site.css`. After any edit, update the `<lastmod>`
dates in `sitemap.xml`, commit to git, and re-upload the changed files.
