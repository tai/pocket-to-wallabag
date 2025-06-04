#!/usr/bin/env python3

import os
import sys
import csv
import json
import datetime 

def usage():
  print('p2w2 - Convert Pocket CSV to Wallabag V2 JSON', file=sys.stderr)
  print('Usage: python3 p2w2.py pocket.csv', file=sys.stderr)
  sys.exit(0)

def epoch2time(et):
  dt = datetime.datetime.fromtimestamp(et)
  return dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')

def pocket2walla(title, url, time_added, tags, status):
  entry = {
    'created_at': epoch2time(int(time_added)),
    'is_archived': 1,
    'is_starred': 0,
    'tags': tags.split('|') if tags else [],
    'title': title,
    'url': url
  } 
  return entry

def main():
  entries = []
  with open(sys.argv[1], newline='') as infile:
    reader = csv.reader(infile, delimiter=",", quotechar='"')
    next(reader)
    for line in reader:
      entry = pocket2walla(*line)
      entries.append(entry)

  # Dump JSON in WallaBagV2 format
  with open("out.json", "w") as outfile:
    json.dump(entries, outfile, indent=2, ensure_ascii=False)

  # Split JSON into chunks to avoid import from timing out
  n = 100
  os.makedirs('out', exist_ok=True)
  for i in range(0, len(entries), n):
    chunk = entries[i:i+n]
    with open(f"out/{i:08d}.json", "w") as outfile:
      json.dump(chunk, outfile, indent=2, ensure_ascii=False)

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    usage()
  main()

