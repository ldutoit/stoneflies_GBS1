## SNPcalling.md


For the SNP calling, I used STACKS [version 2.0b](http://catchenlab.life.illinois.edu/stacks/)

SAY SOMETHING ON IND CODES


I followed a DENOVO procedure where I called loci in the absence of reference genome. The general procedure is outline in the stacks on the [software website](http://catchenlab.life.illinois.edu/stacks/manual/). I started by a quick quality control step looking at our reads using fastQC and did not notice any contamination.



## Process radtags (STACKS first step)

First I create [snp_calling_files/barcodes.txt](snp_calling_files/barcodes.txt).

Then I call process radtags which will separate the reads per individual with barcode rescue (allowing 1 mismatch in the barcode). It is important to have one folder (i.e. here raw) that contains all the files with reads(i.e. only USDA_S1_L001_R1_001_trimmed97clean.fastq) and nothing else.


```
 process_radtags -i gzfastq -p raw/ -o ./samples/ -b barcodes.txt -e pstI  -c -q --inline_null -r
274117278 total sequences
 11140915 ambiguous barcode drops (4.1%)
   200341 low quality read drops (0.1%)
  1365091 ambiguous RAD-Tag drops (0.5%)
261410931 retained reads (95.4%)
```

We also ran FastQC on this. As expected, barcodes were gone and the enzyme is left in. That is a good checkpoint to have a look at overrepresented sequences and remove contamination.


## STACKS pipeline

I create a [population map](snp_calling_files/popmap.txt) that is required by STACKS, there is no population information actually contained in it.

Then I call SNPs denovo using the pipeline in [stacks_pipeline.sh](stacks_pipeline.sh)

## Post-STACKS Filtering

Out of STACKS we obtained 330 648 SNPs. We had not filtered those for coverage across individuals or coverage within individuals.

Furthermore, one could see that there are many stacks with multiple SNPs within a 100bp, which can be an indication of repeats merged as a single stacks:

```
# count number of SNP per stacks in bash
cat   SNPcall_default/populations.snps.vcf | grep -v "^#" |  cut -f 1 | uniq -c | sort | sed  -E 's/^\s+//g' > nsnpsperstacks.txt
## plot in R
data<-read.table("nsnpsperstacks.txt",h=F)
	table(data[,1])

  1     2     3     4     5     6     7     8     9    10    11    12    13
43722 21716 11533  6998  4111  2603  1623   937   607   344   199   126    68
   14    15    16    17    18    19    20    21
   40    28    21     9     5     3     1     2
```


We then ran filter_stacks_vcf.py requiring at least 80% of individuals left (76 out of 95, 1 control) to have at least 1 of coverage and ended up keeping obtaining X sites. We only kept one read per Stacks for Stacks containg up to two loci. We excluded all other Stacks.

```
python ~/repos/scripts/stoneflies_GBS1/filter_stacks_vcf.py SNPcall_default/populations.snps.vcf  output_snpfiles_all -mincov 1   -min_nind_with_mincov 76 
```

That outputted 3548 SNPs and a few statistics in the file stats_per_ind.txt,  showing that 2 individuals + the blank control (GBSNEG1) had low average coverage and less than 1000 SNPs. Those were removed and the filtering reran.	

```
sample  avg_depth_GENOT_sites   n_GENOT_sites   n_missing_sites
L700_V09        6.0582781457    755     2793
L700_F10        3.0     1       3547
GBSNEG1 0       0       3548

```

We excluded those individuals and created a second dataset.

```
python ~/repos/scripts/stoneflies_GBS1/filter_stacks_vcf.py SNPcall_default/populations.snps.vcf  output_snpfiles_restricted -mincov 1   -min_nind_with_mincov 74 -blacklistsamples bad_inds.txt
```

that now contained 3763 SNPs. It should be noted that the average coverage per ind is very high. For the same amount of sequencing, it is possible to use more individuals or to use enzymes that will lead to more sites.

## Genepop and structure file 


I then make files in the genepop format


```
perl ~/repos/scripts/stoneflies_GBS1/vcf2genepop.pl vcf=output_snpfiles_restricted/filtered.vcf -pops=""L550,L700,L850,S600,S800"" >  output_snpfiles_restricted/filtered.gen

```
We also created a structure input file

```
python ~/repos/scripts/stoneflies_GBS1/vcf2structure.py output_snpfiles_restricted/filtered.vcf output_snpfiles_restricted/filtered.str
```


## Summary 

output_snpfiles_restricted : 3763 sites covered for at least 80 % of 93 individuals. We kept mmaximum 1 site in each 100bp fragment (i.e. each stacks) while excluding fragments with more than 2 sites (i.e. likely to be repeats).