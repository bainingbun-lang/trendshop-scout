import argparse
import csv
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

GOOGLE_RSS = "https://trends.google.com/trending/rss?geo={geo}"
NS = {"ht": "https://trends.google.com/trending/rss"}


def trending_terms(geo):
    with urllib.request.urlopen(GOOGLE_RSS.format(geo=geo), timeout=20) as r:
        root = ET.fromstring(r.read())
    terms = {}
    for item in root.iter("item"):
        title = item.findtext("title", default="").lower()
        traffic = item.findtext("ht:approx_traffic", default="", namespaces=NS)
        terms[title] = traffic
    return terms


def match(name, terms):
    words = [w for w in re.findall(r"\w+", name.lower()) if len(w) > 3]
    for term, traffic in terms.items():
        if any(w in term for w in words):
            return term, traffic
    return None, ""


def load_products(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    p = argparse.ArgumentParser(description="Cruza tus productos con tendencias de Google Trends")
    p.add_argument("csv", help="CSV con columnas: name,cost,price")
    p.add_argument("--geo", default="MX")
    args = p.parse_args()

    terms = trending_terms(args.geo)
    rows = []
    for product in load_products(args.csv):
        cost = float(product["cost"])
        price = float(product["price"])
        term, traffic = match(product["name"], terms)
        rows.append({
            "name": product["name"],
            "margin": round(price - cost, 2),
            "trend": term or "",
            "traffic": traffic,
        })

    rows.sort(key=lambda r: (r["trend"] == "", -r["margin"]))
    for r in rows:
        status = f"tendencia: {r['trend']} ({r['traffic']})" if r["trend"] else "sin tendencia"
        print(f"{r['name']:<30} margen {r['margin']:>8.2f}  {status}")
    print("\nUna coincidencia con tendencia no garantiza ventas. Valida con datos propios antes de invertir.")


if __name__ == "__main__":
    main()
