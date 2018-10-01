

#This quickly change pop label into a new vcf file from 14pop to 4 by replacing whatever comes before the "_ " according to the blow key

output =open("filtered4pops.vcf","w")

keypops = {"L1200_V01":"LV","L1200_V02":"LV","L1200_V04":"LV","L1200_V05":"LV","L1200_V06":"LV","L1200_V07":"LV","L1200_V08":"LV","L1200_V10":"LV","L1200_V11":"LV","L1200_V12":"LV","L320_F01":"LF","L320_F02":"LF","L320_F03":"LF","L320_F04":"LF","L320_F05":"LF","L435_F01":"LF","L435_F03":"LF","L435_F05":"LF","L435_F06":"LF","L435_F08":"LF","L435_F09":"LF","L435_F10":"LF","L435_F11":"LF","L435_F12":"LF","L435_F14":"LF","L435_F15":"LF","L435_F16":"LF","L435_F17":"LF","L550_F01":"LF","L550_F02":"LF","L550_F03":"LF","L550_F04":"LF","L550_F05":"LF","L550_F06":"LF","L550_F07":"LF","L550_F08":"LF","L550_F09":"LF","L550_F10":"LF","L550_V01":"LV","L550_V02":"LV","L700_F01":"LF","L700_F02":"LF","L700_F03":"LV","L700_F04":"LF","L700_F05":"LF","L700_F07":"LV","L700_F08":"LF","L700_F09":"LF","L700_F11":"LF","L700_F12":"LV","L700_F13":"LV","L700_V01":"LV","L700_V02":"LV","L700_V03":"LV","L700_V04":"LV","L700_V05":"LV","L700_V06":"LV","L700_V07":"LV","L700_V08":"LV","L700_V10":"LV","L700_V12":"LV","L700_V13":"LV","L700_V14":"LV","L700_V15":"LV","L700_V16":"LV","L850_F01":"LF","L850_F02":"LF","L850_V01":"LV","L850_V02":"LV","L850_V03":"LV","L850_V04":"LV","L850_V05":"LV","L850_V06":"LV","L850_V09":"LV","L850_V10":"LV","L850_V11":"LV","L850_V12":"LV","L850_V13":"LV","S1000_V01":"SV","S1000_V02":"SV","S1000_V03":"SV","S1000_V04":"SV","S1000_V05":"SV","S1000_V06":"SV","S1000_V07":"SV","S1000_V08":"SV","S1000_V09":"SV","S1000_V10":"SV","S1100_V01":"SV","S1100_V02":"SV","S1100_V03":"SV","S1100_V04":"SV","S1100_V05":"SV","S1100_V06":"SV","S1100_V07":"SV","S1100_V08":"SV","S1100_V09":"SV","S1100_V10":"SV","S390_F01":"SF","S390_F02":"SF","S390_F03":"SF","S390_F04":"SF","S390_F05":"SF","S390_F06":"SF","S390_F09":"SF","S390_F10":"SF","S480_F01":"SF","S480_F02":"SF","S480_F03":"SF","S480_F04":"SF","S480_F05":"SF","S480_F06":"SF","S480_F07":"SF","S480_F08":"SF","S480_F09":"SF","S480_F10":"SF","S600_F01":"SF","S600_F02":"SF","S600_F03":"SF","S600_F04":"SF","S600_F05":"SV","S600_F06":"SF","S600_F07":"SF","S600_F08":"SF","S600_V01":"SV","S680_F01":"SF","S680_F02":"SF","S680_F03":"SF","S680_F04":"SF","S680_F05":"SF","S680_F06":"SF","S680_F07":"SF","S680_F08":"SF","S680_F09":"SF","S680_F10":"SF","S680_V01":"SV","S680_V02":"SV","S680_V03":"SV","S680_V04":"SV","S680_V05":"SF","S680_V06":"SV","S680_V07":"SV","S680_V08":"SV","S680_V09":"SV","S680_V10":"SV","S800_F01":"SF","S800_F03":"SF","S800_V02":"SV","S800_V03":"SV","S800_V04":"SV","S800_V05":"SV","S800_V06":"SV","S800_V07":"SV","S880_V01":"SV","S880_V02":"SV","S880_V03":"SV","S880_V04":"SV","S880_V05":"SV","S880_V06":"SV","S880_V07":"SV","S880_V08":"SV","S880_V09":"SV","S880_V10":"SV","L850_V07":"LV","L850_V08":"LV","S680_D":"SF"}

#Lug Vestigial  (LV)
#Lug Full (LF)
#Six Vestigial (SV)
#Six Full (SF)

set(keypops.values())


with open("/Users/dutlu42p/repos/mahuika/stoneflies_GBS1/output_snpfiles_restricted/filtered.vcf") as f:
	for line in f:
		if not line.startswith("#CHROM"):
			output.write(line)
		else:
			info=line.split()
			for i,item in enumerate(info):
				if item in keypops.keys():
					info[i] = keypops[item]+"_"+"".join(item.split("_"))
					print item,info[i]					
				else:
					print "NOT",i
			print info
			output.write("\t".join(info)+"\n")

output.close()



import os
#Make .gen file
os.system("perl ~/repos/mahuika/stoneflies_GBS1/vcf2genepop.pl vcf=filtered4pops.vcf -pops='LV,LF,SV,SF' >  filtered4pops.gen")


#Make .str file
os.system("python ~/repos/mahuika/stoneflies_GBS1/vcf2structure.py filtered4pops.vcf filtered4pops.str")


# the structure file is not ordered by pops , we could order it by pops

data = {line.split("\t")[0]: line for line in open("filtered4pops.str")}

#write output
output = open("filtered4popsordered.str","w")
output.write(data["chr8_40"])
del data["chr8_40"]
for key in sorted(data.keys()):
	output.write(data[key])

output.close()
os.system("mv  filtered4popsordered.str filtered4pops.str")

#The arlequin format was also created using GENEPOP conversion tool online:
#http://genepop.curtin.edu.au/genepop_op7.html
