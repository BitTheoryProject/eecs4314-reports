# Setup

1. extract [FreeBSD 12.4.0](https://github.com/freebsd/freebsd-src/releases/tag/release%2F12.4.0) source
2. Download [Understand](https://licensing.scitools.com/login) with education license
3. Open Understand IDE
4. `file` > `new` > `project` and open extracted source
5. Wait for analysis
6. `project` > `export dependencies` > `file dependencies` > `export csv` to `eecs4313-reports/a2/src/`
7. Might need to do additional preprocessing on output

# Methods to Extract Dependencies

1. [Understand](https://licensing.scitools.com/login) (see [A2 source](/a2/src/README.md))
2. Custom Include Extraction Scripts
   1. run `python script/gen-ta-file.py -t <subsystem>.raw.ta -ss <subsystems-json-file> -s <src_path>` (create raw.ta file)
   2. run `python script/gen-containment.py -t <subsystem>.raw.ta -c <containment_file_name> -ss <subsystems-json-file> -s <src_path>` (create contain file)
   3. run `script/final-containment.sh -j lib/ql.jar -t <subsystem>.raw.ta -c <contain-filename> -n <subsystems-name>` (create final .con.ta, ls.ta, ignored.txt files)
   4. run `python script/clean-ignored.py -t <subsystems-name>.ls.ta -i ignored.txt -r res.txt` (filter ignored files from ls.ta)
   5. run `script/ls-edit.sh -j lib/lseditor-7.3.13.jar -f <subsystems-name>.ls.ta` (visualize file dependency with containment structure)
3. to-do, srcML
