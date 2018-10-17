## SNPcalling.md


For the SNP calling, I used STACKS [version 2.0b](http://catchenlab.life.illinois.edu/stacks/)

I followed a DENOVO procedure where I called loci in the absence of reference genome. The general procedure is outline in the stacks on the [software website](http://catchenlab.life.illinois.edu/stacks/manual/). I started by a quick quality control step looking at our reads using fastQC and did not notice any contamination.



## Process radtags (STACKS first step) in 2 batches

As there are 2 lanes containing 2 barcodes, I ran process_radtags twice.

First I create [snp_calling_files/barcodes1.txt](snp_calling_files/barcodes1.txt) and [snp_calling_files/barcodes2.txt](snp_calling_files/barcodes2.txt)

Then I call process radtags which will separate the reads per individual with barcode rescue (allowing 1 mismatch in the barcode). It is important to have one folder (i.e. here raw) that contains all the files with reads(i.e. only USDA_S1_L001_R1_001_trimmed97clean.fastq) and nothing else.


```
#1st lane

 process_radtags -i gzfastq -p raw1/ -o ./samples1/ -b barcodes1.txt -e pstI  -c -q --inline_null -r

274117278 total sequences
 11140915 ambiguous barcode drops (4.1%)
   200341 low quality read drops (0.1%)
  1365091 ambiguous RAD-Tag drops (0.5%)
261410931 retained reads (95.4%)

#2 lane
 process_radtags -i gzfastq -p raw2/ -o ./samples2/ -b barcodes2.txt -e pstI  -c -q --inline_null -r

299955078 total sequences
  6169015 ambiguous barcode drops (2.1%)
   377174 low quality read drops (0.1%)
   680267 ambiguous RAD-Tag drops (0.2%)
292728622 retained reads (97.6%)
```
At this stage, we combined individuals across the two lanes.

4 individuals, L850_V07, L850_V08, S680_D and L550_V02 ( L550_V02.2 in the second lane) are sequenced across both lanes. The control GBSNEG1 is also in both lanes! We quickly combined them before grouping all the samples into one folder and finishing ther SNP calling using combine_process.sh.



We also ran FastQC on this. As expected, barcodes were gone and the enzyme is left in. That is a good checkpoint to have a look at overrepresented sequences and remove contamination.




## STACKS pipeline

I create a [population map](snp_calling_files/popmap.txt) that is required by STACKS, there is no population information actually contained in it. It contaisn all the samples from both lanes. Some individuals will be dropped later if thee result of the sequencing is poor.

I  call SNPs denovo using [ustacks.sh](ustacks.sh) followed by [fromcstackstopopulations.sh](fromcstackstopopulations.sh).

## Post-STACKS Filtering

Out of STACKS we obtained 321 250 SNPs.
```
cat SNPcall_default/populations.snps.vcf | grep -v "#" | wc -l
#321250
```
 We had not filtered those for coverage across individuals or coverage within individuals.

Furthermore, one could see that there are many stacks with multiple SNPs within a 100bp, which can be an indication of repeats merged as a single stacks:

```
# count number of SNP per stacks in bash
cat   nsnpsperstacks.txt" | grep -v "^#" |  cut -f 1 | uniq -c | sort | sed  -E 's/^\s+//g' > nsnpsperstacks.txt
##  in R
data<-read.table("nsnpsperstacks.txt",h=F)
	table(data[,1])

    1     2     3     4     5     6     7     8     9    10    11    12    13
64892 31477 15915  9338  5670  3667  2376  1604   985   602   386   235   162
   14    15    16    17    18    19    20    21    22    23    24    26
   88    64    43    33    11    11     7     7     7     3     1     2
```


We then ran [filter_stacks_vcf.py](filter_stacks_vcf.py) requiring at least 80% of individuals left (152 out of 179) to have at least 1 of coverage and. We only kept one read per Stacks for Stacks containg up to two loci. We excluded all other Stacks.

```
python ~/repos/scripts/stoneflies_GBS1/filter_stacks_vcf.py SNPcall_default/populations.snps.vcf  output_snpfiles_all -mincov 1   -min_nind_with_mincov 152 
```

That outputted 2060 SNPs and a few statistics in the file stats_per_ind.txt/ This number is low. We quickly looked at the distribution of SNPs per individuals. We found that some individuals had very few SNPs:
```
nsnpsperinds<-read.table(stats_per_ind.txt",,h=T)
quantile(nsnpsperinds[,3],seq(0,1,0.05))
    0%     5%    10%    15%    20%    25%    30%    35%    40%    45%    50%
   0.0  969.4 1726.8 1892.7 1925.0 1947.5 1962.4 1968.0 1971.2 1975.1 1979.0
   55%    60%    65%    70%    75%    80%    85%    90%    95%   100%
1981.0 1985.0 1987.7 1991.6 1994.0 1996.4 1999.0 2001.2 2006.1 2018.0

```

Those low individuals were:

```
sample	avg_depth_GENOT_sites	n_GENOT_sites	n_missing_sites
L700_F10	0	0	2060
L1200_V09	5.46341463415	123	1937
L700_F06	5.5119047619	252	1808
S390_F08	5.79949874687	399	1661
L700_V09	5.8056206089	427	1633
L435_F04	26.5320987654	810	1250
L435_F13	33.2218181818	825	1235
L435_F02	18.2620772947	828	1232
L700_V11	5.96860986547	892	1168
L1200_V03	6.3609406953	978	1082
S800_F02	7.09170731707	1025	1035
L435_F07	9.00522778193	1339	721
S390_F07	9.15603799186	1474	586
```

We excluded those 13 individuals and created a second dataset retaining sites covered for at least 133 out of 166 inds (80%). We also keep 1 SNP per STACKS for STACKS with up to 3 SNPs.

```
python ~/repos/scripts/stoneflies_GBS1/filter_stacks_vcf.py SNPcall_default/populations.snps.vcf  output_snpfiles_restricted -mincov 1   -min_nind_with_mincov 133 -blacklistsamples bad_inds.txt -max_nsnps_per_valid_stacks 3
```

that now contained 3763 SNPs. It should be noted that the average coverage per ind is very high. For the same amount of sequencing, it is possible to use more individuals or to use enzymes that will lead to more sites.

## Genepop and structure file 


I then make files in the genepop format

```
perl ~/repos/scripts/stoneflies_GBS1/vcf2genepop.pl vcf=output_snpfiles_restricted/filtered.vcf -pops="L1200,L320,L435,L550,L700,L850,S100,S110,S390,S480,S600,S680,S800,S880
" >  output_snpfiles_restricted/filtered.gen


```
We also created a structure input file

```
python ~/repos/scripts/stoneflies_GBS1/vcf2structure.py output_snpfiles_restricted/filtered.vcf output_snpfiles_restricted/filtered.str
```
The arlequin format was also created using GENEPOP conversion tool online:

[http://genepop.curtin.edu.au/genepop_op7.html](http://genepop.curtin.edu.au/genepop_op7.html)

## Summary 

output_snpfiles_restricted :  4633 sites covered for at least 80 % of 166 individuals. We kept maximum 1 site in each 100bp fragment (i.e. each stacks) while excluding fragments with more than 3 sites (i.e. likely to be repeats).
