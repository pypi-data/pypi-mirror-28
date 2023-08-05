[![Waffle.io - Columns and their card count](https://badge.waffle.io/setminami/Jsonica.png?columns=all)](https://waffle.io/setminami/Jsonica?utm_source=badge)

# Jsonica
[ja](./README_ja.md)

# What's this?

# Setup'n Usage
[Usage Sample](./Usage_Samples.md)

# What I wanna do and Where advantage
  - I only want to be interested in huge data and want to manage them easily.
    - I wanna eliminate the noise that I want to do and concentrate on meeting the necessary conditions.
  - I wanna automatically generate concrete representation like JSON, Yaml, md ...etc, from abstract representation such as Excel (I call them 'META descriptor' in the docs.).
    - I'd like to compute data inversely from a tool that gives artificial bias to the data or makes it easy to create data suitable for artificial hypotheses.
      - Excel itself gets huge data summary, it is suitable for statistical data creation.
    - By hold an abstract representation, you only need a limited representation to build last ideal one, and no other output is needed until you need it.
    - By describing the object of interest abstractly, the ∀representation including the unrecognized item can focus on shaping with limited convenience in each lower and something more concrete layer.
  - Distribution and collection as a small grain file to a large number of people to concentrate work and parallelize.
    - For example, it is ideal to output sheets with huge JSON files when you initialize each sheet by distributing them from the excel and finalize them when collecting.
    - For detailed specifications, only a part of team member(s) who know well about it may hold, and accurately describe, each one wishes to manage distributed knowledge that only needs to know the part in each charge.

see also. [Appendix. mindmap](./Appendixies.md)

# building Excel file and edit
  - To manage it as 1 sheet → a layer
  - A sheet indicating the root item must have `root` as the sheet name
    - When there is `-r sheetname`, `sheetname` is recognized as root sheet, but no `-r`, xlsx must have a sheet named `root`.
  - Column should be interpreted as key.
    - In each column, describe jsonschema for the corresponding item **column's comment**.
    - For communication, comment lines other than jsonschema are given by adding `#` at the beginning of each comment line, and this line shall not be interpreted when JSON is generated.
    - With the xlsx initialization command, the setting contents of jsonschema are read from yaml, and a template file with jsonschema descriptions as embedded comment is generated.
  - If you want to have an item one level below, make it a separate sheet and put a hyperlink to sheet in the item name column
    - In the case of found `'type': 'array'` in schema description, all items in linked sheet treated as an array are added to the parent, and in case of `'type':'object'` sheet which have rows, **the last row** is added as object.
    - If you donot want to make an array as one level lower item, specify `" type ":" object "` in the schema which corresponding to the column.
  - Each child-item sheets were pointed from a parent item sheet, in a cell with str `sheet://sheet_name`
    - It is unlikely that you choose a menu or use shortcut from Excel and put a hyperlink to another seat
    - Because hyperlinks description may be different depending on the procedure of filling in Excel, OS and environment, link is to be written manually with a META manner.
    - Allow whitespace on encode so that `sheet://` and later will be the sheet name as it is
    - If typo is found, immediately raise it as a command error. see. Appendix. Errors
  - Since it is not affected by the specification of Excel, do not overwrite unnecessary macros as much as possible

# Sample Files
  - META descriptor and `jsonica.py gen -of csv -hr 2` output sample
    - [xlsx & genarated json](https://github.com/setminami/Jsonica/tree/master/Samples)
  - Search for xlsx git management style, that neednot adjust configuration on each local git environment of non Tech members.
    - [xlsx git management (trial)](https://github.com/setminami/Jsonica/tree/master/output/cheatsheet.xlsx)
  - Yaml file, for initial xlsx template.
    - [template.yaml](https://github.com/setminami/Jsonica/blob/master/template.yaml)
  - jsonschema based on xlsx directly and seamless. (TBD)

## [Appendix.](./Appendixies.md)
