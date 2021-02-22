#!/usr/bin/env python3
# python script used to generate example date from the original awesome remarkable list
import re
import os

import json

def safe_filename(filename: str) -> str:
    return "".join(c for c in filename if c.isalnum() or c in ('_','-')).rstrip()

infile, outfolder = 'README.old.md', '_items'

regex_category_text = '## (.*)\n'
category_parser = re.compile(regex_category_text)

regex_item_text = '- \[(?P<name>.*)\]\((?P<url>.*)\) - (?P<description>.*)\n'
item_parser = re.compile(regex_item_text)

category = ''
list_items = []
with open(infile, 'r') as f:
    for line in f:
        m = category_parser.match(line) 
        if m:
            category = m.group(1)
        else:
            m = item_parser.match(line)
            if m:
                item = {**{'category': category}, ** m.groupdict()}
                list_items.append(item)


#with open(os.path.join('_data', 'items.json'), 'w') as outfile:
#    json.dump(list_items, outfile, indent=4)



from string import Template
template = Template("""---
layout: item
category: $category
name: $name
description: $description
website: $url
tags: []
---

$content
""")
if not os.path.exists('_items'):
    os.makedirs('_items')
for item in list_items:
    #print(item)
    filename = os.path.join(outfolder, safe_filename(item['name']) + '.md')
    if os.path.exists(filename):
        print("{} already exists".format(filename))
    with open(filename, 'w') as f:
        f.write(template.substitute({**item, 'content': item['description']}))
    