	#!/bin/bash
#REQUISITE process radtags should output sample files into $src/samples .. the pipeline should be checked along the way for options
##This is designed to run on slurm systems BUT individual command lines for stacks are easily identifiable


#Stacks proceeds in six major stages. 
#First, reads are demultiplexed and cleaned by the process_radtags program. 
#The next three stages comprise the main Stacks pipeline: building loci (ustacks), 
#creating the catalog of loci (cstacks), and matching against the catalog (sstacks). 
#In the fifth stage, the gstacks program is executed to assemble and merge paired-end 
#contigs, call variant sites in the population and genotypes in each sample. 
#In the final stage, the populations program is executed, depending on the type of input data. 
#This flow is diagrammed in the following figure.


###PARAMETERS

#module load Stacks
src=/home/ludovic.dutoit/projects/stoneflies_GBS1/STACKS

files=$(ls  samples)

mkdir -p stacks
mkdir -p jobs
mkdir -p SNPcall_default
#

# 1. USTACKS ( finding loci/stacks for each individual)



# Build loci de novo in each sample for the single-end reads only. If paired-end reads are available, 
# they will be integrated in a later stage (tsv2bam stage).
# This loop will run ustacks on each sample, e.g.
#
id=1
for sample in $files
do
    echo $sample
    echo $'#!/bin/sh\nmodule load Stacks'  > jobs/ustacks$sample.job
    echo "ustacks  -t gzfastq -f samples/$sample -o SNPcall_default/ -i $id  -p 2" >> jobs/ustacks$sample.job # this is the command
    let "id+=1"
    cat jobs/ustacks$sample.job
    sbatch -A uoo00116 -t 1-00:00:00 -p node -n 1 -c 2  --mem=16G  -J $sample jobs/ustacks$sample.job  
done


#If "some of them fails for memory issues: run ustacksfail once you found the one that failed rerun them but with the right  -i


# If the problem is that one file is too big, it cab be subsamples, I did it using subsampleustacks.md for the sample AU_N_1 but it did not help

# AT THIS STAGE, we dropped the sample AU_N_1 cause even subsampling we did not make it run



#2. CSTACKS
# Build the catalog of loci available in the metapopulation from the samples contained
# in the population map. To build the catalog from a subset of individuals, supply
# a separate population map only containing those samples.
#cstacks  -P $src/stacks/ -M $src/popmaps/popmap -p 1 -n 16

echo $'#!/bin/sh\nmodule load Stacks\n mkdir -p catalog'  > cstacks.sh
echo "cstacks  -P SNPcall_default/ -M  popmap.txt -p 12 --k_len 6 " >> cstacks.sh # this is the command
sbatch -A uoo00116 -t 2-00:00:00  -J cstacks  -p node -n 1 -c 12  --mem=128G cstacks.sh

#
# Run sstacks. Match all samples supplied in the population map against the catalog. HEAVY!
#sstacks -P $src/stacks/ -M $src/popmaps/popmap -p 8

echo $'#!/bin/sh\nmodule load Stacks'  > sstacks.sh
echo "sstacks -P SNPcall_default  -M popmap.txt -p 8" >> sstacks.sh # this is the command
sbatch -A uoo00116 -t 3-00:00:00  -J sstacks  -p node -n 1 -c 8  --mem=64G sstacks.sh

#
# Run tsv2bam to transpose the data so it is stored by locus, instead of by sample. We will include
# paired-end reads using tsv2bam. 
#
echo $'#!/bin/sh\nmodule load Stacks'  > tsv2bam.sh
echo "tsv2bam -P SNPcall_default -M popmap.txt -t 8 " >> tsv2bam.sh # this is the command
sbatch -A uoo00116 -t 2-00:00:00  -J tsv2bam  -p node -n 1 -c 8  --mem=64G tsv2bam.sh


# Run gstacks: build a paired-end contig from the metapopulation data (if paired-reads provided),
# align reads per sample, call variant sites in the population, genotypes in each individual.
#
echo $'#!/bin/sh\nmodule load Stacks'  > gstacks.sh
echo "gstacks -P SNPcall_default -M  popmap.txt -t 1 " >> gstacks.sh # this is the command
sbatch -A uoo00116 -t 04:00:00  -J gstacks  -p node -n 1 -c 8  --mem=64G gstacks.sh

# Run populations. Calculate Hardy-Weinberg deviation, population statistics, f-statistics
# export several output files. 


#Populations
#I do it no filters so I can blacklist loci in the vcf file outputted by populations


echo $'#!/bin/sh\nmodule load Stacks'  > populations0.sh
echo "populations -P SNPcall_default/  -M popmap.txt -p 1 -r 0.00	 --vcf --genepop --structure --fstats --hwe  -t 8 " >> populations0.sh # this is the command
sbatch -A uoo00116 -t 2-00:00:00  -J populations0  -p node -n 1 -c 8  --mem=64G populations0.sh





