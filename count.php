<?php
// Tally counter. Records page path + visitor-type label + timestamp only.
// NO IP, NO user agent, NO referrer, nothing identifying is ever stored.
//
// CLASSIFY AT ARRIVAL, STORE THE LABEL ONLY (2026-08-04, ruled by Zane).
// The address and the user agent are read in memory to decide one of four
// labels and are then discarded with the request. They are never written,
// never logged, never held. The privacy design is unchanged in substance:
// what leaves this file is a page, a label, and a time.
//
// WHY THIS EXISTS: the 2026-08-02 traffic audit showed the daily count was
// almost entirely a machine, a home-page-only "metronome" firing on a
// 21h35m cycle, and the audit could not name it because the instrument had
// deliberately never collected identity. The 2026-08-03 follow-up found
// Hostinger keeps no access log on the filesystem at all, so the question
// could not be answered from the server either. Classifying at arrival
// answers it without keeping anything: the metronome's next hit carries a
// label, and the label is the finding.
//
// THE FOUR LABELS, in the order they are decided:
//   crawler  a self-declaring bot. These were DROPPED at ingest until
//            today and are now counted, which is the one change that adds
//            rows to the log rather than annotating them.
//   bot      a data-center address. Catches undeclared automation running
//            a real browser engine behind an ordinary browser UA, which is
//            exactly what the audit said the old regex could never see.
//   human    a browser user agent from an address that is not data-center.
//   unknown  the honest remainder. Never guessed into another bucket.
//
// PRECEDENCE IS DELIBERATE: a declared crawler running in AWS is recorded
// as crawler, not bot, because a self-declaration is stronger evidence than
// an address range. Stated here so the order is read as a decision.
//
// ZANE'S OWN VISITS CLASSIFY AS HUMAN AND CANNOT BE SEPARATED. This is the
// privacy design choosing its own tradeoff, not an oversight: with no IP
// and no identifier stored, a visit from his laptop is byte identical to a
// visit from a stranger. Self-exclusion would require storing or tokenizing
// something about the visitor, which this instrument refuses. Named in the
// ledger row so the number is read with it in mind.
//
// FILE SHAPE: every function is declared first, then the CLI return below,
// then the ingest. The order exists so the acceptance test can load this
// file and call ssp_classify() directly, with real addresses as transient
// input, instead of spoofing HTTP requests that would write real rows into
// the real log to test a classifier.

// Declared-bot pattern. Same expression that used to exit at ingest; it now
// decides a label instead of discarding the visit.
function ssp_is_declared_crawler($ua) {
    return $ua === '' || preg_match(
        '/bot|crawl|spider|slurp|curl|wget|python|httpclient|headless|preview|scan|fetch/i',
        $ua);
}

// One address against one CIDR, IPv4 and IPv6, by packed-byte comparison.
// inet_pton gives 4 bytes for v4 and 16 for v6, so a length mismatch means
// the families differ and the answer is no.
function ssp_in_cidr($ip, $cidr) {
    $slash = strpos($cidr, '/');
    if ($slash === false) return false;
    $subnet = substr($cidr, 0, $slash);
    $bits   = (int) substr($cidr, $slash + 1);
    $ipb = @inet_pton($ip);
    $sb  = @inet_pton($subnet);
    if ($ipb === false || $sb === false || strlen($ipb) !== strlen($sb)) return false;
    if ($bits < 0 || $bits > strlen($sb) * 8) return false;
    $whole = intdiv($bits, 8);
    $rem   = $bits % 8;
    if ($whole > 0 && strncmp($ipb, $sb, $whole) !== 0) return false;
    if ($rem > 0) {
        $mask = chr((0xff << (8 - $rem)) & 0xff);
        if (((ord($ipb[$whole]) ^ ord($sb[$whole])) & ord($mask)) !== 0) return false;
    }
    return true;
}

function ssp_is_datacenter($ip) {
    if ($ip === '') return false;
    static $cidrs = null;
    if ($cidrs === null) {
        $path = __DIR__ . '/cidrs.php';
        $cidrs = is_readable($path) ? (array) require $path : [];
    }
    foreach ($cidrs as $cidr) {
        if (ssp_in_cidr($ip, $cidr)) return true;
    }
    return false;
}

// Browser-shaped user agent. Deliberately broad: this runs only after the
// declared-crawler and data-center tests have both said no, so its job is
// to separate a real browser from something odd, not to catch bots.
function ssp_is_browser_ua($ua) {
    return (bool) preg_match('/Mozilla|AppleWebKit|Gecko|Safari|Chrome|Firefox|Edg|OPR|Version/i', $ua);
}

function ssp_classify($ua, $ip) {
    if (ssp_is_declared_crawler($ua)) return 'crawler';
    if (ssp_is_datacenter($ip))       return 'bot';
    if (ssp_is_browser_ua($ua))       return 'human';
    return 'unknown';
}

// Loaded from the command line, this file is a library and stops here: it
// sends no headers, reads no request, and writes no row. Only a real web
// request runs the ingest below. This is what makes the classifier testable
// without a test ever touching the live log.
if (PHP_SAPI === 'cli') return;

// ---- ingest ----------------------------------------------------------

http_response_code(204);
header('Cache-Control: no-store');

$pages = ['/', '/about.html', '/approach.html', '/coaching.html', '/ai-partner.html', '/404.html'];
$p  = $_GET['p'] ?? '';
$ua = $_SERVER['HTTP_USER_AGENT'] ?? '';
$ip = $_SERVER['REMOTE_ADDR'] ?? '';

// Bad-path drop, UNCHANGED and still first. Scanners probing for
// /wp-login.php or /.env produce nothing at all, not even an unknown row.
// This is the strongest filter in the file and it stays exactly as it was.
if (!in_array($p, $pages, true)) exit;

$label = ssp_classify($ua, $ip);
unset($ua, $ip);   // explicit, so the discard is visible and not merely implied

@file_put_contents('/home/u619638832/ssp-stats/hits.log',
  gmdate('Y-m-d\TH:i:s\Z') . ',' . $p . ',' . $label . "\n",
  FILE_APPEND | LOCK_EX);
