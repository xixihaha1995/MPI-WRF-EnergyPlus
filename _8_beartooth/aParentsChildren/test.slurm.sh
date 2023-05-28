#!/bin/bash

#SBATCH --account=communitybem
#SBATCH --time=00:01:00
#SBATCH --partition=teton
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --job-name=configure_script
#SBATCH --output=configure_script_%j.out
#SBATCH --error=configure_script_%j.err

# Set the directory where you want to install the software, Change to the source code directory
DIR="/home/lwu4/fortran_experiments/_8_beartooth/aParentsChildren"
cd $DIR
pwd

# Print the node list assigned to the job
echo "Job running on nodes:"
echo $SLURM_JOB_NODELIST

# Print the environment variables
echo "Environment variables:"
env

# Print the SLURM job ID and task information
echo "SLURM job ID: $SLURM_JOB_ID"
echo "Number of tasks: $SLURM_NTASKS"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "Tasks per node: $SLURM_TASKS_PER_NODE"

# Execute the program
srun ./parent.exe
