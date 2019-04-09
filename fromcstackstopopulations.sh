#!/bin/sh
module load Stacks
mkdir -p catalog
cstacks  -P SNPcall_default/ -M  popmap.txt -p 18 --k_len 6
#run the last thirty then
#echo "cstacks done"

sstacks -P SNPcall_default  -M popmap.txt -p 8

#echo "sstacks done"

tsv2bam -P SNPcall_default -M popmap.txt -t 8

#echo "gstacks done"

gstacks -P SNPcall_default -M  popmap.txt -t 8

#echo "gstacks done"

populations -P SNPcall_default/  -M popmap.txt -p 1 -r 0.00	 --vcf --genepop --structure --fstats --hwe  -t 8

#echo "populations done"
