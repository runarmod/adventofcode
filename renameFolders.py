import os

for i in range(2015, 2022):
    i = str(i)
    for folder in os.listdir(os.path.join(os.getcwd(), i)):
        os.rename(os.path.join(os.getcwd(), i, folder), os.path.join(os.getcwd(), i, folder.zfill(2)))
