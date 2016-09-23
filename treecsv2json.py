#!/usr/bin/python3

# treecsv2json.py convert a family tree CSV file from
# http://mcdemarco.net/tools/family-tree-generator/lineage.html to a
# JSON file, stripping out some of the less-useful data.

# Original data: pid, name, gender, generation, byear, dyear, dage,
# myear, mage, ptype, clan, spouseId, parentId1, parentId2, parentNodeId

# JSON format: each node is identified by a unique ID and contains a
# string name, an integer generation, and a list of children,
# consisting of more nodes. A leaf of the tree will have an empty
# child list. IDs are stored as strings because JSON keys can't be
# integers.

# Removed information
# - spouseId: to ensure the data forms a tree (and simplicity), spouses are cut out.
# - byear, dyear, dage: age information is unimportant for a graph of relationships.
# - myear, mage: we cut out the spouses, so why keep other marriage data?
# - ptype: not really sure what this meant, anyway.
# - clan: only useful for Scottish data, and not that useful then.
# - ptype: I honestly have no idea what this is for
# - parentNodeId: the JSON will be structured as a tree, so this is unnecessary.

# Usage
# python3 treecsv2json.py file.csv
# - generates JSON from file.csv and saves it to file.json
# python3 treecsv2json.py file.csv out.json
# - generates JSON from file.csv and saves it to out.json

import csv, json, sys

## Process command line arguments
if len(sys.argv) < 2:
    print("Please specify an input file.")
    sys.exit(2);

csvName = sys.argv[1]

# If a third argument was given, use that as the output
# filename. Otherwise, replace the ".csv" extension of the input with
# ".json".
if len(sys.argv) >= 3:
    jsonName = sys.argv[2]
else:
    csvSections = csvName.split(".")
    csvSections[-1] = "json"
    jsonName = ".".join(csvSections)

## Read and process CSV data
# Read data from the input file, handling any exceptions that might
# come up.
try:
    with open(csvName, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=",")
        rawData = [line for line in reader if line[0][0] != "#"]
except FileNotFoundError:
    print("\"" + csvName + "\" does not exist.")
    sys.exit(1)
except IsADirectoryError:
    print("\"" + csvName + "\" is a directory.")
    sys.exit(21)

# Convert the raw data to a dictionary
keys = ["name", "gender", "generation", "byear", "dyear", \
        "dage", "myear", "mage", "ptype", "clan", "spouseId", \
        "parentId1", "parentId2", "parentNodeId"]
data = {}
for row in rawData:
    data[row[0]] = dict(zip(keys, row[1:]))

# Cut out the information we don't care about
# Remove spouses
spouseless = {}
for pid in data:
    if data[pid]["spouseId"] == "": # Only spouses have spouseIds
        spouseless[pid] = data[pid]
data = spouseless

delKeys = ["gender", "byear", "dyear", "dage", "myear", "mage", \
           "ptype", "clan", "spouseId", "parentNodeId"]
for row in data:
    for key in delKeys:
        del data[row][key]

# Convert generations to integers
for pid in data:
    data[pid]["generation"] = int(data[pid]["generation"])

## Build the JSON data structure
def children(parent, data):
    """Get the children of an ID."""

    kids = []
    for pid in data:
        if data[pid]["parentId1"] == parent or data[pid]["parentId2"] == parent:
            kids.append(pid)

    return kids

def constructTree(root, data):
    tree = {"name": data[root]["name"], "generation": data[root]["generation"], "children": {}}

    kids = children(root, data)
    for child in kids:
        tree["children"][child] = constructTree(child, data)

    return tree

# Find the root of the tree - generation 0
for pid in data:
    if data[pid]["generation"] == 0:
        root = pid

famTree = constructTree(root, data)
