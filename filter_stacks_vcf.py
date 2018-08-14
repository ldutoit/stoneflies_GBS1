#!/usr/bin/env python2
#import modules
from __future__ import print_function
import argparse
import sys
import os
#third parties module
import vcf


#Simple argument parser to use as a base when constructing other. Here are two guides:
#http://www.pythonforbeginners.com/argparse/argparse-tutorial
#https://pymotw.com/2/argparse/


#FUNCTIONS



def errprint(*args, **kwargs):
    ''' print to stderr not stdout'''
    print(*args, file=sys.stderr, **kwargs)

#parser
parser = argparse.ArgumentParser() # add the parser
parser.add_argument("input",help="VCF file") # add the parser
parser.add_argument("outputfolder", help=" output folder",type=str)
parser.add_argument("-mincov", help="Minimum coverage for a genotype to be considered", type=int,default=1)
parser.add_argument("-min_nind_with_mincov",help="Minimum number of individuas that have at least *mincov*",  type=int,default=1) 
parser.add_argument("-max_nsnps_per_valid_stacks",help=" We exclude al SNP from a stacks wity >max_nsnps_per_valid_stacks SNPs. We always keep maximum 1 SNP per stacks ", type=int,default=2) 
parser.add_argument("-blacklistsamples",help="a path to a file with samples to exclude, 1 per line",default=None,action="store")
args = parser.parse_args()

#Functions
def checkSnp_Cov(input_vcf,record,mincov=0,maxcov=100000000,inds="all",nalleles=[1,2,3,4],nb_ind_with_min_cov="all",snps=False):
	"""Check if a site respect coverage conditions for selected individuals. Return TRUE/False. In order to be true if any coverage is specified the individual has to be called

		input_vcf # an object of class vcf.parser.Reader from which the recorded is extracted
		record #  an object of class  vcf.model._Record
		mincov # the coverage minimum the site should have for the for every  individual sppecified with ind
		maxcov # the coverage maximum the site should have for the for every  individual sppecified with ind
		inds # a list of selected individuals. if inds="all" or ["alls"] consider every sample
		called	#all individuals need an assigned genotype
		nalleles (list) # a list of integer of alleles tolerated for the check. for example [1] is for monomorphic snp, [1,2] include snps and [1,2,3] include triallele snps
		nb_ind_with_min_cov="all" # the number of individuals that need at least mincov to call the site. If "all", it becomes the same as ind, If "all_vcf", it becomes all the individuals in the vcf  Not applicable to maxcov!
		>>> input_vcf=vcf.Reader(fsock=None, filename=sample_vcfgz, compressed=True, prepend_chr="False", strict_whitespace=False)
		>>> record=input_vcf.next()
		>>> checkSnp_Cov(input_vcf,record)###check function
		True
		>>> checkSnp_Cov(input_vcf,record,5)#check mincov
		False
		>>> checkSnp_Cov(input_vcf,record,maxcov=12)# checkmaxcov
		True
		>>> checkSnp_Cov(input_vcf,record,maxcov=5)#check maxcov
		False
		>>> checkSnp_Cov(input_vcf,record,maxcov=10,inds=['OC_3_M','OC_4_M','OC_5_M'])#check inds
		True
		>>> checkSnp_Cov(input_vcf,record,5,nb_ind_with_min_cov=3)
		True
	"""
	###Checks
	#print "in checkSnp_Cov nb_ind_with_min_cov :",nb_ind_with_min_cov, " inds", inds
	#pdb.set_trace()
	#print "check", input_vcf.filename
	if type(input_vcf)!=vcf.parser.Reader: raise Exception ("input_vcf must be a parser.Reader object")
	if type(record)!=vcf.model._Record: raise Exception ("record must be a  vcf.model._Record object")
	#function
	if inds=="all" or inds==["all"]:inds=input_vcf.samples# if no list of individuals, us all individuals 
	if nb_ind_with_min_cov=="all" : nb_ind_with_min_cov=len(inds)# if we want all the individuals with at least X coverage
	if nb_ind_with_min_cov=="all_vcf" : 
		nb_ind_with_min_cov=len(input_vcf.samples)# if we want all the individuals with at least X coverage
		inds=input_vcf.samples
	#print "in checkSnp_Cov nb_ind_with_min_cov :",nb_ind_with_min_cov, " inds", inds
	if not len(record.alleles) in nalleles: return False # check the number of alleles
	#print snps
	# check all inds in parameters are in the vcf
	if not all([ind in input_vcf.samples  for ind in inds]): 
		#print set(inds).difference(set(input_vcf.samples)), "are in the sample but not in the vcf"
		raise Exception
	if snps==True: 
		if not any([ind.is_het for ind in record.samples if ind.sample in inds])  : 
			return False # not an heterozygous site 
	if "DP" in record.FORMAT:
		#print len([ind for  ind in record.samples if ind.sample in  inds]),"inds"
		if mincov==0 :# we want to avoid to take in the None that are 0 and prevent us to use the condition
			cond=all([ ind["DP"]<=maxcov for ind in record.samples if ind["DP"]!=None and (ind.sample in inds) ]) 
		else: # we need to take into account the none cause they mean DP=0 and cond=False
			#print [mincov<= ind["DP"]<=maxcov and ind.called==True for ind in record.samples  if (ind.sample in inds)].count(True)   
			#pdb.set_trace()
			cond=nb_ind_with_min_cov<=[mincov<= ind["DP"]<=maxcov and ind.called==True for ind in record.samples  if (ind.sample in inds)].count(True)   
			#print "check_cov", len(inds)
	else:
		cond=False#raise Exception ("format do not include DP for",record.POS,record.CHROM)
	#check that this one is variable!
	#if cond==True: print [sample["DP"] for sample in record.samples if (sample.sample in inds)]
	#if cond==True: assert 8<=[5<= ind["DP"]<=maxcov and ind.called==True for ind in record.samples  if (ind.sample in inds)].count(True)," very ugly.... just to check that 1 individual is okay for 7 reads and that I check that all along"
	return cond

