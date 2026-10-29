# Deploying summitspringpartners.com

This is a static site of one page, index.html, in seven bands, with one
PHP counter, count.php, and the address range list it reads, cidrs.php.
No build step, no dependencies, nothing to install. Deploying means
copying files to a web host.

## How it deploys

Run `scripts/deploy.sh` from main. It rsyncs the repo root to Hostinger's
`public_html` over SSH with `--delete`, so the server mirrors the tree
exactly. It always shows a dry run first and publishes only on a typed
`yes`. Lines starting with `*deleting` will be removed from the server.

## What is published

```
index.html
404.html
.htaccess
count.php
cidrs.php
favicon.ico
robots.txt
sitemap.xml
assets/          (all files except assets/hero/hero-a-peaks-bw.jpg)
css/             (all files)
fonts/           (all files)
js/              (all files)
```

deploy.sh excludes everything else: `copy/`, `scripts/`, `shots/`,
`decisions/`, `.git/`, `.claude/`, `.gitignore`, `DEPLOY.md`, `AGENTS.md`,
`CLAUDE.md`, `website-lap2-report-2026-10-27.md`, any README and any
`.DS_Store`. They are source material, not the site. The full size hero
original, `assets/hero/hero-a-peaks-bw.jpg`, stays off the server too;
the page uses the hero-a 800, 1600 and 2400 sets.

Everything lands in the web root, `public_html`, so that `index.html`
sits at the top level and the home page is reachable at
`https://summitspringpartners.com/`.

## .htaccess

The web root's `.htaccess` sets the 404 page and sends every address of
the old five page site to its band on the one page, with and without
`.html`:

```
/resources.html            301  /#ai-partner
/approach, /approach.html  301  /#consulting
/ai-partner(.html)         301  /#ai-partner
/coaching(.html)           301  /#coaching
/about(.html)              301  /#about
/contact(.html)            301  /#contact
```

## After deploying, check these

1. Purge the Hostinger CDN cache in hPanel. The CDN fronts the site
   (`server: hcdn`), and until the purge it can keep serving the old
   pages and the old home with a 200.
2. Run `scripts/copy_pass_proof.py` without `--no-live`. Its cell 9
   fetches the live one page and requires it to be byte identical to
   the tree; it closes `cells passed 9, failed 0, of 9`.
3. Check the eleven old addresses above with `curl -sI`. Each answers
   301 with a Location at its band's fragment. Read them once with a
   cache busting query such as `?cb=1` and once on the plain URL after
   the purge. Apache appends a request's query to the redirect target,
   so a cache busted read answers `/#ai-partner?cb=1`; strip the query
   from the Location before comparing it.
4. `https://summitspringpartners.com/` loads the one page with the serif
   headline and navy background (if it's white with default fonts,
   `css/` or `fonts/` didn't upload). The nav and footer anchors land
   on their bands, and each band's "More on this" opens in place.
5. On a phone, the page has no sideways scroll.
6. "Start a Conversation" opens an email to zane@summitspringpartners.com
   with the subject "Conversation".
7. Visit a nonsense URL like `/xyz`: the styled 404 page should appear.
8. The browser tab shows the peak favicon.
9. Paste the site URL into a LinkedIn post draft or a text message: the
   navy share card with the logo and name should appear as preview.
   (LinkedIn caches previews; use https://www.linkedin.com/post-inspector/
   to refresh it after changes.)

## HTTPS and the domain

Serve over HTTPS. Pick one canonical form of the domain,
`summitspringpartners.com` without `www`, and have the host redirect
`www.summitspringpartners.com` to it. The sitemap and Open Graph URLs
assume the non-www form.

## Making content changes later

The page is plain HTML; edit text directly in index.html. The copy
source of record lives in `copy/website-copy.md`, and any copy change
reopens its band there as a draft for approval first. Sitewide colors,
spacing, and the mobile layout live in `css/site.css`. After any edit,
update the `<lastmod>` date in `sitemap.xml`, run
`scripts/copy_pass_proof.py --no-live`, commit to git, merge to main and
run `scripts/deploy.sh`.
