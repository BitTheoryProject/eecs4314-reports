# Setup

1. extract [FreeBSD 12.4.0](https://github.com/freebsd/freebsd-src/releases/tag/release%2F12.4.0) source
2. Download [Understand](https://licensing.scitools.com/login) with education license
3. Open Understand IDE
4. `file` > `new` > `project` and open extracted source
5. Wait for analysis
6. `project` > `export dependencies` > `file dependencies` > `export csv` to `eecs4313-reports/a2/src/`
7. Might need to do aditional preprocessing on output

# Instructions to Visualize dependency

1. run `perl script/csv-to-ta.pl ./freebsd_FileDependencies.csv` (convert csv to raw.ta)
2. run `perl script/gen-containment.pl ./freebsd_FileDependencies.raw.ta ./freebsd_IPC.contain <freebsd-src-path>` (create contain file)
3. run `script/final-containment.sh -c freebsd_IPC.contain -t freebsd_FileDependencies.raw.ta -n freebsd_IPC -j lib/ql.jar` (create final ls.ta file)
4. run `script/ls-edit.sh -f ./freebsd_IPC.con.ta -j lib/lseditor-7.3.13.jar` (visualize file dependency with containment structure)
