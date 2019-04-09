# stoneflies_GBS1

## Description
This repository describes the SNP calling associated to the manuscript


**Treeline drives insect wing loss, genome-wide divergence and speciation**
Graham A. McCulloch, Brodie J. Foster, Ludovic Dutoit, Eleanor Hay, Andrew J. Veale, Peter K. Dearden, Jonathan M. Waters
.



## Source files

The sequenced library and the sample information file is  on the local high capacity storage at otago uni:

storage.hcs-p01.otago.ac.nz/sci-bioinformatics-project-archive

It is in the process of being uploaded to the short read archive


## Analyses
### SNP calling

We started the SNP calling using STACKS v 2.0. The whole process is described in [SNPcalling.md](SNPcalling.md).


### reassigned pops


I transformed the dataset of 14 sample locations into 4 populations using [reassign.py](reassign.py) and created the files output_snpfiles_restricted/filtered4pops.vcf,  output_snpfiles_restricted/filtered4pops.str output_snpfiles_restricted/filtered4pops.dat.

The pops were:

```
Lug Vestigial  (LV)
Lug Full (LF)
Six Vestigial (SV)
Six Full (SF)
```

### Summary

[output_snpfiles_restricted](output_snpfiles_restricted)  4633 sites covered for at least 80 % of 166 individuals. We kept maximum 1 site in each 100bp fragment (i.e. each stacks) while excluding fragments with more than 3 sites (i.e. likely to be repeats).

The file with the **4pops** extension change nothing else than individual names from sampling location to populations.
