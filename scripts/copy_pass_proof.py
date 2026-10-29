#!/usr/bin/env python3
"""copy_pass_proof: the one page of Revision 6, read against the copy doc.

Usage: copy_pass_proof.py [--no-live]

Nine cells against the website repo this file sits in, pointed at the
one page, index.html, alone; the hero previews were removed when Zane
chose hero A. Cell 1 requires every text node of the page to sit
verbatim in copy/website-copy.md. Cells 2 to 8 hold the doc's metadata block and the sitewide
rules from its Global build rules, and the sitemap stamp, the deploy date. Cell 9 fetches
the live one page and requires it to be byte identical to the tree; it
is red before a deploy by design and --no-live skips it for the pre
deploy run.

Closing line: cells passed N, failed M, of T. One line is appended to
~/scripts/_state/proof_runs.log per run. Exit 0 only when nothing
failed. Writing rules apply to every line this script prints.
"""
import html
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "1a9e23a"  # the Revision 5 copy commit this pass builds on
PAGES = ["index.html"]
LIVE_PAGES = ["index.html"]
SITE = "https://summitspringpartners.com/"
DEPLOY = "2026-10-29"  # the day Revision 6 went live, stamped in sitemap.xml
LOG = os.path.expanduser("~/scripts/_state/proof_runs.log")

results = []


def cell(name, ok, detail):
    results.append((name, ok, detail))
    if not ok:
        FAILS.append(name)
    print(f"cell {len(results)} {name}: {'PASS' if ok else 'FAIL'}, {detail}")


def read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as f:
        return f.read()


def at_base(path):
    r = subprocess.run(["git", "show", f"{BASE}:{path}"], cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git show {BASE}:{path} failed: {r.stderr.strip()}")
    return r.stdout


def text_nodes(raw):
    body = raw.split("<main", 1)[1] if "<main" in raw else raw
    body = body.split("</main>", 1)[0]
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    nodes = []
    # Leaf elements only: a layout div nests, so matching every div swallows
    # the paragraphs inside it; the eyebrow div is the one div that is text.
    for m in re.finditer(r"<(p|h1|h2|h3|li)\b[^>]*>(.*?)</\1>|<div class=\"ssp-eyebrow\"[^>]*>(.*?)</div>", body, flags=re.S):
        inner = re.sub(r"<[^>]+>", "", m.group(2) if m.group(2) is not None else m.group(3))
        inner = html.unescape(inner).replace(" ", " ")
        inner = re.sub(r"\s+", " ", inner).strip()
        if inner and not re.match(r"^\d\d$", inner):
            nodes.append(inner)
    return nodes


def head_fields(raw):
    out = {}
    for key, pat in [("title", r"<title>(.*?)</title>"),
                     ("description", r'name="description" content="([^"]*)"'),
                     ("og:title", r'property="og:title" content="([^"]*)"'),
                     ("og:description", r'property="og:description" content="([^"]*)"')]:
        m = re.search(pat, raw)
        out[key] = m.group(1) if m else None
    return out


# The Judge session's second sitting, 2026-09-30: the keyed proof line.
UNIT = "copy_pass_proof.py:no-live" if "--no-live" in sys.argv else "copy_pass_proof.py"
PY, KEYER = "/opt/homebrew/bin/python3", os.path.expanduser("~/scripts/proof_key.py")
FAILS = []
try:
    PROOF_BEGIN = subprocess.run([PY, KEYER, "begin", UNIT], capture_output=True, text=True).stdout.strip() or "none@0"
except Exception:
    PROOF_BEGIN = "none@0"

# Cell 1: text integrity against the copy doc.
doc = read("copy/website-copy.md")


def norm(s):
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


doc_flat = norm(doc.replace("**", "").replace("*", ""))
# A counter the doc writes as "<n> hours back" renders with a number in place of <n>.
templates = [re.compile(re.escape(t).replace(re.escape("<n>"), r"\d+") + "$") for t in re.findall(r'"(<n>[^"]*)"', doc)]


def in_doc(node):
    return node in doc_flat or any(t.match(node) for t in templates)


try:
    problems = []
    texts = {page: text_nodes(read(page)) for page in PAGES}
    for node in texts["index.html"]:
        if not in_doc(node):
            problems.append(f"index.html: not in the doc: {node[:60]}")
    cell("text integrity against the copy doc", not problems,
         f"{len(texts['index.html'])} nodes on the page, {len(problems)} problem(s)" + (": " + "; ".join(problems) if problems else ""))
except Exception as exc:
    cell("text integrity against the copy doc", False, f"could not run: {exc}")

# Cell 2: metadata as the doc's one page Metadata block sets it.
meta_block = doc.split("## Page: One page", 1)[1].split("### Metadata", 1)[1].split("\n---", 1)[0]
want_meta = dict(re.findall(r"\*\*(Title|Meta description|OG description):\*\* (.*)", meta_block))
bad = []
for page in PAGES:
    h = head_fields(read(page))
    if (h["title"], html.unescape(h["description"] or ""), html.unescape(h["og:description"] or "")) != \
            (want_meta.get("Title"), want_meta.get("Meta description"), want_meta.get("OG description")):
        bad.append(page)
cell("metadata from the doc on the page", not bad, f"pages with a head field off the doc: {bad or 'none'}")

# Cell 3: copy doc lines found in their pages, Revision 6 named.
page_of = {"One page": "index.html", "404": "404.html"}
missing = []
checked = 0
for sec in re.split(r"^## Page: ", doc, flags=re.M)[1:]:
    sec = sec.split("\n## ", 1)[0]  # a section ends at the next H2, so the retired record is never read
    name = re.sub(r"\s*—.*", "", sec.split("\n")[0]).strip()
    key = next((k for k in page_of if name.startswith(k)), None)
    if not key:
        missing.append(f"no page for section {name}")
        continue
    raw = read(page_of[key])
    text = norm(raw)
    body = sec.split("### Metadata")[0]
    for line in body.split("\n"):
        l = line.strip()
        if not l or l.startswith("#") or l.startswith("**") or l.startswith('*"') or l.startswith("Nav ") \
                or l.startswith("*No CTA") or l.startswith("Full bleed"):
            continue
        l = re.sub(r"^- ", "", l).strip("*")
        l = re.sub(r"\*\*(.*?)\*\*", r"\1", l)
        if len(l) < 12 or "LOCKED" in l:
            continue
        checked += 1
        if norm(l) not in text:
            missing.append(f"[{key}] {l[:70]}")
    meta = sec.split("### Metadata")[1] if "### Metadata" in sec else ""
    for m in re.finditer(r"\*\*(Title|Meta description|OG description):\*\* (.*)", meta):
        k, v = m.group(1), m.group(2).strip()
        checked += 1
        if k == "Title":
            ok = f"<title>{v}</title>" in raw
        elif k == "Meta description":
            ok = f'name="description" content="{v}"' in raw
        else:
            ok = f'og:description" content="{html.escape(v, quote=False)}"' in raw or f'og:description" content="{v}"' in raw
        if not ok:
            missing.append(f"[{key}] metadata {k}")
rev = "Revision 6, 2026-10-27" in doc.split("\n---", 1)[0]
cell("copy doc Revision 6 matches the page", not missing and rev,
     f"{checked} lines checked, {len(missing)} missing, Revision 6 named {rev}" + (": " + "; ".join(missing) if missing else ""))

# Cell 4: og:title mirrors the title tag.
breaks = []
for page in PAGES:
    h = head_fields(read(page))
    if h["title"] != h["og:title"]:
        breaks.append(page)
cell("og:title mirrors the title on the page", not breaks, f"mirror breaks: {breaks or 'none'}")

# Cell 5: one CTA per page, in the last band only; Return home on 404.
counts = {page: read(page).count("Start a Conversation") for page in PAGES}
last_band = {page: read(page).split('id="contact"', 1)[-1].count("Start a Conversation") for page in PAGES}
ok5 = all(counts[p] == 1 and last_band[p] == 1 for p in PAGES) \
    and read("404.html").count("Start a Conversation") == 0 and "Return home" in read("404.html")
cell("one CTA, last band only", ok5, "counts " + ", ".join(f"{p} {c}" for p, c in counts.items()))

# Cell 6: Bozeman in five positions on each page and nowhere in 404.
boz = {p: len(re.findall(r"Bozeman", read(p))) for p in PAGES}
boz_404 = len(re.findall(r"Bozeman", read("404.html")))
cell("Bozeman in five positions per page only", all(c == 5 for c in boz.values()) and boz_404 == 0,
     ", ".join(f"{p} {c}" for p, c in boz.items()) + f", 404 {boz_404}")

# Cell 7: sitemap lists the one page, stamped the deploy date.
sm = read("sitemap.xml")
want = {SITE: DEPLOY}
got = dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sm))
cell("sitemap lists the one page", got == want, f"{len(got)} url(s), one page stamped {got.get(SITE)}")

