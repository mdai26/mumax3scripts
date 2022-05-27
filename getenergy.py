import numpy as np
import os
import shutil
import matplotlib.pyplot as plt
import csv
from matplotlib import cm
import math

# specify the list of parameters 
Ku1list = [1.5]
Templist = range(0,100,2)
# specify the output path
outdir = 'result'
# specify dimension
dim = 64

energy = []

for Ku1 in Ku1list:
    for Temp in Templist:
        # read net data from the file
        foldername = os.path.join(outdir, 'AFM_Ku1_%.1f_Temp_%d.out' % (Ku1, Temp)) 
        filename = os.path.join(foldername, 'table.txt')
        data = np.loadtxt(filename, skiprows=1)
        energy.append(data[7980,8])

olist = zip(Templist, energy)

with open(os.path.join(outdir, 'energy.csv'),'w') as ofile:
    writer = csv.writer(ofile, delimiter = '\t')
    writer.writerows(olist)




