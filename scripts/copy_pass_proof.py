#!/usr/bin/env python3
"""copy_pass_proof: the diagnose first copy pass of 2026-09-07, proven.

Usage: copy_pass_proof.py [--no-live]

Nine cells against the website repo this file sits in. Cell 1 renders
the text nodes of the six pages at the pass's base commit and in the
working tree and requires the difference to be exactly the nine locked
changes, eight replaced and one added, on Home, Approach, and AI
Partner, with Coaching, About, and 404 untouched. Cells 2 to 8 hold the
sitewide rules from copy/website-copy.md's Global build rules and the
sitemap stamp. Cell 9 fetches the six live pages and requires each to
be byte identical to the tree; it is red before a deploy by design and
--no-live skips it for the pre deploy run.

Closing line: cells passed N, failed M, of T. One line is appended to
~/scripts/_state/proof_runs.log per run. Exit 0 only when nothing
failed. Writing rules apply to every line this script prints.
"""
import html
import os
import re
import subprocess
import sys
import time
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "acf1874"
PAGES = ["index.html", "approach.html", "ai-partner.html", "coaching.html", "about.html", "404.html"]
SITE = "https://summitspringpartners.com/"
LOG = os.path.expanduser("~/scripts/_state/proof_runs.log")

OLD_P1 = "I consult on the leadership system. I build the AI systems myself. I was an engineer before I was a consultant, and the order matters."
NEW_P1 = "I consult on the leadership system. I know AI systems from the inside because I have built them myself. I was an engineer before I was a consultant, and the order matters."
NEW_HOME_ADDED = "The AI side opens with a short diagnostic that stands on its own and can end there."
OLD_EYEBROW_A = "When the system in question is the one being built around AI."
NEW_EYEBROW_A = "When the system in question is the one AI is about to inherit."
OLD_A3 = "The build that follows keeps one line: the system takes the leg work, your people keep the judgment calls, and the hours that come back are counted."
NEW_A3 = "Whatever gets switched on keeps one line: the system takes the leg work, your people keep the judgment calls, and the hours that come back are counted."
OLD_ECHO = "This is one of two expressions of the same practice. The other is the consulting itself, and every build runs on its spine."
NEW_ECHO = "This is one of two expressions of the same practice. The other is the consulting itself, and every engagement here runs on its spine."
OLD_EYEBROW_B = "What you are actually building."
NEW_EYEBROW_B = "What the work leaves behind."
OLD_B2 = "The work builds that capture into how the company operates. A workflow is installed, an internal champion is trained to run it, and every correction they make feeds back so the system gets more like your business and less like a generic tool. Month over month, the evidence is visible: corrections captured, edit rates falling, cycle times shrinking."
NEW_B2 = "The work decides which AI to switch on and which to leave off, names who owns each approval, and puts that capture into how the company already operates, on the platform you have. An internal champion is trained to run it, and every correction they make feeds back, so the system gets more like your business and less like a generic tool. Month over month, the evidence is visible: corrections captured, edit rates falling, cycle times shrinking."
OLD_B3 = "The ongoing work is governance and judgment. What the system is permitted to decide, where a human stays in the loop, how it is audited, and what happens when the model providers ship a feature that replaces something you built. When that happens, you migrate onto it and redeploy the effort to the next thing. That is the job."
NEW_B3 = "The ongoing work is governance and judgment. What the system is permitted to decide, where a human stays in the loop, how it is audited, and what happens when the model providers ship a feature that replaces something you switched on. When that happens, you migrate onto it and redeploy the effort to the next thing. That is the job."
OLD_LEV = "The work that is generic is not worth building. The model providers will ship it for free before long, and you should let them."
NEW_LEV = "The work that is generic is not worth a system of its own. The model providers will ship it for free before long, and the right call is to switch theirs on and govern it."

EXPECTED = {
    "index.html": {"replaced": [(OLD_P1, NEW_P1)], "added": [NEW_HOME_ADDED]},
    "approach.html": {"replaced": [(OLD_EYEBROW_A, NEW_EYEBROW_A), (OLD_A3, NEW_A3)], "added": []},
    "ai-partner.html": {"replaced": [(OLD_ECHO, NEW_ECHO), (OLD_EYEBROW_B, NEW_EYEBROW_B), (OLD_B2, NEW_B2), (OLD_B3, NEW_B3), (OLD_LEV, NEW_LEV)], "added": []},
    "coaching.html": {"replaced": [], "added": []},
    "about.html": {"replaced": [], "added": []},
    "404.html": {"replaced": [], "added": []},
}

results = []


def cell(name, ok, detail):
    results.append((name, ok, detail))
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


