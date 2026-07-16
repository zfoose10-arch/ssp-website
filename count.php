<?php
// Tally counter. Records page path + timestamp only — no IP, UA, referrer, or identifiers.
http_response_code(204);
header('Cache-Control: no-store');

$pages = ['/', '/about.html', '/approach.html', '/coaching.html', '/ai-partner.html', '/404.html'];
$p  = $_GET['p'] ?? '';
$ua = $_SERVER['HTTP_USER_AGENT'] ?? '';

if (!in_array($p, $pages, true)) exit;
// Drop obvious bots at ingest; the UA string itself is never stored.
if ($ua === '' || preg_match('/bot|crawl|spider|slurp|curl|wget|python|httpclient|headless|preview|scan|fetch/i', $ua)) exit;

@file_put_contents('/home/u619638832/ssp-stats/hits.log',
  gmdate('Y-m-d\TH:i:s\Z') . ',' . $p . "\n",
  FILE_APPEND | LOCK_EX);
