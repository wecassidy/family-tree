#!/usr/bin/python3

# treecsv2json.py convert a family tree CSV file from
# http://mcdemarco.net/tools/family-tree-generator/lineage.html to a
# JSON file, stripping out some of the less-useful data.

# Original data: id, name, gender, generation, byear, dyear, dage,
# myear, mage, ptype, clan, spouseId, parentId1, parentId2, parentNodeId

# JSON format: each node has a string name, an int generation, and a
# list of children, consisting of more nodes. A leaf of the tree will
# have an empty child list. For simplicity, it is safe to assume that
# names will be unique within the tree.

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
