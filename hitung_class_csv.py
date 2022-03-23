import pandas as pd
from pathlib import Path

class_list = []
sum_class = []
for z in range(76):
    pathAnno = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/newAnno/%d.txt' % z)

    file = Path(pathAnno)
    if file.is_file():
        # print("Reading ECG-%d" % z)
        anotasi = pd.read_csv(pathAnno, sep=',')
        npanotasi = anotasi.values
        tipe = npanotasi[:, 2]

        for x in tipe:
            class_list.append(x)

classes = list(dict.fromkeys(class_list))
for i in classes:
    counter = class_list.count(i)
    sum_class.append(counter)

print(classes)
print(sum_class)
