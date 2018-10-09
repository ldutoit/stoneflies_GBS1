# stoneflies_GBS1

## Description
A RADSeq dataset from NZ stoneflies, looking at ther popgen with a focus on the different morphotypes.

## Key Players
Graham McCulloch, Jon Waters

## Objectives
I start with the SNP calling. We will see the rest later.

## Physical location of the data
The sequenced library and the sample information file is here on Google Drive. Contact me for access.

It consists of 2 lanes to a total of approximately 	180 flies. After QC, the total number of flies was reduced to 166.

## Source files

The sequenced library and the sample information file is  on the local high capacity storage at otago uni:

storage.hcs-p01.otago.ac.nz/sci-bioinformatics-project-archive

## Analyses
### SNP calling

We started the SNP calling using STACKS v 2.0. The whole process is described in [SNPcalling.md](SNPcalling.md).


### reassigned pops


I transformed the dataset of 14 pops into 4 pops using reassign.py and created the files output_snpfiles_restricted/filtered4pops.vcf,  output_snpfiles_restricted/filtered4pops.str output_snpfiles_restricted/filtered4pops.dat.

The pops were:

```
Lug Vestigial  (LV)
Lug Full (LF)
Six Vestigial (SV)
Six Full (SF)
```

### Summary

output_snpfiles_restricted :  4633 sites covered for at least 80 % of 166 individuals. We kept maximum 1 site in each 100bp fragment (i.e. each stacks) while excluding fragments with more than 3 sites (i.e. likely to be repeats).

The file with the **4pops** extension change nothing else than individual names!
