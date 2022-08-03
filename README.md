# WilsonGenAI
Protocol for classifying ATP7B gene linked variants causing Wilson's Disease using two AI models.


## About
WilSonGenAI has been created to facilitate the classification of variants of uncertain significance. We trained two models on a one-of-its kind database comprising of gold-standard variants classified by ACMG/AMP Guidelines.  The two algorithms used are TabNet, a deep learning algorithm designed particularly for tabular data, and XGBoost, since traditionally tree ensemble models are relied on for tabular data classification. This README document illustrates the installation, preprocessing and procedure for running both the models.


## Installation
Download and install the latest version of [Anaconda](https://docs.anaconda.com/anaconda/install/linux/). Additionally, download and install [ANNOVAR](https://annovar.openbioinformatics.org/en/latest/user-guide/download/) and [Loftee](https://github.com/konradjk/loftee) for hg38.


Create and activate the wilsongen-ai conda environment:
```
conda env create -f wilsongen-ai.yml
conda activate wilsongen-ai
```

Prepare your VCF file as shown in the sample.vcf file. Please do not Add "chr" in front of the chromosome number.

Run Annovar on the VCF using the following commands:
```
convert2annovar.pl --format vcf4 sample.vcf --outfile res.avinput --includeinfo --withzyg

table_annovar.pl res.avinput PATH_TO/humandb --buildver hg38 --outfile res --protocol refGene,gnomad30_genome,esp6500siv2_all,gme,AFR.sites.2015_08,AMR.sites.2015_08,ALL.sites.2015_08,EAS.sites.2015_08,EUR.sites.2015_08,SAS.sites.2015_08,mcap,revel,avsnp150,clinvar_20210501,dbnsfp42a --operation g,f,f,f,f,f,f,f,f,f,f,f,f,f,f --nastring . --otherinfo

awk -F"\t" 'OFS="\t" {print $157":"$158":"$160":"$161, $0}' res.hg38_multianno.txt | sed 's/^chr//g' - | sed 's/Otherinfo4:Otherinfo5:Otherinfo7:Otherinfo8/ID/g' > multianno_processed
```

Next, sort your VCF and run Loftee using the following command and prepare the output file as follows:
```
vcf-sort sample.vcf > sorted.vcf

nohup vep --format vcf --species homo_sapiens --merged --dir_plugin PATH_TO/vep_data/Plugins --dir_cache PATH_TO/vep_data/ --assembly GRCh38 --cache --offline --sift b --ccds --uniprot --hgvs --symbol --numbers --domains --gene_phenotype --canonical --protein --biotype --uniprot --tsl --pubmed --variant_class --shift_hgvs 1 --check_existing --total_length --allele_number --no_escape --xref_refseq --failed 1 --vcf --minimal --flag_pick_allele --pick_order canonical,tsl,biotype,rank,ccds,length --polyphen b --af --af_1kg --af_esp --af_gnomad --max_af --mane --appris --regulatory --exclude_predicted --fasta PATH_TO/vep_data/homo_sapiens_merged/106_GRCh38/Homo_sapiens.GRCh38.dna.toplevel.fa --input_file sorted.vcf --output_file lof_sorted.vcf --plugin LoF,loftee_path:PATH_TO/vep_data/Plugins,human_ancestor_fa:PATH_TO/vep_data/loftee_grch38/human_ancestor.fa.gz,conservation_file:PATH_TO/vep_data/loftee_grch38/loftee.sql,gerp_bigwig:PATH_TO/vep_data/loftee_grch38/gerp_conservation_scores.homo_sapiens.GRCh38.bw

awk -F"\t" 'OFS="\t" {print $1":"$2":"$4":"$5, $8}' lof_sorted.vcf | awk -F['\t,'] 'OFS="\t" { for(i=2;i<=NF;i++) print $1, $i}' - | sed 's/|/\t/g' - | awk -F"\t" 'OFS="\t" {if($29 == "YES" && $80 == "HC" && $30 ~ "NM_") print $1,"1"}' - | awk 'BEGIN{print "ID\tLoF_HC_Canonical"}1' - | sed 's/^chr//g' - > op_lof
```

Place the resulting files multianno_processed and op_lof in the preprocessing folder. Next, create a file called "op_outcome" and place it in the same folder. This file should contain two columns, namely "ID" containing your variant in "Chr:Start:Ref"Alt" format, and "Outcome", describing whether the variant is Pathogenic (1) or Benign (0). A sample op_outcome file is attached.

Now run the python script preprocessing_pipeline.py, using the command:
```
python3 preprocessing_pipeline.py.
```
This will result in an output file called pipeline.csv. It can now be used as the input for both the models.


## Creating the Model
The TabNet model can be run using the script tabnet.py, and the XGBoost model using xg_boost.py in the tabnet and xgboost folders respectively.

## Predictions
Predictions can be made using our model on the user data after processing the VCF into pipelie.py as discussed above, and leaving the "Outcome" column blank. The script predict_tabnet.py can be used to run TabNet and predict_xg_boost.py to run XGBoost to obtain predictions rerspectively. 
