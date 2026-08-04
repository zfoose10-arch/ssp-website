<?php
// Data-center address ranges, consulted in memory by count.php to decide
// the "bot" label. Nothing here is ever written to the hits log.
//
// A .php file returning an array, NOT a .txt, on purpose: it deploys with
// the site by the existing rsync rule, and a direct request for
// /cidrs.php returns an empty 200 instead of serving the list as text.
//
// PROVENANCE, STATED HONESTLY BECAUSE IT GOVERNS HOW MUCH TO TRUST IT.
// This list was curated by hand from the providers' published allocations,
// recorded from knowledge at authoring time and NOT fetched from the
// endpoints below at build time. It is therefore a good-faith approximation
// that will age. The authoritative sources, for refreshing it:
//
//   AWS          https://ip-ranges.amazonaws.com/ip-ranges.json
//   Google Cloud https://www.gstatic.com/ipranges/cloud.json
//   Azure        https://www.microsoft.com/en-us/download/details.aspx?id=56519
//   Cloudflare   https://www.cloudflare.com/ips-v4
//   DigitalOcean https://digitalocean.com/geo/google.csv
//   Hetzner      https://bgp.he.net/AS24940
//   OVH          https://bgp.he.net/AS16276
//   Linode       https://geoip.linode.com/
//
// COVERAGE IS DELIBERATELY IMPERFECT AND THAT IS ACCEPTED, per the ruling.
// Large stable aggregates are preferred over exhaustive per-region lists:
// a /8 that a provider holds almost entirely is worth more here than two
// hundred /16s that rot in a month. The cost of that choice is stated
// rather than hidden: a small number of non-data-center addresses inside
// an aggregate would be labeled bot, and any provider or range not listed
// is invisible and its traffic lands in human or unknown instead.
//
// THE FAILURE DIRECTION MATTERS. A miss labels a machine as human, which
// inflates the human column. It never labels a person as a machine unless
// that person is browsing from inside a cloud range, which is rare. When
// in doubt about a range, leaving it out is the safer error.
//
// This file is a dependent of the Site traffic ledger row. Changing it is
// a website surface deploy with its own gate.

