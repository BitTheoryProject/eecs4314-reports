# Methods to Extract Dependencies

`<method-name> = understand|srcML|custom`

1. create `raw.ta file`
   1. if `<method-name>` = [understand](https://licensing.scitools.com/login)
      1. run `perl script/csv-to-ta.pl freebsd_FileDependencies.csv` (convert csv to raw.ta, [A2 source](/a2/src/README.md))
   2. if `method-name>` = `srcML` run 
      2.1 Navigate to FreeBSD source code directory. run `srcml ./freebsd-src-release-12.4.0/sys -o FreeBSD_Kernel.xml`
      2.2 Apply the XPath query to the generated xml, run `srcml FreeBSD_Kernel.xml --xpath="//src:unit[@type='include']/@filename | //cpp:include/cpp:file" > freeBSD_Kernel_dependencies.xml`
      2.3 run `python3 script/gen-ta-file-srcml.py -t method-srcML/freebsd_kernel.raw.ta -ss kernel_ss.json -s <freebsd-src> -x <srcMl-xml>` on the generated xml from part 2. 
   3. if `method-name>` = `custom` run `python3 script/gen-ta-file.py -t method-custom/freebsd_kernel.raw.ta -ss kernel_ss.json -s <freebsd-src>`
2. run `python3 script/gen-containment.py -t method-<method-name>/freebsd_kernel.raw.ta -c method-<method-name>/freebsd_kernel.contain -ss kernel_ss.json -s <freebsd-src>` (create contain file)
3. run `script/final-containment.sh -j lib/ql.jar -t method-<method-name>/freebsd_kernel.raw.ta -c method-<method-name>/freebsd_kernel.contain -n method-<method-name>/freebsd_kernel` (create final .con.ta, ls.ta, ignored.txt files)
4. run `python3 script/clean-ignored.py -t method-<method-name>/freebsd_kernel.ls.ta  -i ignored.txt -r res.txt -o` (filter ignored files from ls.ta)
5. run `script/ls-edit.sh -j lib/lseditor-7.3.13.jar -f freebsd_kernel.ls.ta` (visualize file dependency with containment structure)

# Performance Analysis & Comparison 

`python3 script/gen-statistics.py -a1 method-understand/freebsd_kernel.ls.ta -a2 method-srcML/freebsd_kernel.ls.ta -a3 method-custom/freebsd_kernel.ls.ta -o results.txt`