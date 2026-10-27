# Website lap two, 2026-10-27

Branch website-one-page, pull request #1. Nothing merged, main untouched, nothing deployed.

## Done

1. **Hero A.** data-hero="a" on the summit band; your five rules in css/site.css, word for word. Hero B is gone: its ten image files, its three CSS rules and both preview pages. The proof script reads index.html alone. The photo source is one line under the 2.1 amendment in copy/ssp-brand-rules.md. Commit 84a0296.
2. **Founder band.** Two columns above 768px. Name and bio sit on the left. The photo sits on the right, 260 to 320px wide, its top level with the name. It takes no height of its own, so it can never run taller than the bio; object-fit crops it if the bio is short (tested). Credentials run full width below. On phones the photo sits above the name at 192 to 200px. Commit d63f123.
3. **Revision 6 copy pass.** 30 passages across consulting, AI, coaching, practice and founder. The copy doc came first: those five bands are reopened as drafts, and the status line is dated and names both methods and your brief. The page follows the doc. **Read copy/revision-6-changes.md to approve.** Every change is there with before, after and the method section behind it. Commit 99bed0f.

## Checks

- Nu validator, index.html and 404.html: no errors, no warnings.
- copy_pass_proof.py --no-live: 8 of 8. Page to doc: 166 nodes, all in the doc. Doc to page: 122 lines, all on the page. The live cell is skipped before a deploy, as designed.
- Computed colors, every element and pseudo element with details open, plus hover states: only 1B2C3E, DEDEDC, BCBCB9, 5E6975, CDC1B3, 908472 and 0E161F.
- Sorter: tap, Left, Right, Enter and drag each moved the cards and the hours added up. Without script it reads as the two columns.
- Details: all three open and close by click and Enter, with and without script. Closed by default, and the text stays in the source.
- Apache redirects: all eleven old paths return 301 to their band. A missing page returns 404 with 404.html.
- Anchor landings: all seven land with the band at the top and the first line below the bar.
- Band beacons: seven fired, one per band, in order. Without script the pixel fires once for /. count.php accepts all eight values.
- Horizontal scroll at 375, 768 and 1440, details open and closed: none.
- Summit framing at 375, 768, 1440, 1728 and 1920 (shots/summit-*.png): the peaks sit under the clouds with margin, the type sits on the dark forest, the river bend shows near the bottom, and the photo fades into the ground before band 2. On phones the river shows.
- Founder band at 375, 768 and 1440 (shots/founder-*.png): no empty block beside the photo.

## Deviations

- **Branch.** I pushed to website-one-page as you asked. The session's own branch, claude/website-one-page-lap2-6kt492, carries the same commits.
- **Summit at 1440.** At a 900px tall window the text plus padding runs 56px past 78vw. The band there shows about 82% of the photo's height rather than 78%. The framing still reads as intended. I kept your rules exact.
- **768px gets the phone layout.** Your summit media query and the founder brief both start the desktop layout at 769px.
- **Photo source in two places.** Rule 2.1 says the source is recorded in the copy doc, so I also wrote it beside band 1 there. That note does not render.
- **Phase 1 lost "(2 to 4 weeks)".** Phase 1 now includes the three team sessions, and the method sets no length. Entry 9 in the changes file.
- **Coaching dropped "meeting weekly".** Plain Sight's default is every two weeks, and that figure is still in brackets. Entry 26.
- **Proof script cell 3** still checks for "Revision 5a". I only repointed the script; it does not yet check for Revision 6.
- **Hero B deletion.** The build lane says nothing is deleted. I followed this prompt, and the files remain in git history.
- **Proof log.** The proof line went to this cloud container's log, with no key, not to your machine's log.

## Left for the home session

- Your read of copy/revision-6-changes.md, then relock the five bands.
- The gate, then the Judge against copy/website-copy.md and the two method files.
- **Before deploy:** scripts/deploy.sh does not exclude shots/ or this report, so a deploy as it stands would publish both. Add excludes or move them first.
- The merge of pull request #1, then the deploy: you run scripts/deploy.sh and type yes. Then run copy_pass_proof.py live.
- The photo sources are already written; nothing more is owed there.
