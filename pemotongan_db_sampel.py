from itertools import count
import pandas as pd
from pathlib import Path
import csv

no_id = 1

header = ['id', 'label', 'time', 'I', 'II', 'III', 'AVR',
          'AVL', 'AVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
with open('db_80_sampel.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
with open('db_80_val_sampel.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
with open('db_80_test_sampel.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

normal = 1
for z in range(76):
    pathAnno = (
        'C:/Users/62812/PROJEK TA/DATASET ST.PETERS/newAnno/%d.txt' % z)
    pathECG = (
        'C:/Users/62812/PROJEK TA/DATASET ST.PETERS/Sinyal30m/I%d.csv' % z)

    file = Path(pathAnno)
    if file.is_file():
        hitung = 1
        y = 0
        print("Reading For NORMAL ECG-%d" % z)
        anotasi = pd.read_csv(pathAnno)
        npanotasi = anotasi.values
        sample = npanotasi[:, 1]
        tipe = npanotasi[:, 2]
        data = pd.read_csv(pathECG)
        npdata = data.values
        ecg = npdata[:, :]

        for x in tipe:
            if (x == "N") and (hitung <= 40):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    normal += 1
                    no_id += 1
                    hitung += 1

            elif (x == "N") and (hitung <= 45):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_val_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    normal += 1
                    no_id += 1
                    hitung += 1

            elif (x == "N") and (hitung <= 50):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_test_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    normal += 1
                    no_id += 1
                    hitung += 1
            y += 1
    if(normal > 3000):
        break

total_pvc = 1
# for z in range(76):
#     pathAnno = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/newAnno/%d.txt' % z)
#     pathECG = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/Sinyal30m/I%d.csv' % z)

#     file = Path(pathAnno)
#     if file.is_file():
#         pvc = 1
#         y = 0
#         print("Reading For PVC ECG-%d" % z)
#         print(total_pvc)
#         anotasi = pd.read_csv(pathAnno)
#         npanotasi = anotasi.values
#         sample = npanotasi[:, 1]
#         tipe = npanotasi[:, 2]
#         data = pd.read_csv(pathECG)
#         npdata = data.values
#         ecg = npdata[:, :]

#         for x in tipe:
#             if (x == "V") and (total_pvc <= 2400):
#                 tengah = sample[y]
#                 awal = tengah-40
#                 if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
#                     f = open("db_80_sampel.csv", "a")
#                     for i in ecg:
#                         if awal == tengah+40:
#                             break
#                         list = []
#                         for line in ecg[awal]:
#                             list.append(line)
#                         ecgs = ','.join(str(v) for v in list)
#                         ecgs = str(no_id)+','+x+','+ecgs + '\n'

#                         f.writelines(ecgs)
#                         awal += 1
#                     f.close()
#                     pvc += 1
#                     total_pvc += 1
#                     no_id += 1

#             if (x == "V") and (total_pvc > 2400) and (total_pvc <= 2700):
#                 tengah = sample[y]
#                 awal = tengah-40
#                 if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
#                     f = open("db_80_val_sampel.csv", "a")
#                     for i in ecg:
#                         if awal == tengah+40:
#                             break
#                         list = []
#                         for line in ecg[awal]:
#                             list.append(line)
#                         ecgs = ','.join(str(v) for v in list)
#                         ecgs = str(no_id)+','+x+','+ecgs + '\n'

#                         f.writelines(ecgs)
#                         awal += 1
#                     f.close()
#                     pvc += 1
#                     total_pvc += 1
#                     no_id += 1

#             if (x == "V") and (total_pvc > 2700) and (total_pvc <= 3000):
#                 tengah = sample[y]
#                 awal = tengah-40
#                 if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
#                     f = open("db_80_test_sampel.csv", "a")
#                     for i in ecg:
#                         if awal == tengah+40:
#                             break
#                         list = []
#                         for line in ecg[awal]:
#                             list.append(line)
#                         ecgs = ','.join(str(v) for v in list)
#                         ecgs = str(no_id)+','+x+','+ecgs + '\n'

#                         f.writelines(ecgs)
#                         awal += 1
#                     f.close()
#                     pvc += 1
#                     total_pvc += 1
#                     no_id += 1
#         y += 1

#     if(total_pvc > 3000):
#         break

rbbb = 1
apb = 1
for z in range(76):
    pathAnno = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/newAnno/%d.txt' % z)
    pathECG = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/Sinyal30m/I%d.csv' % z)

    file = Path(pathAnno)
    if file.is_file():
        y = 0
        print("Reading For RBBB ECG-%d" % z)
        anotasi = pd.read_csv(pathAnno)
        npanotasi = anotasi.values
        sample = npanotasi[:, 1]
        tipe = npanotasi[:, 2]
        data = pd.read_csv(pathECG)
        npdata = data.values
        ecg = npdata[:, :]

        for x in tipe:
            if (x == "V") and (total_pvc <= 2400):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    total_pvc += 1
                    no_id += 1

            if (x == "V") and (total_pvc > 2400) and (total_pvc <= 2700):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_val_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    total_pvc += 1
                    no_id += 1

            if (x == "V") and (total_pvc > 2700) and (total_pvc <= 3000):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_test_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    total_pvc += 1
                    no_id += 1

            if (x == "R") and (rbbb <= 2400):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    rbbb += 1
                    no_id += 1

            if (x == "R") and (rbbb > 2400) and (rbbb <= 2700):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_val_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    rbbb += 1
                    no_id += 1

            if (x == "R") and (rbbb > 2700) and (rbbb <= 3000):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_test_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    rbbb += 1
                    no_id += 1

            if (x == "A") and (apb <= 2400):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    apb += 1
                    no_id += 1

            if (x == "A") and (apb > 2400) and (apb <= 2700):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_val_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    apb += 1
                    no_id += 1

            if (x == "A") and (apb > 2700) and (apb <= 3000):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_80_test_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+40:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    apb += 1
                    no_id += 1

            y += 1

for z in range(76):
    pathAnno = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/newAnno/%d.txt' % z)
    pathECG = ('C:/Users/62812/PROJEK TA/DATASET ST.PETERS/Sinyal30m/I%d.csv' % z)

    file = Path(pathAnno)
    if file.is_file():
        y = 0
        print("Reading For APB ECG-%d" % z)
        anotasi = pd.read_csv(pathAnno)
        npanotasi = anotasi.values
        sample = npanotasi[:, 1]
        tipe = npanotasi[:, 2]
        data = pd.read_csv(pathECG)
        npdata = data.values
        ecg = npdata[:, :]

        for x in tipe:
            if (x == "A") and (apb <= 2400):
                tengah = sample[y]
                awal = tengah-50
                if (awal >= 1) and (int(sample[y]+30) < len(ecg)):
                    f = open("db_80_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+30:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    apb += 1
                    no_id += 1

            if (x == "A") and (apb > 2400) and (apb <= 2700):
                tengah = sample[y]
                awal = tengah-50
                if (awal >= 1) and (int(sample[y]+30) < len(ecg)):
                    f = open("db_80_val_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+30:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    apb += 1
                    no_id += 1

            if (x == "A") and (apb > 2700) and (apb <= 3000):
                tengah = sample[y]
                awal = tengah-50
                if (awal >= 1) and (int(sample[y]+30) < len(ecg)):
                    f = open("db_80_test_sampel.csv", "a")
                    for i in ecg:
                        if awal == tengah+30:
                            break
                        list = []
                        for line in ecg[awal]:
                            list.append(line)
                        ecgs = ','.join(str(v) for v in list)
                        ecgs = str(no_id)+','+x+','+ecgs + '\n'

                        f.writelines(ecgs)
                        awal += 1
                    f.close()
                    apb += 1
                    no_id += 1

            y += 1

    if(apb > 3000):
        break

print("DONE")
