#/bin/sh
mkdir samples

#copy both lane in the common folder samples

cp samples1/* samples/
cp samples2/* samples/ 

#Recreate the one that were present in both lanes as the sum of the two

zcat samples1/S680_D.fq.gz samples2/S680_D.fq.gz | bgzip -c > temp
mv temp samples/S680_D.fq.gz 


zcat samples1/L850_V08.fq.gz samples2/L850_V08.fq.gz | bgzip -c > temp
mv temp samples/L850_V08.fq.gz 


zcat samples1/L850_V07.fq.gz samples2/L850_V07.fq.gz | bgzip -c > temp
mv temp samples/L850_V07.fq.gz 

zcat samples1/L550_V02.fq.gz samples2/L550_V02.2.fq.gz | bgzip -c > temp2
mv temp samples/L550_V02.fq.gz 

zcat samples1/GBSNEG1.fq.gz samples2/GBSNEG1.fq.gz | bgzip -c > temp
mv temp samples/GBSNEG1.fq.gz 


rm samples/L550_V02.2.fq.gz # this was copied at first but should not be here now!n