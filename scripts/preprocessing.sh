#!/bin/bash

#export current working directory
export cwd=$(pwd)

#declare all working files/dirs
input_filename='sample.vcf'
preprocessing_foldername=$cwd/WilsonGenAI/preprocessing/


#export lof paths
export LOF="$cwd/loftee"
export VEP_PATH=$LOF/vep
export VEP_DATA=$LOF/vep_data
export VER=106
export PERL5LIB=$VEP_PATH:$PERL5LIB
export PATH=$VEP_PATH/htslib:$PATH
export PERL5LIB=$VEP_PATH
export PATH="$VEP_PATH/htslib:$PATH"
#export PATH=$HOME/vep/samtools/bin:$PATH
export PERL_BASE="$LOF/perl"
export PERL5LIB="$PERL_BASE/perl-5.24.1/lib/perl5:$PERL_BASE/perl-5.24.1/lib/perl5/x86_64-linux:$PERL5LIB"
export PATH="$PERL_BASE/perl-5.24.1/bin:$PATH"
export PATH="$VEP_PATH:$PATH"
export KENT_SRC=$LOF/kent-335_base/src
export MACHTYPE=$(uname -m)
export CFLAGS="-fPIC"
export MYSQLINC='mysql_config --include | sed -e 's/^-I//g''
export MYSQLLIBS='mysql_config --libs'
export PERL5LIB=$PERL5LIB:$PERL_BASE/cpanm/lib/perl5
#ln -s $KENT_SRC/lib/x86_64/* $KENT_SRC/lib/


#preprocessing
cd $preprocessing_foldername
rm *
cp ../input_folder/$input_filename $preprocessing_foldername
cp ../input_folder/op_outcome $preprocessing_foldername
vcf-sort $input_filename > sorted.vcf
echo "File Sorted"


#run lof command
nohup vep --format vcf --species homo_sapiens --merged --dir_plugin $VEP_DATA/Plugins \
--dir_cache $VEP_DATA --assembly GRCh38 --cache --offline --sift b --ccds --uniprot --hgvs \
--symbol --numbers --domains --gene_phenotype --canonical --protein --biotype --uniprot --tsl --pubmed --variant_class --shift_hgvs 1 --check_existing --total_length --allele_number \
--no_escape --xref_refseq --failed 1 --vcf --minimal --flag_pick_allele --pick_order canonical,tsl,biotype,rank,ccds,length --polyphen b --af --af_1kg --af_esp --af_gnomad --max_af --mane \
--appris --regulatory --exclude_predicted --fasta $VEP_DATA/homo_sapiens_merged/106_GRCh38/Homo_sapiens.GRCh38.dna.toplevel.fa \
--plugin LoF,loftee_path:$VEP_DATA/Plugins,human_ancestor_fa:$VEP_DATA/loftee_grch38/human_ancestor.fa.gz,conservation_file:$VEP_DATA/loftee_grch38/loftee.sql,gerp_bigwig:$VEP_DATA/loftee_grch38/gerp_conservation_scores.homo_sapiens.GRCh38.bw \
--input_file sorted.vcf --output_file lof_sorted.vcf --force_overwrite


#create op_lof file
awk -F"\t" 'OFS="\t" {print $1":"$2":"$4":"$5, $8}' lof_sorted.vcf | awk -F['\t,'] 'OFS="\t" { for(i=2;i<=NF;i++) print $1, $i}' - | sed 's/|/\t/g' - | awk -F"\t" 'OFS="\t" {if($29 == "YES" && $80 == "HC" && $30 ~ "NM_") print $1,"1"}' - | awk 'BEGIN{print "ID\tLoF_HC_Canonical"}1' - | sed 's/^chr//g' - > op_lof


#copy vcf to annovar and change folder to there
cd $cwd/annovar
rm *
cp $preprocessing_foldername/$input_filename .
echo "VCF copied to annovar folder"


#run annovar
../WilsonGenAI/scripts/convert2annovar.pl --format vcf4 $input_filename --outfile res.avinput --includeinfo --withzyg

../WilsonGenAI/scripts/table_annovar.pl *.avinput ../humandb --buildver hg38 --outfile res \
--protocol refGene,gnomad30_genome,esp6500siv2_all,gme,AFR.sites.2015_08,AMR.sites.2015_08,ALL.sites.2015_08,EAS.sites.2015_08,EUR.sites.2015_08,SAS.sites.2015_08,mcap,revel,avsnp150,clinvar_20210501,dbnsfp42a \
--operation g,f,f,f,f,f,f,f,f,f,f,f,f,f,f --nastring . --otherinfo

awk -F"\t" 'OFS="\t" {print $157":"$158":"$160":"$161, $0}' *multianno.txt | sed 's/^chr//g' - | sed 's/Otherinfo4:Otherinfo5:Otherinfo7:Otherinfo8/ID/g' > multianno_processed

#copy all result files to the preprocessing folder
cp *multianno* $preprocessing_foldername


cd $preprocessing_foldername

python3 ../scripts/atp7b.py
