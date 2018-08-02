# stoneflies_GBS1

## Description
A RADSeq dataset from NZ stoneflies, looking at ther popgen with a focus on the different morphotypes.

## Key Players
Graham McCulloch, Jon Waters

## Objectives
I am start with the SNP calling. We will see the rest later.

## Physical location of the data
The sequenced library and the sample information file is here on Google Drive. Contact me for access.

It consists of X samples sequenced with inline barcode on a single-end ILLUMNA library with the restriction enzyme PstI as a cutter.

## Source files

Add later 


## Analyses
### SNP calling
**In construction**



We started the SNP calling using STACKS v 2.0. The whole process is described in SNPcalling.md. 


***Plan***

After Stacks filtering,  keep only 1 SNP per stack (i.e. 100bp locus made of stacked read) for stacks with max 2 SNPs. SNPs with less than 80% individuals with >=1 reads would also be excluded.
