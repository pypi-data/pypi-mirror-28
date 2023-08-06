# How to Install
```
pip install jsonica
```

# Usage Sample
```
# generate
$ jsonica.py gen -i ./Samples/cheatsheet.xlsx -o ./output -of tsv:./output
Analyzing... /Users/set/Desktop/Github/JSON_XLSX_Manager/Samples/cheatsheet.xlsx
Output json Success ➡️ ./output/cheatsheet.json

$ jsonica.py gen -i ./Samples/cheatsheet.xlsx -o ./output/test.json -of tsv:./output
Analyzing... /Users/set/Desktop/Github/JSON_XLSX_Manager/Samples/cheatsheet.xlsx
Output json Success ➡️ ./output/test.json

$ jsonica.py g -o - -of tsv:./output
[{"color": "fff000", "title": "Anchors", "items": [{"sign": "^", "desc-en": "Matches at the start of string or start of line if multi-line mode is enabled. Many regex implementations have multi-line mode enabled by default."}, {"sign": "$", "desc-en": "Matches at the end of string or end of line if multi-line mode is  enabled. Many regex implementations have multi-line mode enabl....

$ jsonica.py g -i ./Samples/cheatsheet.xlsx -hr 2 -o - -of tsv:./output
[
  {
    "color": "fff000",
    "items": [
....

# check silent outputs
$ ls ./output
cheatsheet.json	cheatsheet.xlsx	test.json

$ ls ./output/cheatsheet.xlsx/
items-Anchors.tsv		items-Modifiers.tsv		items-bracketEx.tsv
items-Case Modifiers.tsv	items-POSIX-CHAR.tsv		items-spchar.tsv
items-CharClass.tsv		items-Quantifiers.tsv		root.tsv
items-Groups.tsv		items-assertion.tsv

# ☝️ can see on github.io like...
# https://github.com/setminami/Jsonica/tree/master/output/cheatsheet.xlsx
```
