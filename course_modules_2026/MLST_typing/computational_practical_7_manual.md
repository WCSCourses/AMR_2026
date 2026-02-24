# Computational Practical 7: Multilocus sequence typing (MLST) and cgMLST prediction from bacterial genomes



## Table of contents

1.	[Introduction](#intro)
2.	[Expected learning outcomes](#outcomes)
3.	[Genomes for MLST and cgMLST analysis](#genomes)
4.	[MLST prediction using mlst-check](#MLST)
5.	[cgMLST prediction using chewBBACA](#cgMLST)
6.	[MLST and cgMLST comparative visualisation](#comparative)
7.	[Q&A](#q&a)



## 1. Introduction <a name="intro"></a>

The ability to distinguish among strains of clinically relevant pathogens enables: (1) identification of circulating genotypes that may differ by features of virulence or antimicrobial resistance (AMR), (2) identification of outbreaks events, and (3) ability to track the source and spread of infections. Multilocus sequence typing (MLST) is a widely used molecular typing tool that is portable, universally adapted and provides a standardised genotypic approach that examines the nucleotide sequences of typically seven loci that encode house-keeping genes ([Maiden. 2006](https://www.annualreviews.org/content/journals/10.1146/annurev.micro.59.030804.121325)). Hundreds of MLST schemes for different pathogens have been made publicly available to ensure that a uniform nomenclature for typing is accessible through sites such as [PubMLST]( https://pubmlst.org/). 

Current advancements and cost-efficiency in generating high-throughput whole-genome sequencing data has led to the expansion of some MLST schemes to core-genome MLST (cgMLST) schemes that include >1000 genes to create sequence types that provide increased resolution for clonal populations of bacteria ([de Been et al. 2015](https://journals.asm.org/doi/full/10.1128/jcm.01946-15)). Following the increase in the number of whole-genomes, PubMLST is increasingly including whole-genome sequences accessed through BIGSdb ([Jolley and Maiden. 2010](https://link.springer.com/article/10.1186/1471-2105-11-595)).

Several bioinformatics tools that identify MLST sequence types directly from the genome have been developed. For example, [mlst-check](https://github.com/sanger-pathogens/mlst_check) enables the identification of sequence types by first consolidating multiple MLST databases from various sources into one database that can be stored locally and kept up-to-date. FASTA files can then be used as input to get sequence types from a corresponding pathogen specific database as well as the genomic sequences for each allele. Similarly, tools for cgMLST have been implemented. An example is [chewBBACA](https://github.com/B-UMMI/chewBBACA) a software used to create and evaluate cgMLST or whole-genome MLST (wgMLST) schema. chewBBACA creates schemas and allele calls on whole genomes resulting from de novo assemblers. For this practical session, [GrapeTree](https://github.com/achtman-lab/GrapeTree) will be used for visualisation.  



## 2. Expected learning outcomes <a name="outcomes"></a>

At the end of this practical session, one should be able to:  
  *	Use command-line tools such as mlst-check and chewBBACA to identify isolates’ MLST and cgMLST profiles or sequence types;
  *	Use tools such as PHYLOViZ and GrapeTree to visualise MLST and cgMLST results, respectively;  
  * Compare and contrast the two methods and when each is useful  



## 3. Genomes for MLST and cgMLST analysis <a name="genomes"></a>

### Data preparation

Navigate to your home directory and create a new mlst directory.

```
cd
mkdir mlst
```

`cd` inside the mlst directory then copy in the directory called mlst_genomes from /home/data/mlst_genomes into your current working directory (i.e. mlst):

```
cd mlst
cp -r /home/data/mlst_genomes .
```


## 4. MLST prediction using mlst-check <a name="MLST"></a>

## mlst-check installation using conda

To install mlst-check, first install or update conda. Then install bioconda and mlst-check.

```
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
conda install perl-bio-mlst-check
```

Set the directory where you would like to store the MLST databases.

```
export MLST_DATABASES=/home/mlst
```


Download the most recent copy of MLST databases

```
download_mlst_databases 
```


You can view the list contained in the MLST databases for your other pathogens of interest

```
get_sequence_type -a
```


Now you can run MLST typing for Klebsiella pneumoniae. In the below code, `-s` specifies the database you want to search against


```
get_sequence_type -s "Klebsiella pneumoniae species complex" /home/mlst/data/mlst_genomes/*.fasta
```

You can add multiple options to the line of code. E.g., `-c` outputs a FASTA file with concatenated alleles for building a phylogenetic tree. Similarly, `-y` outputs a phylip file with concatenated alleles for the same purpose.

```
get_sequence_type -c -s "Klebsiella pneumoniae species complex" /home/mlst/data/mlst_genomes/*.fasta
```

mlst-check outputs a 'mlst_results.allele.csv' that contains the sequence type number of each input FASTA file and the corresponding allele numbers for each gene in the scheme. 

Note:
It is important to submit unknown alleles to PubMLST for identification and allele number assignment. Therefore, if one of the alleles is unknown in the database, mlst-check assigns it a 'U' flag, and the third column will describe it as 'Unknown'. If the combination of allele numbers is new, it will be flagged as 'Novel'.

The 'mlst_results.genomic.csv' spreadsheet is similar to the mlst_results.allele.csv spreadsheet, but it gives the full sequences of each allele instead of the allele number. These can then be used for submission to PubMLST in the case of unknown or novel alleles.


## 5. cgMLST prediction using chewBBACA <a name="cgMLST"></a>

## chewBBACA installation

Install chewbbaca and activate environment


```
conda create -n chewbbaca -c bioconda -c conda-forge chewbbaca grapetree
conda activate chewbbaca
```


Retrieve K. pneumoniae cgMLST schema form ridom seqsphere

```
curl -o k_pneumoniae_cgMLST_alleles.zip https://www.cgmlst.org/ncs/schema/Kpneumoniae1936/alleles/
unzip k_pneumoniae_cgMLST_alleles.zip -d k_pneumoniae_cgMLST
```


PrepExternalSchema - Adapt the ridom seqsphere schema to be used with chewBBACA

```
chewBBACA.py PrepExternalSchema -g k_pneumoniae_cgMLST -o k_pneumoniae_schema --cpu 8
```


AlleleCall - Determine the allelic profiles of a set of genomes

```
chewBBACA.py AlleleCall -i mlst_genomes -g k_pneumoniae_schema -o allele_calls --cpu 8
```


SchemaEvaluator - Build an interactive report for schema evaluation

```
chewBBACA.py SchemaEvaluator -g k_pneumoniae_schema -o SchemaEvaluator --cpu 8
```


AlleleCallEvaluator - Build an interactive report for allele calling results evaluation

```
chewBBACA.py AlleleCallEvaluator -i allele_calls -g k_pneumoniae_schema -o AlleleCallEvaluator --cpu 8 
```


ExtractCgMLST - Determine the set of loci that constitute the core genome

```
chewBBACA.py ExtractCgMLST -i allele_calls/results_alleles.tsv -o cgmlst_matrix
```


Open GrapeTree and follow the below steps

```
grapetree
```


Steps for GrapeTree visualisation:

## Load cgMLST file
* Click “Load Data”  
* Select cgMLST95.tsv inside the cgmlst_matrix directory  
* Select MSTreeV2 under the method drop-down arrow  

## Tree Layout


## Node Style
* Check Show Labels  
* Colour By: ID  
* Label Font Size: 11  
* Node Size: 500  
* Kurtosis (%): 30  


## Branch Style
* Check Show Labels  
* Font Size: 17  
* Scaling (%): 53  
* Check Log Scale  



## 6. MLST and cgMLST comparative visualisation <a name="comparative"></a>

TBC - Discussion


## 7. Q&A <a name="q&a"></a>