# Cell 1: text integrity against the base commit.
try:
    problems = []
    total_changes = 0
    for page in PAGES:
        old = text_nodes(at_base(page))
        new = text_nodes(read(page))
        exp = EXPECTED[page]
        # Apply the expected changes to the old list and require equality.
        want = list(old)
        for o, n in exp["replaced"]:
            if o not in want:
                problems.append(f"{page}: base lacks the node to replace: {o[:60]}")
                continue
            want[want.index(o)] = n
        for a in exp["added"]:
            if a not in new:
                problems.append(f"{page}: added node absent: {a[:60]}")
        # Remove the added nodes from the new list before comparing.
        new_less = list(new)
        for a in exp["added"]:
            if a in new_less:
                new_less.remove(a)
        if want != new_less:
            extra = [n for n in new_less if n not in want]
            missing = [w for w in want if w not in new_less]
            problems.append(f"{page}: unexpected text drift, extra {extra[:2]}, missing {missing[:2]}")
        total_changes += len(exp["replaced"]) + len(exp["added"])
    # The added Home node must sit right after the leg work paragraph.
    home_new = text_nodes(read("index.html"))
    i = home_new.index("The AI takes the leg work. Your people keep the judgment calls. The hours that come back are counted.")
    if home_new[i + 1] != NEW_HOME_ADDED:
        problems.append("index.html: the added sentence is not directly after the leg work paragraph")
    cell("text integrity against " + BASE, not problems and total_changes == 9,
         f"{total_changes} expected changes, {len(problems)} problem(s)" + (": " + "; ".join(problems) if problems else ""))
except Exception as exc:
    cell("text integrity against " + BASE, False, f"could not run: {exc}")

# Cell 2: metadata unchanged on every page.
bad = []
for page in PAGES:
    if head_fields(at_base(page)) != head_fields(read(page)):
        bad.append(page)
cell("metadata unchanged on six pages", not bad, f"pages with a changed head field: {bad or 'none'}")

# Cell 3: copy doc lines found in their pages, Revision 4 named.
doc = read("copy/website-copy.md")
page_of = {"Home": "index.html", "Approach": "approach.html", "AI Operating Partner": "ai-partner.html",
           "Coaching": "coaching.html", "About": "about.html", "404": "404.html"}


def norm(s):
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


missing = []
checked = 0
for sec in re.split(r"^## Page: ", doc, flags=re.M)[1:]:
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
        if not l or l.startswith("#") or l.startswith("**") or l.startswith('*"') or l.startswith("Nav ") or l.startswith("*No CTA"):
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
            ok = f'og:description" content="{v}"' in raw
        if not ok:
            missing.append(f"[{key}] metadata {k}")
rev4 = "Revision 4, 2026-09-07" in doc.split("\n---", 1)[0]
cell("copy doc Revision 4 matches the pages", not missing and rev4,
     f"{checked} lines checked, {len(missing)} missing, Revision 4 named {rev4}" + (": " + "; ".join(missing) if missing else ""))

# Cell 4: og:title mirrors the title tag.
breaks = []
for page in PAGES[:5]:
    h = head_fields(read(page))
    if h["title"] != h["og:title"]:
        breaks.append(page)
cell("og:title mirrors the title on five pages", not breaks, f"mirror breaks: {breaks or 'none'}")

# Cell 5: one CTA per page, none on About, Return home on 404.
counts = {page: read(page).count("Start a Conversation") for page in PAGES}
ok5 = all(counts[p] == 1 for p in PAGES[:4]) and counts["about.html"] == 0 and counts["404.html"] == 0 \
    and "Return home" in read("404.html")
cell("one CTA sitewide as governed", ok5, "counts " + ", ".join(f"{p} {c}" for p, c in counts.items()))

# Cell 6: Bozeman in five Home positions and nowhere else.
home = read("index.html")
boz_home = len(re.findall(r"Bozeman", home))
boz_else = {p: len(re.findall(r"Bozeman", read(p))) for p in PAGES[1:]}
cell("Bozeman in five Home positions only", boz_home == 5 and not any(boz_else.values()),
     f"home {boz_home}, elsewhere {sum(boz_else.values())}")

# Cell 7: sitemap lastmod.
sm = read("sitemap.xml")
want = {"https://summitspringpartners.com/": "2026-09-07", "https://summitspringpartners.com/approach.html": "2026-09-07",
        "https://summitspringpartners.com/ai-partner.html": "2026-09-07", "https://summitspringpartners.com/coaching.html": "2026-07-14",
        "https://summitspringpartners.com/about.html": "2026-07-14"}
got = dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sm))
cell("sitemap lastmod stamped on three pages", got == want, f"{len([k for k in want if got.get(k) == want[k]])} of 5 as expected")

# Cell 8: no em dash in the three pages, and none added to the copy doc.
# The copy doc's section headers carry em dashes from its first issue
# (Page: Home LOCKED and the Approach stage headers); this pass adds none.
dashes = {p: read(p).count("—") for p in ["index.html", "approach.html", "ai-partner.html"]}
doc_now = read("copy/website-copy.md").count("—")
doc_base = at_base("copy/website-copy.md").count("—")
cell("no em dash in the pages, none added to the copy doc", not any(dashes.values()) and doc_now == doc_base,
     "pages " + ", ".join(f"{p} {c}" for p, c in dashes.items()) + f"; copy doc {doc_now} now, {doc_base} at base")

# Cell 9: live pages byte identical to the tree.
if "--no-live" in sys.argv:
    print("cell 9 live pages: skipped by --no-live")
else:
    diffs = []
    for page in PAGES:
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
    cell("six live pages byte identical to the tree", not diffs, "; ".join(diffs) if diffs else "six of six identical")

passed = sum(1 for _, ok, _ in results if ok)
failed = len(results) - passed
closing = f"cells passed {passed}, failed {failed}, of {len(results)}"
print(closing)
try:
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} copy_pass_proof.py {closing}\n")
except Exception as exc:
    print(f"proof log not written: {exc}")
sys.exit(0 if failed == 0 else 1)