# Cell 8: no em dash in the pages, and none added to the copy doc.
# The copy doc's 404 section header carries one em dash from its first
# issue; this pass adds none.
dashes = {p: read(p).count("—") for p in PAGES}
doc_now = read("copy/website-copy.md").count("—")
doc_base = at_base("copy/website-copy.md").count("—")
cell("no em dash in the pages, none added to the copy doc", not any(dashes.values()) and doc_now == doc_base,
     "pages " + ", ".join(f"{p} {c}" for p, c in dashes.items()) + f"; copy doc {doc_now} now, {doc_base} at base")

# Cell 9: the live one page byte identical to the tree.
if "--no-live" in sys.argv:
    print("cell 9 live page: skipped by --no-live")
else:
    diffs = []
    for page in LIVE_PAGES:
        try:
            with urllib.request.urlopen(SITE + page, timeout=20) as r:
                live = r.read()
        except Exception as exc:
            diffs.append(f"{page} fetch failed: {exc}")
            continue
        with open(os.path.join(REPO, page), "rb") as f:
            local = f.read()
        if live != local:
            diffs.append(f"{page} differs, live {len(live)} bytes, tree {len(local)} bytes")
    cell("live one page byte identical to the tree", not diffs, "; ".join(diffs) if diffs else "one of one identical")

passed = sum(1 for _, ok, _ in results if ok)
failed = len(results) - passed
closing = f"cells passed {passed}, failed {failed}, of {len(results)}"
print(closing)
try:
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    try:
        fd, fails_path = tempfile.mkstemp(prefix="proof-fails.")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("".join(n + "\n" for n in FAILS))
        wrote = subprocess.run([PY, KEYER, "write-line", "--unit", UNIT, "--begin", PROOF_BEGIN, "--log", LOG,
                                "--fails-file", fails_path, "--", f"copy_pass_proof.py {closing}"], capture_output=True, text=True).returncode == 0
    except Exception:
        wrote = False
    if not wrote:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} copy_pass_proof.py {closing} [key none unit {UNIT}: the writer could not run]\n")
except Exception as exc:
    print(f"proof log not written: {exc}")
sys.exit(0 if failed == 0 else 1)
