import numpy as np
import os
import shutil
import matplotlib.pyplot as plt
import csv
from matplotlib import cm
import math

def copyfile(outdir, Ku1, Temp):
    # name for the folder
    foldername = 'Ku1_%.1f_Temp_%d' % (Ku1, Temp)
    # name for mumax3 file in the folder
    mumax3name = os.path.join(foldername, 'AFM_' + foldername + '.mx3')
    # name for mumax3 output folder
    mumax3out = os.path.join(foldername, 'AFM_' + foldername + '.out')
    # set up new directory
    newout = os.path.join(outdir, 'AFM_' + foldername + '.out')
    os.makedirs(newout, exist_ok = True)
    # copy file to the directory
    shutil.copy(os.path.join(mumax3out, 'log.txt'), os.path.join(newout, 'log.txt'))
    shutil.copy(os.path.join(mumax3out, 'table.txt'), os.path.join(newout, 'table.txt'))
    shutil.copy(os.path.join(mumax3out, 'm000000.ovf'), os.path.join(newout, 'm000000.ovf'))
    shutil.copy(os.path.join(mumax3out, 'm000399.ovf'), os.path.join(newout, 'm000399.ovf'))
    shutil.copy(os.path.join(mumax3out, 'regions000000.ovf'), os.path.join(newout, 'region000000.ovf'))
    # copy mumax3 file
    shutil.copy(mumax3name, os.path.join(outdir, 'AFM_' + foldername + '.mx3'))
    return newout

def netplot(dim, net, imagename):
    # for quiver plot, we need to specify grids
    nx = np.arange(0,dim,1)
    ny = np.arange(0,dim,1)
    ny, nx = np.meshgrid(ny, nx)
    # get netx, nety and netz
    netx, nety, netz = net[:,:,0], net[:,:,1], net[:,:,2]
    # plot
    fig = plt.figure(figsize = (12,12))
    ax = fig.add_subplot(111)
    ax.set_aspect('equal', 'box')
    ax.quiver(nx, ny, netx, nety, netz, pivot = 'mid', cmap = cm.bwr, clim = (-1,1), scale_units='xy',angles='xy')
    plt.savefig(imagename)
    plt.close(fig)


def readnet(dim, filename):
    # read net vector from file
    netdata = np.loadtxt(open(filename,'rt').readlines()[:-2], skiprows = 28, dtype = float)
    net = np.empty((dim, dim, 3))
    # change the data into correct format
    for j in range(dim):
        for i in range(dim):
            net[i,j,0:3] = netdata[j*dim + i][0:3]

    return net

def calQ(n1, n2, n3):
    # calculate the topological number of a triangle
    number = np.dot(n1, np.cross(n2, n3)) / (1 + np.dot(n1, n2) + np.dot(n1, n3) + np.dot(n2, n3))
    numberQ = np.arctan(number) * 2
    return numberQ


def netanalysis(net,dim):
    toponumberN1 = 0; toponumberN2 = 0
    for j in range(dim):
        for i in range(dim):
            # deal with periodic boundary condtion
            il = i - 1
            if il < 0:
                il = il + dim
            ir = i + 1
            if ir >= dim:
                ir = ir - dim
            jl = j - 1
            if jl < 0:
                jl = jl + dim
            jr = j + 1
            if jr > 0:
                jr = jr - dim
            # calculate the four traingles
            # (i-1, j+1) (i+1, j+1)
            trag1 = calQ(net[i][j][0:3],net[il][jr][0:3],net[ir][jr][0:3])
            # (i-1, j+1) (i-1, j-1)
            trag2 = calQ(net[i][j][0:3],net[il][jr][0:3],net[il][jl][0:3])
            # (i-1, j-1) (i+1, j-1)
            trag3 = calQ(net[i][j][0:3],net[il][jl][0:3],net[ir][jl][0:3])
            # (i+1, j-1) (i+1, j+1)
            trag4 = calQ(net[i][j][0:3],net[ir][jl][0:3],net[ir][jr][0:3])
            
            # calculate site A and site B seperately
            if (i+j) % 2 == 0:
                toponumberN1 = toponumberN1 + 1 / (4*math.pi) * (trag1 + trag2 + trag3 + trag4)
            else:
                toponumberN2 = toponumberN2 + 1 / (4*math.pi) * (trag1 + trag2 + trag3 + trag4)

    return toponumberN1, toponumberN2


# specify the list of parameters 
Ku1list = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
Templist = [0, 50, 100, 150, 200, 250, 300]
#Ku1list = [0.4]
#Templist = [50]
# specify the output path
outdir = 'result'
# specify dimension
dim = 64

olist_Ku1 = []; olist_Temp = []
olist_topo1 = []; olist_topo2 = []

for Ku1 in Ku1list:
    for Temp in Templist:
        # copy file
        newout = copyfile(outdir, Ku1, Temp)
        # read net data from the file
        filename = os.path.join(newout, 'm000399.ovf')
        net = readnet(dim, filename)
        # plot figure
        imagename = os.path.join(outdir, 'AFM_Ku1_%.1f_Temp_%d.png' % (Ku1, Temp))
        netplot(dim, net, imagename)
        # get topological number
        topo1, topo2 = netanalysis(net,dim)
        # output
        olist_Ku1.append(Ku1)
        olist_Temp.append(Temp)
        olist_topo1.append(topo1)
        olist_topo2.append(topo2)

olist = zip(olist_Ku1, olist_Temp, olist_topo1, olist_topo2)

with open(os.path.join(outdir, 'results.csv'),'w') as ofile:
    writer = csv.writer(ofile, delimiter = '\t')
    writer.writerows(olist)




