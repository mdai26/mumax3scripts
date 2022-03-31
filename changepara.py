import numpy as np
import os
import shutil

# specify the list of parameters 
Ku1list = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
Templist = [0, 50, 100, 150, 200, 250, 300]
# specify the current path
path = '/ocean/projects/dmr180039p/mdai26/AFMsimulation/diffKdiffTemp'

for Ku1 in Ku1list:
    for Temp in Templist:
        # specify folder name and make the folder
        foldername = 'Ku1_%.1f_Temp_%d' % (Ku1, Temp)
        os.makedirs(foldername, exist_ok = True)
        # specify the name of mumax3 file
        efilename = 'AFM_' + foldername + '.mx3'
        # copy the mumax3 file to the folder
        shutil.copy2('AFM.mx3', os.path.join(foldername, efilename))
        # read the parameter and replace the variables
        fin = open(os.path.join(foldername, efilename), 'rt')
        para = fin.read()
        para = para.replace('Ku1Value', str(int(Ku1*1e5)))
        para = para.replace('TempValue', str(Temp))
        fin.close()
        # write the changed parameters to the mumax3 file
        fin = open(os.path.join(foldername, efilename), 'wt')
        fin.write(para)
        fin.close()
        shutil.copy2('run.sh', os.path.join(foldername, 'run.sh'))
        # read the run.sh and replace variables
        fin = open(os.path.join(foldername, 'run.sh'), 'rt')
        para = fin.read()
        para = para.replace('filename', efilename)
        fin.close()
        # write the changed parameters to mumax3 file
        fin = open(os.path.join(foldername, 'run.sh'), 'wt')
        fin.write(para)
        fin.close()
        # change directory to submit jobs
        os.chdir(os.path.join(path, foldername))
        os.system("sbatch run.sh")
        # change back
        os.chdir(path)



