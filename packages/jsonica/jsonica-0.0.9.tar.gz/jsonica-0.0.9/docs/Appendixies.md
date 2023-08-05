## Appendix.1 Errors
sys.exit by each index.

```python
errors = ['OK',
            'sheets link not found.', 'schema not found.', # 1, 2
            'root sheet not found.', 'Unrecognized item type were found.', # 3, 4
            'Unknown accumulator!', 'Output json has failed.', # 5, 6
            'Unsupported table filetype found.', 'setting yaml file not found']
```

## Appendix 2. Help
```
$ jsonica.py -h
usage: jsonica.py [-h] [-v] [-e {python built-in codec}]  ...

generate complex structure JSON with analyzing META descripted file.

positional arguments:
                        sub-commands
    initialize (init, i)
                        create formated workbook template.
    generate (gen, g)   generate analyzed files as TEXT from META descritor
                        file. (e.g., Excel)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -e {python built-in codec}, --encoding {python built-in codec}
                        Set default charactor encode. When not set this, it is
                        treated as "utf-8". see also. https://docs.python.org/3.6/library/codecs.html#standard-encodings

# initialize subcommand help
$ jsonica.py init -h
usage: jsonica.py initialize [-h] [-tx [path/to/outputfile.xlsx]]

optional arguments:
  -h, --help            show this help message and exit
  -tx [path/to/outputfile(.xlsx)], --template_xlsx [path/to/outputfile(.xlsx)]
                        This is an initialize helper option. Generate template
                        xlsx file based on same filename.yaml. **And if you
                        set this, other options are ignored.** will be
                        subcommand.

# generate subcommand help
$ jsonica.py gen -h
usage: jsonica.py generate [-h] [-v] [-i [path/to/inputfile]]
                                       [-hr tabsize] [-r [sheetname]]
                                       [-o [path/to/outputfile.json]]
                                       [-of [(csv | tsv):path/to/outputdir]]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i [path/to/inputfile], --input [path/to/inputfile]
                        Set path/to/input xlsx filename.
  -hr tabsize, --human_readable tabsize
                        set indent size by numeric value, Output humanreadable
                        json files.
  -r [sheetname], --root_sheet [sheetname]
                        set a sheetname in xlsx book have. construct json tree
                        from the sheet as root item. "root" is Default root
                        sheet name.
  -o [path/to/outputfile(.json)], --output [path/to/outputfile(.json)]
                        Output interpreted json. If this set which endswith
                        ".json" as set full filename, output jsonfile treated
                        as the name. But when not set ".json", adopt original
                        xlsx filename, like
                        path/to/outputfile/[source_METAFile_name].json (-o has
                        special filename "-" as STDOUT, and when set like "-o
                        -", all other stdout messages were masked.)
  -of [(csv | tsv):path/to/outputdir], --output_format [(csv | tsv):path/to/outputdir]
                        Output with the format, If you set this, output
                        formfiles to
                        path/to/[source_METAFile_name].xlsx/[sheetname.?sv]s
                        It'll be recommended, if you want to have
                        communication with non Tech team without any
                        gitconfiging.
```

## Appendix 3. MindMap
[mindnode(ja only)](https://my.mindnode.com/vWDYEyp9p7s2kFgCr4yzuVrokfimz3Cx2nvGR1Xg/em#97,31,-2)
