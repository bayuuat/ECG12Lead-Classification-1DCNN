import pandas as pd
from pathlib import Path

for z in range(76):
    pathAnno = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/Annot/%d.txt' % z)

    file = Path(pathAnno)
    if file.is_file():

        # first get all lines from file
        with open(pathAnno, 'r') as f:
            lines = f.readlines()

        # remove spaces
        list = []
        for line in lines:
            la = line.split()
            la = ','.join(la)
            la = la.replace('Sample,#', 'Sample#')
            l = la + '\n'
            list.append(l)

        # finally, write lines in the file
        with open('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/newAnno/%d.txt' % z, 'w') as f:
            f.writelines(list)

print("DONE")
