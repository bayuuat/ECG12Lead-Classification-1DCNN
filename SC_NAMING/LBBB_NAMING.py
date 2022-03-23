import os
import shutil
import csv


pathFVN = 'C:/Users/62812/PROJEK TA/DATASET MAS MPU/FVN/'
pathLBBB = 'C:/Users/62812/PROJEK TA/DATASET MAS MPU/LBBB/'
pathRBBB = 'C:/Users/62812/PROJEK TA/DATASET MAS MPU/RBBB/'
pathNormal = 'C:/Users/62812/PROJEK TA/DATASET MAS MPU/Normal/'
pathPVC = 'C:/Users/62812/PROJEK TA/DATASET MAS MPU/PVC/'


newDatasetPathTrain = 'C:/Users/62812/PROJEK TA/DATASET BARU/train/'
newDatasetPathTest = 'C:/Users/62812/PROJEK TA/DATASET BARU/test/'

i = 1
for filename in os.listdir(pathLBBB):
    if i <= 200:
        shutil.copyfile(os.path.join(pathLBBB, filename),
                        os.path.join(newDatasetPathTrain, 'LBBB'+str(i)+'.txt'))
        with open('trainlabel.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            file = 'LBBB'+str(i)+'.txt'
            data = [file, 'L']
            writer.writerow(data)

    else:
        shutil.copyfile(os.path.join(pathLBBB, filename),
                        os.path.join(newDatasetPathTest, 'LBBB'+str(i-200)+'.txt'))

    i = i + 1
    if i == 221:
        break
