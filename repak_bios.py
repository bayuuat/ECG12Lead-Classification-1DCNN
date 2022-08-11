import biosppy
import pandas as pd
import numpy as np
import csv
from scipy import signal

heartbeat = pd.read_csv("DATASET ST.PETERS/Sinyal30m/I1.csv", sep=',')

r_peaks_pan = heartbeat.iloc[:1285, 2]
r_peaks_pan = np.asarray(r_peaks_pan)

_, Filtrasi, _, _, _, _, _ = biosppy.signals.ecg.ecg(
    signal=r_peaks_pan, sampling_rate=257.0, show=True)
# _, FilteredAwal, RpeakAwal, _, _, _, _ = biosppy.signals.ecg.ecg(
#     signal=r_peaks_pan, sampling_rate=200.0, show=False)

# print("ORI")
# print(len(r_peaks_pan))
# print("SAMPLING")
# print(len(sinyalbaru))
# print('')
# print("FILTER ORI")
# print(FilteredAwal)
# print("FILTER SAMPL")
# print(len(Filtered))
# print('')
# print("RPEAK ORI")
# print(RpeakAwal)
print("RPEAK SAMPL")
print(Rpeak)


# header = ['no', 'sample']
# with open('anno_alat.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(header)

# no_id = 1

# list = []
# for line in Rpeak:
#     list.append(line)

# f = open("anno_alat.csv", "a")
# for v in list:
#     ecgs = str(no_id)+','+str(v) + '\n'

#     f.writelines(ecgs)
#     no_id += 1
# f.close()
