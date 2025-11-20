#!/usr/bin/env python3
"""
Append ?utm_source=atomfeed (or &utm_source=atomfeed) to entry links in Atom feed files
Usage: python scripts/add_utm_to_feeds.py --dir output

This works as a post-build step after Pelican writes the `output/` directory.
"""
import argparse
import glob
import os
import xml.etree.ElementTree as ET

ATOM_NS = '{http://www.w3.org/2005/Atom}'


def fix_href(href, param='utm_source=atomfeed'):
    if not href:
        return href
    # If fragment-only or mailto, skip
    if href.startswith('#') or href.startswith('mailto:'):
        return href
    sep = '&' if '?' in href else '?'
    # Avoid adding multiple times
    if param in href:
        return href
    return href + sep + param


def process_file(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except Exception as e:
        print(f"Skipping {path}: parse error: {e}")
        return 0

    changed = 0
    # For Atom feeds look for <entry> and <link href="..."/>
    for entry in root.findall(f'.//{ATOM_NS}entry'):
        # Prefer the link with rel="alternate" if present
        links = entry.findall(f'{ATOM_NS}link')
        for link in links:
            href = link.get('href')
            if not href:
                continue
            # Only modify links that look like site URLs (http/https) or absolute paths
            if href.startswith('http') or href.startswith('/'):
                new = fix_href(href)
                if new != href:
                    link.set('href', new)
                    changed += 1
        # Optionally update content links inside <content type="html"> but we skip that to avoid breaking embedded HTML

    if changed:
        # Write back preserving XML declaration
        tree.write(path, encoding='utf-8', xml_declaration=True)
    return changed


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dir', '-d', default='output', help='Pelican output directory')
    args = p.parse_args()
    base = args.dir
    patterns = [os.path.join(base, '**', '*.atom.xml'), os.path.join(base, '**', 'all.atom.xml')]
    files = set()
    for pat in patterns:
        files.update(glob.glob(pat, recursive=True))

    total_changed = 0
    for f in sorted(files):
        c = process_file(f)
        if c:
            print(f"Updated {c} links in {f}")
            total_changed += c
    print(f"Done. Total links updated: {total_changed}")


if __name__ == '__main__':
    main()
