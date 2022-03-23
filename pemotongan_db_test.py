import pandas as pd
from pathlib import Path
import csv

normal = 1
rbbb = 1
pvc = 1
apb = 1
fvn = 1
no_id = 99001

for z in range(10, 76):
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
        ecg = npdata[:, :]

        for x in tipe:
            if (x == "N") and (normal <= 200):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_baru.csv", "a")
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
            if (x == "V") and (pvc <= 200):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_baru.csv", "a")
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
                pvc += 1
                no_id += 1
            if (x == "R") and (rbbb <= 200):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_baru.csv", "a")
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
            if (x == "A") and (apb <= 200):
                tengah = sample[y]
                awal = tengah-40
                if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
                    f = open("db_baru.csv", "a")
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
            # if (x == "F") and (fvn <= 100):
            #     tengah = sample[y]
            #     awal = tengah-40
            #     if (awal >= 1) and (int(sample[y]+40) < len(ecg)):
            #         f = open("db_baru.csv", "a")
            #         for i in ecg:
            #             if awal == tengah+40:
            #                 break
            #             list = []
            #             for line in ecg[awal]:
            #                 list.append(line)
            #             ecgs = ','.join(str(v) for v in list)
            #             ecgs = str(no_id)+','+x+','+ecgs + '\n'

            #             f.writelines(ecgs)
            #             awal += 1
            #         f.close()
            #     fvn += 1
            #     no_id += 1
            y += 1
print("DONE")
