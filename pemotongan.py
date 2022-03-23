import pandas as pd
from pathlib import Path
import csv

normal = 1
rbbb = 1
pvc = 1
apb = 1
fvn = 1

header = ['fname', 'label']
with open('label.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

for z in range(76):
    pathAnno = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/newAnno/%d.txt' % z)
    pathECG = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/Sinyal30m/I%d.csv' % z)

    file = Path(pathAnno)
    if file.is_file():
        y = 0
        print("Reading ECG-%d" % z)
        anotasi = pd.read_csv(pathAnno)
        npanotasi = anotasi.values
        sample = npanotasi[:, 1]
        tipe = npanotasi[:, 2]
        data = pd.read_csv(pathECG)
        npdata = data.values
        ecg = npdata[:, 1:]

        for x in tipe:
            if (x == "N") and (normal <= 2000):
                tengah = sample[y]
                awal = tengah-180
                if (awal >= 1) and (int(sample[y]+180) < len(ecg)):
                    f = open(
                        "C:/Users/62812/PROJEK TA/DATASET BAYU/NOR%d.txt" % normal, "w")
                    for i in ecg:
                        if awal == tengah+180:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = ecgs + '\n'
                        f.writelines(ecgs)
                        awal += 1
                    f.close()

                    with open('label.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        file = 'NOR'+str(normal)+'.csv'
                        data = [file, 'N']
                        writer.writerow(data)

                    normal += 1

            if (x == "V") and (pvc <= 2000):
                tengah = sample[y]
                awal = tengah-180
                if (awal >= 1) and (int(sample[y]+180) < len(ecg)):
                    f = open(
                        "C:/Users/62812/PROJEK TA/DATASET BAYU/PVC%d.txt" % pvc, "w")
                    for i in ecg:
                        if awal == tengah+180:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = ecgs + '\n'
                        f.writelines(ecgs)
                        awal += 1
                    f.close()

                    with open('label.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        file = 'PVC'+str(pvc)+'.csv'
                        data = [file, 'V']
                        writer.writerow(data)

                    pvc += 1

            if (x == "R") and (rbbb <= 2000):
                tengah = sample[y]
                awal = tengah-180
                if (awal >= 1) and (int(sample[y]+180) < len(ecg)):
                    f = open(
                        "C:/Users/62812/PROJEK TA/DATASET BAYU/RBBB%d.txt" % rbbb, "w")
                    for i in ecg:
                        if awal == tengah+180:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = ecgs + '\n'
                        f.writelines(ecgs)
                        awal += 1
                    f.close()

                    with open('label.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        file = 'RBBB'+str(rbbb)+'.csv'
                        data = [file, 'R']
                        writer.writerow(data)

                    rbbb += 1

            if (x == "A") and (apb <= 2000):
                tengah = sample[y]
                awal = tengah-180
                if (awal >= 1) and (int(sample[y]+180) < len(ecg)):
                    f = open(
                        "C:/Users/62812/PROJEK TA/DATASET BAYU/APB%d.txt" % apb, "w")
                    for i in ecg:
                        if awal == tengah+180:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = ecgs + '\n'
                        f.writelines(ecgs)
                        awal += 1
                    f.close()

                    with open('label.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        file = 'APB'+str(apb)+'.csv'
                        data = [file, 'A']
                        writer.writerow(data)

                    apb += 1

            if (x == "F") and (fvn <= 2000):
                tengah = sample[y]
                awal = tengah-180
                if (awal >= 1) and (int(sample[y]+180) < len(ecg)):
                    f = open(
                        "C:/Users/62812/PROJEK TA/DATASET BAYU/FVN%d.txt" % fvn, "w")
                    for i in ecg:
                        if awal == tengah+180:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = ecgs + '\n'
                        f.writelines(ecgs)
                        awal += 1
                    f.close()

                    with open('label.csv', 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        file = 'FVN'+str(fvn)+'.csv'
                        data = [file, 'F']
                        writer.writerow(data)

                    fvn += 1

            y += 1
print("DONE")
