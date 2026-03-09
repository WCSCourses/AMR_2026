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

The ability to distinguish among strains of clinically relevant pathogens enables: (1) identification of circulating genotypes that may differ by features of virulence or antimicrobial resistance (AMR), (2) identification of outbreaks events, and (3) ability to track the source and spread of infections. Multilocus sequence typing (MLST) is a widely used molecular typing tool that is portable, universally adapted and provides a standardised genotypic approach that examines the nucleotide sequences of typically seven loci that encode house-keeping genes ([Maiden. 2006](https://www.annualreviews.org/content/journals/10.1146/annurev.micro.59.030804.121325)). Hundreds of MLST schemes for different pathogens have been made publicly available to ensure that a uniform nomenclature for typing is accessible through sites such as [PubMLST](https://pubmlst.org/). 

Recent advances and cost-efficiency in generating high-throughput whole-genome sequencing data have led to the expansion of some MLST schemes into core-genome MLST (cgMLST) schemes that include >1000 genes, creating sequence types that provide increased resolution for clonal population structures of bacterial genomes ([de Been et al. 2015](https://journals.asm.org/doi/full/10.1128/jcm.01946-15)). Following the increase in the number of whole genomes, PubMLST is increasingly including whole-genome sequences accessed through BIGSdb ([Jolley and Maiden. 2010](https://link.springer.com/article/10.1186/1471-2105-11-595)).

Several bioinformatics tools that identify MLST sequence types directly from the genome have been developed. For example, [mlst](https://github.com/tseemann/mlst) enables the identification of sequence types using PubMLST databases. FASTA files can then be used as input to get sequence types from a corresponding pathogen-specific database as well as the genomic sequences for each allele. Similarly, tools for cgMLST have been implemented. An example is [chewBBACA](https://github.com/B-UMMI/chewBBACA) a software used to create and evaluate cgMLST or whole-genome MLST (wgMLST) schema. chewBBACA creates schemas and allele calls on whole genomes resulting from de novo assemblers. For this practical session, [GrapeTree](https://github.com/achtman-lab/GrapeTree) will be used for visualisation.  



## 2. Expected learning outcomes <a name="outcomes"></a>

At the end of this practical session, one should be able to:  
  *	Use command-line tools such as mlst-check and chewBBACA to identify isolates’ MLST and cgMLST profiles or sequence types;
  *	Use tools such as PHYLOViZ and GrapeTree to visualise MLST and cgMLST results, respectively;  
  * Compare and contrast the two methods and when each is useful  



## 3. Genomes for MLST and cgMLST analysis <a name="genomes"></a>

### Data preparation

Table 1 contains the list of strains to be analysed in this practical from the CPE outbreak we will be investigating. Table 2 contains additional strains to be analysed (optionally, if time allows) sourced from key studies on the genomic epidemiology of methicillin-resistant *Staphylococcus aureus* (MRSA) ([Holden *et al.* 2013](https://doi.org/10.1101/gr.147710.112)) and extensively drug-resistant (XDR) *Salmonella typhi* ([Klemm *et al.* 2018](https://doi.org/10.1128/mbio.00105-18)). In this practical we will analyze the same strains characterised in the previous practical, plus the one you've been assigned to in the EpiCollect practical.

Table 1 CPE strains to be analysed in this practical
| Species | Study and origin | Strain Id | Illumina accession | Assembly file name |
| :---    | :---             | :---      | :---               | :---      |     
| *K. pneumoniae* | Roberts *et al.* 2024, CPE strain | cpe004 | ERR4095909 | cpe004_Kpn-ST78-NDM1.fasta |
| *E. coli* | Roberts *et al.* 2024, CPE strain | cpe069 | ERR5386320 | cpe069_Eco-NDM1.fasta |

Table 2 Additional strains to be analysed (optional).
| Species	| Study and origin | Strain Id | Genome accession | Assembly file name | 
| :---    | :---             | :---      | :---               | :---      |     
| *S. aureus*	| Holden *et al.* 2013, Berlin (Germany), 2007, ST22 EMRSA-15 | 07-02477 | ERR017261  | ERR017261.assembly.fa |
| *S. aureus*	| Holden *et al.* 2013, UK, 2005, ST22 EMRSA-15	| HO50960412 | HE681097 (GenBank) | HO50960412.fa |
| *S. typhi*	| Klemm *et al.* 2018 (ACT), Pakistan, 2016, 4.3.1 (H58) XDR | BL0006 | ERR2093245	| ERR2093245.assembly.fa |
| *S. typhi* | Klemm *et al.* 2018, Pakistan (2016) – 4.3.1 (H58) pre-XDR	| Pak60168 | ERR2093329	|ERR2093329.assembly.fa |

First of all, launch the Docker image on your machine:

If you haven’t done so already, clone the course Github directory into your home directory:

```bash
docker run -it --mount "type=bind,source=C:\Users\User\Desktop\amr25_data,target=/home/" amr:Dockerfile
```

Navigate to directory `home/data/`and create a new directory for this practical named `cp7`:

```bash
cd /home/data/data
mkdir cp7
cd cp7/
```

Next, copy the genome assemblies we will use for mlst run (i.e., those in Tables 1 and 2) from cp6 directory:

```bash
cp /home/data/data/cp6/complete_assemblies/cpe004_Kpn-ST78-NDM1.fasta .
cp /home/data/data/cp6/complete_assemblies/cpe069_Eco-NDM1.fasta .
```

Copy the additional genome assemblies that we will use for a batch run:

```bash
cp /home/data/data/cp6/additional_genomes/HO50960412.fa .
cp /home/data/data/cp6/additional_genomes/ERR017261.assembly.fa .
cp /home/data/data/cp6/additional_genomes/ERR2093245.assembly.fa .
cp /home/data/data/cp6/additional_genomes/ERR2093329.assembly.fa .
```

Also, identify and copy the genome assembly of **your assigned CPE strain** (the one on your EpiCollect sheet).


## 4. MLST prediction using mlst tool <a name="MLST"></a>

## mlst installation using conda

Create conda environment for mlst:

```
conda create -n mlst
```

Activate the conda environment using:

```
conda activate mlst
```

Now, install the mlst tool within the mlst conda environment you just created.

```
conda install mlst
```

Run mlst --help to test if it was successfully installed. You should see multiple run options.

```
mlst --help
```

Check available mlst schemes for other pathogens of interest using:

```
mlst --longlist
```

Run the mlst tool on your fasta files, e.g.:

```
mlst cpe004_Kpn-ST78-NDM1.fasta
```

Do a batch run for the rest of the .fa files and direct the result to a .csv output

```
mlst --csv *.fa --quiet > output.csv
```

Note:
It is important to submit unknown alleles to PubMLST for identification and allele number assignment. Therefore, if one of the alleles is unknown in the database, run:
mlst novel.fa --novel STR > novel_out


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