## program
errprint("Start")

#print args


# check inputs, and print it as a list file

if not os.path.exists(args.outputfolder): os.system("mkdir -p "+args.outputfolder)

### get the list of individuals to exclude

vcffile =args.input

# main list
print("check site for coverage across individuals")
input_vcf=vcf.Reader(fsock=None, filename=vcffile, compressed=False, prepend_chr="False", strict_whitespace=False)#open the vcf parser
print (len(input_vcf.samples), "originally in vcf")
#get the individual sorted
if args.blacklistsamples:
	blacklist = set([line.strip() for line in open(args.blacklistsamples)])
else:
	blacklist=[]
inds = set(input_vcf.samples).difference(blacklist) 
print (blacklist)
 
print(inds)
#filtering site by site

list_sites= []
nsites_per_stacks = {} # to know the number of snp per stacks
i=0
for site in input_vcf:
	i+=1
	if i%1000==0: print (i,"sites processed")	
	cond =  checkSnp_Cov(input_vcf,site,mincov=args.mincov,maxcov=100000000,inds=inds,nalleles=[2],nb_ind_with_min_cov=args.min_nind_with_mincov,snps=False)
	#print (cond)
	if cond:
		if site.CHROM in nsites_per_stacks.keys():
			nsites_per_stacks[site.CHROM]+=1
		else:
			nsites_per_stacks[site.CHROM]=1
		list_sites.append([site.CHROM,site.POS])

# keep 1 site per lcoi for all loci with < max_nsnps_per_valid_stacks
print("checknumber of sites per sequences:")

final_list_sites = []
for site in list_sites:
	if nsites_per_stacks[site[0]] <= args.max_nsnps_per_valid_stacks: # if that stacks only has one site
		final_list_sites.append(site)
		nsites_per_stacks[site[0]] = 10e6 # indirect way of making sure we oonly ger this one site and not the other sites from the same stacks because 
print(len(list_sites),"sites before check",len(final_list_sites),"sites left after removing stacks with more than",args.max_nsnps_per_valid_stacks,"variable sites")


#Now we know all the condistion

print ("outputting sites to vcf")

nsnps=0
output=open(args.outputfolder+"/filtered.vcf","w")
with open(vcffile) as f:
	for line in f:
		if line.startswith('##'):
			output.write(line)
		elif line.startswith("#C"):
			#locate the black sample
			positionstokeep = [index for index,item in enumerate(line.split()) if item not in blacklist]
			print (positionstokeep)
			newline= "\t".join([item for index,item in enumerate(line.split()) if index in positionstokeep])+"\n"
			output.write(newline)
		elif ["chr"+line.split()[0],int(line.split()[1])] in final_list_sites:
			newline= "\t".join([item for index,item in enumerate(line.split()) if index in positionstokeep])+"\n"
			output.write(newline)
			nsnps+=1
		#else: 
		#	print (["chr"+line.split()[0],line.split()[1]])
output.close()



print ("stats per ind and site")



input_vcf=vcf.Reader(fsock=None, filename=args.outputfolder+"/filtered.vcf", compressed=False, prepend_chr="False", strict_whitespace=False)#open the vcf parser
nsites = 0
cov_dict = {ind:[] for ind in input_vcf.samples } # coverage dictionary to know coverage across samples
for site in input_vcf:
	nsites +=1
	assert site.heterozygosity>=0
	for ind_info in site.samples:
		if ind_info["GT"] !="./.":
			cov_dict[ind_info.sample].append(ind_info["DP"])
		
# print out the file ind by ind

output=open(args.outputfolder+"/stats_per_ind.txt","w")
output.write("\t".join(["sample","avg_depth_GENOT_sites","n_GENOT_sites","n_missing_sites"])+"\n")
for ind in input_vcf.samples:
	#avg_depth_GENOT_sites avoid division by zero
	if sum(cov_dict[ind]) == 0: 
		avg_depth_GENOT_sites = 0
	else:
		avg_depth_GENOT_sites = sum(cov_dict[ind])/float(len(cov_dict[ind]))
	output.write("\t".join([str(x) for x in [ind,avg_depth_GENOT_sites,len(cov_dict[ind]),nsites-len(cov_dict[ind])]])+"\n")

output.close()

