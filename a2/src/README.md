# Setup

1. extract [FreeBSD 12.4.0](https://github.com/freebsd/freebsd-src/releases/tag/release%2F12.4.0) source
2. Download [Understand](https://licensing.scitools.com/login) with education license
3. Open Understand IDE
4. `file` > `new` > `project` and open extracted source
5. Wait for analysis
6. `project` > `export dependencies` > `file dependencies` > `export csv` to `eecs4313-reports/a2/src/`
7. Might need to do additional preprocessing on output

# Instructions to Visualize Dependency

1. run `perl script/csv-to-ta.pl freebsd_FileDependencies.csv` (convert csv to raw.ta)
2. run `perl script/gen-containment.pl freebsd_FileDependencies.raw.ta <contain-filename> <freebsd-src-path> <subsystems-json>` (create contain file)
3. run `script/final-containment.sh -j lib/ql.jar -t freebsd_FileDependencies.raw.ta -c <contain-filename> -n <subsystems-name>` (create final .con.ta, ls.ta, ignored.txt files)
4. run `python script/clean-ignored.py -t <subsystems-name>.ls.ta -i ignored.txt -r res.txt` (filter ignored files from ls.ta)
5. run `script/ls-edit.sh -j lib/lseditor-7.3.13.jar -f <subsystems-name>.ls.ta` (visualize file dependency with containment structure)
