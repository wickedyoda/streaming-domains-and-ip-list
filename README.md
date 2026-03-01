# Domain and IP Lists for Policy Routing

This repository contains domain and network lists for streaming services,
social platforms, device ecosystems, and other traffic groups that you may
want to route through different VPN exits, WAN paths, or filtering policies.

Use these lists with tools like OpenWrt/GL.iNet policy routing, pfSense
aliases, DNS-based split tunneling, firewall sets, and proxy rules.

## Repository Structure

- `netflix/domains.md`  
  Netflix-focused domains (streaming, apps, APIs, support, corporate).

- `netflix/router-list.txt`  
  Combined Netflix router list (domains + CIDRs) for direct import/use in
  policy routing and alias tools.

- `netflix/ipv4-address.md`  
  Netflix/Open Connect IPv4 ranges.

- `netflix/ipv6-address.md`  
  Netflix/Open Connect IPv6 ranges.

- `netflix/ans.md`  
  Netflix-related ASN references.

- `streaming_services/streaming_domains_whitelist.txt`  
  Mixed streaming provider domains and related IP ranges.

- `social_media/social_media.txt`  
  Social media domain list.

- `porn/known_porn_domains_v2.txt`  
  Large categorized/adult-domain style list for filtering or routing.

- `bypass_sites.txt`  
  General bypass set (social/media/mixed) for alternate route handling.

- `bamboo_printer/bamboo_domains.txt`  
  Bambu Lab and Makerworld related domains for device/cloud connectivity.

## Suggested Usage Pattern

1. Keep one list per routing intent (for example: `vpn-us`, `vpn-uk`,
   `direct`, `blocked`, `dns-only`).
2. Prefer domain-based matching first, then add IP/ASN where needed.
3. Refresh lists periodically and monitor misses in firewall/DNS logs.
4. Test on a non-critical client before rolling rules to your full network.

## Notes on Accuracy

- Domain and CDN infrastructure changes frequently.
- Some services use regional/ISP-local endpoints not always captured in static
  files.
- IP-only matching is useful, but domain-based rules are usually more stable.

## Validation Safeties

This repo includes automated checks for list formatting and data hygiene:

- Valid domain/CIDR/ASN entry types by file
- Duplicate entry detection
- CRLF/trailing-whitespace detection

Run locally:

```bash
make validate
```

CI:

- GitHub Actions runs the same validator on every push and pull request.

## Disclaimer

These lists are curated references, not authoritative vendor feeds. Use at your
own risk and validate against your own traffic patterns.

## License

MIT
