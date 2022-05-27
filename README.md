# Scripts for MuMax3 

This repo contains the python codes and scripts for mumax3 simulation.

## Automatically change parameters and submit jobs

changepara.py can be used to automatically

1) replace the values of anisotropy and temperature in the file AFM.mx3
2) Submit jobs to perform simulation with different physical parameters.

```
python changepara.py
```
Note: AFM.mx3, changepara.py and run.sh need to be put in the same folder.

## Calculate topological number and plot the magnetization automatically
collectresult.py can be used to automatically

1) Copy needed files to a new folder
2) Plot the final magnetization distribution and save it as an image.
3) Calculate the corresponding topological number using the discretized method
4) Save the topological number under different physical parameters in a txt file.

```
python collectresult.py
```
## extract total energy from table.txt
getenergy.py can be used to automatically
1) extract total energy from a certain time step of table.txt file
2) save the extracted energy in csv file

```
python getenergy.py
```
