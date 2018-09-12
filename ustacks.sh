#!/bin/bash
#REQUISITE process radtags should output sample files into $src/samples .. the pipeline should be checked along the way for options
##This is designed to run on slurm systems BUT individual command lines for stacks are easily identifiable





###PARAMETERS

module load Stacks
src=/home/ludovic.dutoit/projects/RAD_Acacia/STACKS

files=$(ls  samples)

mkdir -p jobs
mkdir -p SNPcall_default/
#

# 1. USTACKS ( finding loci/stacks for each individual)



# Build loci de novo in each sample for the single-end reads only. If paired-end reads are available, 
# they will be integrated in a later stage (tsv2bam stage).
# This loop will run ustacks on each sample, e.g.
#
id=1
for sample in $files
do
    echo $'#!/bin/sh\nmodule load Stacks'  > jobs/ustacks$sample.job
    echo "ustacks  -t gzfastq -f samples/$sample -o SNPcall_default/ -i $id  -p 8" >> jobs/ustacks$sample.job # this is the command
    let "id+=1"
    cat jobs/ustacks$sample.job
    sbatch -A uoo00116 -t 10:00:00  -N 1 -c 4  --mem=32G  -J $sample jobs/ustacks$sample.job  
done




