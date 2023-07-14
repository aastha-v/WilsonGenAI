# WilsonGenAI
Protocol for classifying ATP7B gene linked variants causing Wilson's Disease using two AI models.


## About
WilSonGenAI has been created to facilitate the classification of variants of uncertain significance. We trained two models on a one-of-its kind database comprising of gold-standard variants classified by ACMG/AMP Guidelines.  The two algorithms used are TabNet, a deep learning algorithm designed particularly for tabular data, and XGBoost, since traditionally tree ensemble models are relied on for tabular data classification. This README document illustrates the installation, preprocessing and procedure for running both the models.


## Installation
Download and install the latest version of [Anaconda](https://docs.anaconda.com/anaconda/install/linux/). Next, download and install [ANNOVAR](https://annovar.openbioinformatics.org/en/latest/user-guide/download/) and [Loftee](https://github.com/konradjk/loftee) for hg38 through this [link](https://clingen.igib.res.in/ML_install.tar.gz). The unzipped folder will install both the tools through the instructions given below.
**Around 100GB free space would be required to download the file, and around 400GB would be needed for the unzipped folder.**
Note: Our pipeline has been standardized on Ubuntu 18.04.6 LTS. 

Unzip the folder and install the tools using the following commands:
```
tar -xvzf ML_install.tar.gz
cd ML_install
bash INSTALL.sh
```

Next, place this repository inside the unzipped folder:
```
git clone https://github.com/aastha-v/WilsonGenAI.git
```

Now create and activate the wilsongen-ai conda environment:
```
conda env create -f WilsonGenAI/wilsongenai.yml
conda activate wilsongenai
```

## Preprocessing
Prepare your VCF file as shown in the WilsonGenAI/input_folder/sample.vcf file and op_outcome file as shown in WilsonGenAI/input_folder/op_outcome. Please do not Add "chr" in front of the chromosome number. To run your own file, place both your vcf and op_outcome files in WilsonGenAI/input_folder.
To process the VCF into the appropriate input format for either creating or using the pre-generated model, run the following command. This will generate a file called 'pipeline.csv', and place it in both the WilsonGenAI/tabnet and WilsonGenAI/xgboost folders. 
```
bash WilsonGenAI/scripts/preprocessing.sh
```
In case the command does not work, please try using absolute paths in the vep command in preprocessing.sh. If that does not work, or if the VEP plugin does not work, please run the following:
```
bash WilsonGenAI/troubeshooting.sh
```


To process a VCF with a different name than "sample.vcf", modify the "input_filename" in the preprocessing.sh script and then run it:
```
input_filename='myvcf.vcf'
```

## Using Pre-Generated Models
To generate predictions using our models for both tabnet and xgboost, run the following commands. Each command will generate a file called predictions_xgboost and predictions_tabnet in the xgboost and tabnet folders respectively. The "Prediction" column bears the final predictions: '0' denotes Benign and '1' denotes Pathogenic.
```
python3 WilsonGenAI/xgboost/predict_xg_boost.py 
python3 WilsonGenAI/tabnet/predict_tabnet.py 
```

## Generating a Model
In order to train a new model based on ones own data, the following commands can be run. These will generate new models named xg_boost_model.txt and tabnet.model.zip respectively.
```
python3 WilsonGenAI/xgboost/xg_boost.py
python3 WilsonGenAI/tabnet/tabnet.py
```

The folders in this repository bear output files for both models generated for the sample.vcf file for reference.
