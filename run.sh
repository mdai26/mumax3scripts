#!/bin/bash

# Run the short-list GPU queue
#SBATCH -p GPU-shared

## Request a GPU from the scheduler, we don't care what kind
#SBATCH --gres=gpu:1
#SBATCH -t 1-00:00 # time (D-HH:MM)

## Create a unique output file for the job
#SBATCH -o test-%j.out
#SBATCH -e test-%j.err

# run the training scripts
module load cuda
mumax3 filename
