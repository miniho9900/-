#!/usr/bin/env python3
"""site/i18n/en_content.py 의 영문 내용을 site/live/*.json 콘텐츠에 *_en 필드로 합칩니다."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "site" / "i18n"))
from en_content import EN, STAT_LABEL_EN

live = ROOT / "site" / "live"
b5 = json.loads((live / "business" / "b5.json").read_text(encoding="utf-8"))
ko = b5["content"]
# price list rows: translate item names / spec text, keep model numbers and prices
rows = [l for l in ko.split("\n") if re.match(r"^\| \d+ \|", l) and len(l.strip("|").split("|")) >= 6]
item = [("보안 L2 PoE 스위치","Secure L2 PoE switch"),("보안 L2 스위치","Secure L2 switch"),("보안 L3 스위치","Secure L3 switch"),("L2 PoE 스위치","L2 PoE switch"),("L2 스위치","L2 switch"),("L3 스위치","L3 switch"),("백본 스위치","Backbone switch"),("(제어부)"," Control Unit —"),("광모듈(SFP)","Optical module (SFP)"),("변환모듈(TX-Copper)","Converter module (TX-Copper)")]
spec = [("네트워크스위치","Network switch"),("유비쿼스","ubiQuoss"),("(부품)","(Part) "),("최대 ","up to "),("Fan-Less 무소음","fanless, silent"),("10G 멀티","10G multi-mode"),("10G 싱글","10G single-mode"),("1G 멀티","1G multi-mode"),("1G 싱글","1G single-mode")]
out = []
for r in rows:
    c = [x.strip() for x in r.strip("|").split("|")]
    for a,b in item: c[1] = c[1].replace(a,b)
    for a,b in spec: c[4] = c[4].replace(a,b)
    c[1] = re.sub(r"\s+"," ",c[1]).replace("— Main Control Unit","").strip()
    out.append("| " + " | ".join(c) + " |")
price = "| No | Item (classification 43222612) | Item ID | Model | KONEPS listing | Registered price (VAT incl.) |\n" + "\n".join(out)
EN["business/b5"]["content_en"] = """## PRODUCTS | Registered procurement products
| No | Item | Details |
| 1 | Enhanced security (security conformity certified) | Security function certificates for all backbone/L3 and security switches / Encryption and hash algorithms against hacking on all models / Enhanced filtering (blocks MAC·IP·ARP attacks) |
| 2 | Reliability | Over 1 million units in operation nationwide for public, enterprise and carrier broadband services / Electrical safety certification for all PoE models |
| 3 | Easy deployment & operation | Standard hardware interfaces / Familiar command set / Convenient NMS (optional) |
| 4 | Leading Korean technology | Numerous patents and utility models / Fanless silent switches, remote hardware reset (patented) |
| 5 | Full L2·L3·multicast support | VRRP·Static·RIP·OSPF·BGP·IS-IS·IGMP·PIM and more |
| 6 | IPv4·IPv6 dual stack | Simultaneous IPv4·IPv6 communication |
| 7 | Easy operation & monitoring | SNMP·RMON·sFlow·port mirroring and other management features |
| 8 | Structured technical support | Manufacturer call center (+82-1577-9550) and online technical library |

## LINE-UP | Differentiated IP-based services
The right network solution for every requirement and scale!
### L3 switches
### L2 switches
### L2 PoE switches
### Security switches
### Backbone switches
### Optical & converter modules

## FEATURED | Products with security function certificates
### E7148
- Item ID 25393875
- Switching fabric 3.6 Tbps · Throughput 1.5 Bpps (128 bytes)
- Service 1G/10G/25GE 48 ports (SFP/SFP+/SFP28)
- Uplink 40G/100GE 6 ports (QSFP+/QSFP28) · redundant power
### E6100
- Item ID 22755362
- Switching fabric 1,280 Gbps · Throughput 714 Mpps
- Service 1G/10G 48 ports (SFP/SFP+)
### E4050-24CX
- Item ID 25043206
- Switching fabric 168 Gbps · Throughput 95.2 Mpps
- Service 1G 24 ports (combo) · Uplink 1G/10G 4 ports (SFP/SFP+)
- Redundant power
### E4050-24S
- Item ID 25691652
- Switching fabric 56 Gbps · Throughput 41.6 Mpps
- Service 1G 24 ports (SFP) · Uplink 1G 4 ports (combo)
- Redundant power
### E4050-24C
- Item ID 25691651
- Switching fabric 56 Gbps · Throughput 41.6 Mpps
- Service 1G 16 ports (UTP) + 1G 8 ports (combo) · Uplink 1G 4 ports (combo)
- Redundant power
### E4050-24T
- Item ID 25691650
- Switching fabric 56 Gbps · Throughput 41.6 Mpps
- Service 1G 24 ports (UTP) · Uplink 1G 4 ports (combo)
- Redundant power

## PRICE LIST | Registered procurement products
Registered supplier: TrizN Inc.
""" + price + """

## WHY ubiQuoss | Why ubiQuoss
### Technology
- Korea's first stable commercial L3 and backbone switches, and mobile (4G/5G) backhaul switches
### Fanless design
- Silent switches (E4020-24T / E4020-24TX)
### Proven stability and market share
- No. 2 in Korean network switch sales (after Cisco), about 1 million units in operation
### Security conformity on all L3 models
- Product stability through advanced security features
### Product range
- The only Korean vendor with an end-to-end total solution
### Electrical safety on all PoE models
- Safety certified under the Electrical Appliances and Consumer Products Safety Control Act
### Korean manufacturer
- Made in Korea (domestic network equipment manufacturer)
### L2–L3 remote reset (patented)
- Efficient networks through patented technology and network automation
### Financial stability
- KOSDAQ-listed (2009) with a sound financial structure
### No. 1 Korean switch vendor
- About 1 million units in operation — a proven solution

## CONTACT | Manufacturer · registered supplier
### Manufacturer — ubiQuoss Inc.
- HQ / R&D: 68 Pangyo-ro 255beon-gil, Bundang-gu, Seongnam-si, Gyeonggi-do
- Customer & technical support: +82-1577-9550
### Registered supplier — TrizN Inc.
- Address: Room 201, Terrace Hill 2, 36 Daehak 3-ro 4beon-gil, Yeongtong-gu, Suwon-si, Gyeonggi-do
- Main line / fax: +82-31-247-5966 / +82-31-212-5903
- Product inquiries: +82-70-5038-1771"""

writes = []
for path, extra in EN.items():
    f = live / (path + ".json")
    if not f.exists(): print("skip (no doc)", path); continue
    d = json.loads(f.read_text(encoding="utf-8"))
    d.update(extra)
    if path == "site/config" and isinstance(d.get("stats"), list):
        d["stats"] = [{**s, "label_en": s.get("label_en") or STAT_LABEL_EN.get(s.get("label",""), "")} for s in d["stats"]]
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    writes.append({"path": path, "fields": list(extra.keys()) + (["stats"] if path=="site/config" else [])})
(ROOT / "site" / "i18n" / "merged.json").write_text(json.dumps(writes, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(writes), "documents updated with English fields")
