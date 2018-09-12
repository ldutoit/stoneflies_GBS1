# stoneflies_GBS1

## Description
A RADSeq dataset from NZ stoneflies, looking at ther popgen with a focus on the different morphotypes.

## Key Players
Graham McCulloch, Jon Waters

## Objectives
I start with the SNP calling. We will see the rest later.

## Physical location of the data
The sequenced library and the sample information file is here on Google Drive. Contact me for access.

It consists of 2 lanes to a total of approximately 	180 flies.

## Source files

The sequenced library and the sample information file is  on the local high capacity storage at otago uni:

storage.hcs-p01.otago.ac.nz/sci-bioinformatics-project-archive

## Analyses
### SNP calling

We started the SNP calling using STACKS v 2.0. The whole process is described in [SNPcalling.md](SNPcalling.md).


### Summary

output_snpfiles_restricted :  4633 sites covered for at least 80 % of 166 individuals. We kept mmaximum 1 site in each 100bp fragment (i.e. each stacks) while excluding fragments with more than 3 sites (i.e. likely to be repeats).