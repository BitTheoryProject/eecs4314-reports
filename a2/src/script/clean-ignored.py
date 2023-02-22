import re
toRemove = set()

with open('./ignored.txt') as file:
    for line in file:
        toRemove.add(line.strip())

# todo: accept ls.ta as arg. maybe write back to ls.ta file 
with open('./freebsd_IPC.ls.ta') as file, open('./res.txt', 'w') as newFile:
    for line in file:
        # get file path from line
        shouldAdd = True
        res = re.search(r"^(cLinks|\$INSTANCE)\s+(.*) (.*)\r?\n?$", line)
        if res:
            type, p1, p2 = res.groups()
            if p1 in toRemove or p2 in toRemove:
                shouldAdd = False
        if shouldAdd:
            newFile.write(line)