return [

    // ---- Amazon Web Services ----
    // 16.12.0.0/15 and 16.144.0.0/12 were ADDED AT THE ACCEPTANCE TEST,
    // 2026-08-04: one of the nine live addresses Zane read out of hPanel,
    // 16.146.3.210, fell outside the initial curation. Recorded here
    // rather than quietly folded in, because it is the single piece of
    // evidence that this list is a curation and not a specification, and
    // the next address from a range nobody thought of will look exactly
    // like this one did.
    '3.0.0.0/8',
    '16.12.0.0/15', '16.144.0.0/12',
    '13.32.0.0/15', '13.34.0.0/15', '13.36.0.0/14',
    '15.156.0.0/14', '15.164.0.0/14', '15.184.0.0/13',
    '18.32.0.0/11', '18.128.0.0/9',
    '34.192.0.0/10',
    '35.71.64.0/22',
    '44.192.0.0/10',
    '46.51.128.0/18', '46.137.0.0/16',
    '50.16.0.0/14', '50.112.0.0/16',
    '52.0.0.0/10', '52.64.0.0/12', '52.84.0.0/14', '52.88.0.0/13',
    '52.192.0.0/11', '52.208.0.0/13',
    '54.64.0.0/11', '54.144.0.0/12', '54.160.0.0/11', '54.192.0.0/12',
    '54.208.0.0/13', '54.224.0.0/11',
    '63.32.0.0/14',
    '75.2.0.0/17', '79.125.0.0/17',
    '99.77.0.0/16', '99.150.0.0/17',
    '107.20.0.0/14', '108.128.0.0/13',
    '174.129.0.0/16', '176.32.0.0/12', '177.71.128.0/17',
    '184.72.0.0/13',
    '204.236.128.0/17', '205.251.192.0/18', '216.182.224.0/19',

    // ---- Google Cloud ----
    '23.236.48.0/20', '23.251.128.0/19',
    '34.64.0.0/10', '34.128.0.0/10',
    '35.184.0.0/13', '35.192.0.0/14', '35.196.0.0/15', '35.198.0.0/16',
    '35.199.0.0/17', '35.200.0.0/13', '35.208.0.0/12', '35.224.0.0/12',
    '35.240.0.0/13',
    '104.154.0.0/15', '104.196.0.0/14',
    '130.211.0.0/16', '146.148.0.0/17',
    '162.222.176.0/21', '199.192.112.0/22', '199.223.232.0/21',

    // ---- Microsoft Azure ----
    '13.64.0.0/11', '13.104.0.0/14',
    '20.0.0.0/8',
    '40.64.0.0/10',
    '51.4.0.0/15', '51.8.0.0/16',
    '52.96.0.0/12', '52.112.0.0/14', '52.125.0.0/16', '52.130.0.0/15',
    '52.132.0.0/14', '52.136.0.0/13', '52.145.0.0/16', '52.146.0.0/15',
    '52.148.0.0/14', '52.152.0.0/13', '52.160.0.0/11', '52.224.0.0/11',
    '65.52.0.0/14',
    '104.40.0.0/13', '104.208.0.0/13',
    '137.116.0.0/15', '138.91.0.0/16',
    '168.61.0.0/16', '168.62.0.0/15',
    '191.232.0.0/13',

    // ---- Cloudflare ----
    '103.21.244.0/22', '103.22.200.0/22', '103.31.4.0/22',
    '104.16.0.0/13', '104.24.0.0/14',
    '108.162.192.0/18',
    '131.0.72.0/22',
    '141.101.64.0/18',
    '162.158.0.0/15',
    '172.64.0.0/13',
    '173.245.48.0/20',
    '188.114.96.0/20', '190.93.240.0/20',
    '197.234.240.0/22', '198.41.128.0/17',

    // ---- DigitalOcean ----
    '45.55.0.0/16', '46.101.0.0/16', '68.183.0.0/16',
    '104.131.0.0/16', '128.199.0.0/16', '134.209.0.0/16',
    '138.68.0.0/16', '139.59.0.0/16',
    '142.93.0.0/16', '143.110.0.0/16', '143.198.0.0/16', '146.190.0.0/16',
    '157.230.0.0/16', '159.65.0.0/16', '159.89.0.0/16',
    '161.35.0.0/16', '164.90.0.0/16', '165.22.0.0/16', '165.227.0.0/16',
    '167.71.0.0/16', '167.99.0.0/16',
    '174.138.0.0/16', '178.62.0.0/16', '188.166.0.0/16',
    '192.241.128.0/17',
    '206.189.0.0/16', '207.154.192.0/18', '209.97.128.0/18',

    // ---- Hetzner ----
    '5.9.0.0/16', '23.88.0.0/17', '46.4.0.0/16',
    '49.12.0.0/16', '49.13.0.0/16',
    '65.108.0.0/16', '65.109.0.0/16',
    '78.46.0.0/15', '88.99.0.0/16', '91.107.0.0/16',
    '94.130.0.0/16', '95.216.0.0/16',
    '116.202.0.0/16', '116.203.0.0/16',
    '128.140.0.0/17', '135.181.0.0/16', '138.201.0.0/16',
    '142.132.0.0/17', '144.76.0.0/16', '148.251.0.0/16',
    '157.90.0.0/16', '159.69.0.0/16', '162.55.0.0/16',
    '167.235.0.0/16', '168.119.0.0/16',
    '176.9.0.0/16', '178.63.0.0/16', '188.40.0.0/16', '195.201.0.0/16',
    '213.133.96.0/19', '213.239.192.0/18',

    // ---- OVH ----
    '51.68.0.0/14', '51.75.0.0/16', '51.77.0.0/16', '51.79.0.0/16',
    '51.81.0.0/16', '51.83.0.0/16', '51.89.0.0/16', '51.91.0.0/16',
    '51.161.0.0/16', '51.178.0.0/16', '51.195.0.0/16', '51.210.0.0/16',
    '51.222.0.0/16',
    '54.36.0.0/16', '54.37.0.0/16', '54.38.0.0/16',
    '91.121.0.0/16',
    '137.74.0.0/16', '141.94.0.0/16', '145.239.0.0/16', '147.135.0.0/16',
    '149.202.0.0/16', '151.80.0.0/16', '158.69.0.0/16',
    '164.132.0.0/16', '167.114.0.0/16',
    '176.31.0.0/16', '178.32.0.0/15', '188.165.0.0/16',
    '192.99.0.0/16', '198.27.64.0/18', '213.186.32.0/19',

    // ---- Linode and Akamai ----
    '45.33.0.0/17', '45.56.64.0/18', '45.79.0.0/16',
    '50.116.0.0/18',
    '66.175.208.0/20', '69.164.192.0/18',
    '96.126.96.0/19',
    '139.162.0.0/16',
    '172.104.0.0/15', '172.105.0.0/16',
    '173.230.128.0/19', '173.255.192.0/18',
    '176.58.96.0/19', '178.79.128.0/18',
    '192.46.208.0/20', '194.195.112.0/20', '198.58.96.0/19',
];
