# Computational Practical 10 - Metagenomics

**Adapted form Modules originally developed by**: Dr. Stanford Kwena, Dr. Ewan Harrison (2024 edition) & Dr. Aarthi Ravikrishnan, Dr. Arun Gonzales Decano (2025 edition)

Modified by: Dr. Stanford Kwenda, Augusto Messa Jr., Miriam Mwamba

## Table of contents
1. [Learning objectives](#objectives)
2. [Introduction](#intro)
3. [Set-up and Dataset](#setup)
4. [Raw data quality and QC](#rawdataqc)
5. [Host contamination removal](#contremoval)
6. [Metagenome assembly with metaSPAdes](#metaspades)
7. [Binning the Contigs](#binning)
8. [Taxonomic classification kof Contigs (MAGs) and/or Reads](#taxclassification)
9. [Genome Annotation](#magsannotation)
10. [AMR Prediction](#amrpred)
11. [Visualization of Taxonomy with Pavian or Krona](#metavisualization)

# **Learning objectives** <a name="objectives"></a>
This tutorial provides a step by step command line workflow for analyzing bacterial genomes from Illumina short-read metagenomica data. By following the steps, you will be able to:

1. Conduct quality control on Illumina reads
2. Assemble short reads into contigs using metaSPAdes.
3. Bin contigs into genomes (Metagenome-Assembled Genomes or MAGs).
4. Taxonomically classify and annotate these genomes.
5. Assess antimicrobial resistance (AMR) potential and visualize taxonomic data.

# **Introduction**<a name="intro"></a>
Metagenomics provides a culture-independent approach to investigate whole microbial communities (i.e. metagenomes). The word [ "Meta" comes from from Ancient Greek (μετά = metá, 'after, beyond') is an adjective meaning 'more comprehensive' or 'transcending'](https://en.wikipedia.org/wiki/Meta_(prefix)). Metagenomics is often used to study a specific community of microorganisms, such as those residing on human skin, in the soil or in a water sample.

There are two major approaches to metagenomic studies:
*  Amplicon sequencing (e.g. targetting the 16S rRNA gene; either entirely or specific regions) - metabarcoding.
*  Shotgun metagenomic sequencing or whole-genome shotgun sequencing.

**Key differences between the two approaches**
Characteristic | 16s rRNA sequencing | Shotgun metagenomic sequencing |
----------|--------------|--------------
Taxonomic Resolution | Bacterial genus level (can resolve down to species level using long reads) | Bacterial species level (can include strains)
Taxonomic coverage | Mainly bacteria and archaea | All microbial taxa including bacteria, viruses and fungi
Host contamination | Low | High
Bioinformatics expertise | Beginner to intermediate | Intermediate to advanced
Functional profiling | No\* | Yes

\* Predicted functional profiling might be possible.

In this tutorial we will be focusing on shotgun metagenomic sequencing.

For this process will need two things: 
* Metagenomic sequencing reads: for this tutorial, raw files from [Guo et al. 2021 - doi: 10.3389/fmicb.2021.709051](https://doi.org/10.3389/fmicb.2021.709051) will be used
* Tools to perform different taks: `FastQC`, `MultiQC` `Fastp`, `seqtk`, `Bbmap`, `metaSPAdes`, `MetaBAT2`, `Kraken2`, `CheckM`, `Prokka`, `ABRicate` (for AMR prediction) and `Pavian` and `Krona` for visualization.

# **Set-up and Dataset** <a name="setup"></a>
Go to the `/home/data/data/` directory and create a directory called `cp10` by running:
```
mkdir /home/data/data/cp10
cd /home/data/data/cp10
```

To download the raw read files, you would run the following commands. However, the data is already in the machine, we just need to copy it to our working directory `cp10`
> [!NOTE]
> DO NOT RUN these commands for the tutorial during this practical. The files we will be using have already been downloaded, we will just copy them. 

```
# Raw
#wget <ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR142/072/SRR14297772/SRR14297772_1_ds.fastq.gz>
#wget <ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR142/072/SRR14297772/SRR14297772_2.fastq.gz>
```

For this tutorail, we will be using a custom set of sequences (which were spiked-in) that can be obtained from [here](https://tinyurl.com/mvr3d263). Let's copy them into our working directory:
```
mkdir /home/data/data/cp10/raw_reads /home/data/data/cp10/clean_reads /home/data/data/cp10/qc_reports
cp /home/data/data/metagenomics/mgx_sequences/SRR14297772_cpe107_* raw_reads/
cp /home/data/data/metagenomics/mgx_sequences/SRR14297772_cpe110_* raw_reads/
ls
```
We should now have within our working directory the following files:
```
# Spiked: c/o Aarthi and Arun: Download from <https://tinyurl.com/mvr3d263>
# Filenames: SRR14297772_cpe107_1.fastq.gz and SRR14297772_cpe107_2.fastq.gz & SRR14297772_cpe110_1.fastq.gz and SRR14297772_cpe110_2.fastq.gz 
```

# **Raw data quality and QC**<a name="rawdataqc"></a>
This initial QC step can be performed using the same approaches introduced in [Computational Practical 3 - Accessing Data and Quality Control](https://github.com/WCSCourses/AMR_2026/blob/main/course_modules_2026/Data_access_QC/Computational_Practical_2_Accessing_Data_and_Quality_Control.md).

QC of raw reads is often a standard first step used to assess the quality of reads and to identify potential problems or other quality related issues:
1. Sequencing technologies can produce reads with varying quality.
2. Some sample-specific issues such as contamination with adapter sequences.
3. Base composition biases.
4. Low base quality.

> [!NOTE]
> Its IMPORTANT to monitor key metrics at different steps of the data analysis workflow.
> Always remember one of the golden rules in Computational Biology: Garbage in :arrow_right: Garbage out

Since we are performing read filtering and QC of metagenomic data, it might be beneficial to perform read deduplication during the initial QC step. This will be done in a single step as we perform our standard QC step. We will perform read QC and filtering based on the steps below:

```
fastp -i raw_reads/SRR14297772_cpe107_1.fastq.gz -I raw_reads/SRR14297772_cpe107_2.fastq.gz -o clean_reads/SRR14297772_cpe107_1_ds_filtered.fastq.gz -O clean_reads/SRR14297772_cpe107_2_ds_filtered.fastq.gz -h qc_reports/cpe107_fastp_report.html -j qc_reports/cpe107_fastp_report.json --length_required 50 --correction --dedup --overrepresentation_analysis --thread 4
fastp -i raw_reads/SRR14297772_cpe110_1.fastq.gz -I raw_reads/SRR14297772_cpe110_2.fastq.gz -o clean_reads/SRR14297772_cpe110_1_ds_filtered.fastq.gz -O clean_reads/SRR14297772_cpe110_2_ds_filtered.fastq.gz -h qc_reports/cpe110_fastp_report.html -j qc_reports/cpe107_fastp_report.json --length_required 50 --correction --dedup --overrepresentation_analysis --thread 4 
```
- **What It Does**: Fastp removes adapters, trims low-quality bases, and discards reads shorter than 50 bp. Hostile gets rid of host (mainly) human reads.
- **Key Options for Fastp**:
    - `-h` and `-j`: Generate HTML and JSON reports with trimming metrics.
    - `-length_required`: Discards reads shorter than 50 bp.
    - `--dedup`: deduplication.
    - `--overrepresentation_analysis`: performing an over representation analysis.
    - `--threads`: specifying how many CPUs can the tool use, to speed up the execution.

> [!NOTE]
> When you are running this pipeline on multiple samples, and you don't want to build this commands one by one for each sample, it's possible to package it within a single loop, just like below.
> Do not run it.
```
## Create output directory for fastp output
##clean_reads=/home/data/data/cp10/clean_reads
##mkdir -p $clean_reads

## Provide path to the raw reads directory
##raw_reads=/home/data/data/cp10/raw_reads

## We will skip the FastQC step

## Execute the for loop to perform QC on all samples in the raw_reads directory
#for fq in $(find $raw_reads -name "*1.f*q.gz"); do \
#	sampleid=$(basename -s "_1.fastq.gz" $fq) \ 
#	read1=$(find $raw_reads -name "${sampleid}*1*f*q.gz") \
#	read2=$(find $raw_reads -name "${sampleid}*2*f*q.gz") \
#	
#	fastp -i "$read1" -I "$read2" \
#	-q 20 -l 36 --cut_front -M 10 -W 4 \
#	-R "$sampleid" -j $clean_reads/${sampleid}.fastp.json \
#	-h $clean_reads/${sampleid}.fastp.html \
#	--correction --dedup --overrepresentation_analysis --thread 4 \
#	-o $clean_reads/${sampleid}.1.fq.gz -O $clean_reads/${sampleid}.2.fq.gz \
#done >> $clean_reads/qc_step1.log 2>&1
```

## **Key points**:

Including a read deduplication step can potentially:
1. Increase the number of metagenome-assembled contigs (might be sample dependent).
2. Improve the length of the metagenome-assembled contigs (might be sample dependent).
3. Improve metagenomic binning yields (i.e. can contribute to the better recovery of MAGs from complex metagenomes).
4. Decrease the maximum memory requirement and time consumption during the computationally intensive meta-assembly step.
5. Enhance the coverage abundance profiles of contigs.

## Read QC visualization (Optional)
For read QC visualization, we can use `multiqc`. We have used this in previous practicals. We have used this in previous practicals. We could use it in the `FastQC` or `Fastp` reports, but that would be most useful if we had multiple samples, since we only have one, we will skip it and just check the `Fastp` report.

```
#qc_reports=/home/data/data/cp10/multiqc
#multiqc -f --no-data-dir $clean_reads --outdir $qc_reports
```

**Group activity 1**

Navigate to the `multiqc` output directory/folder and open the report in your browser. In groups of 2 or 3 discuss the following:
1. Number of reads in each sample?
2. Percentage of reads which passed filters in each sample?
3. What was the duplication rate before filtering?
4. The average quality after filtering?
5. What is the average length of the reads?

# **Host contamination removal**<a name="contremoval"></a>
“A contaminated sequence is one that does not faithfully represent the genetic information from the biological source organism/organelle because it contains one or more sequence segments of foreign origin.” [NCBI VecScreen](https://www.ncbi.nlm.nih.gov/tools/vecscreen/contam/)
* Shotgun metagenome sequencing data obtained from a host environment will usually be contaminated with sequences from the host organism
* Host sequences should be removed before further analysis:
	- To avoid biases
	- Reduce downstream computational load
	- Data protection or unintended data sharing e.g. in the case of a human host
* Positive vs negative filtering

For the decontamination step, we will use a tool called [`hostile`](https://github.com/bede/hostile) (developed by Constantinides et al. 2023 - doi: [10.1093/bioinformatics/btad728](https://doi.org/10.1093/bioinformatics/btad728)).

> [!IMPORTANT]
> In this tutorial, we will be using the cleaned files from `fastp`. So, DO NOT run the code bellow.
> However, in the practical applications, please ensure that you have removed the host reads to ensure your downstream analyses is on microbial reads only.

```
## Create and activate a conda env 
#conda create -y -n hostile -c conda-forge -c bioconda hostile 
#conda activate hostile
#conda activate --stack amr # to access packages from the amr env 
## Run Hostile on paired short reads 
#hostile clean --fastq1 SRR14297772_cpe107_1_ds_filtered.fastq.gz --fastq2 SRR14297772_cpe107_2_ds_filtered.fastq.gz -o - > SRR14297772_cpe107.interleaved.fastq

## Bin interleaved fastq files into clean.fastq1 and clean.fastq2 using seqtk
#seqtk seq -1 SRR14297772_cpe107.interleaved.fastq > clean.SRR14297772_cpe107_1.fastq
#seqtk seq -2 SRR14297772_cpe107.interleaved.fastq > clean.SRR14297772_cpe107_2.fastq

## Compress all fastq files (pigz offers fast compression. You can also use gzip)
#pigz SRR14297772_cpe107.interleaved.fastq
#pigz clean.SRR14297772_cpe107_1.fastq
#pigz clean.SRR14297772_cpe107_2.fastq
```

## **Downsample Reads (Optional)**
Sometimes this step is done -- but it is not mandatory. For this tutorial, we will skip this step.

Reduce the number of reads in the dataset while preserving the diversity of the sample. Use `seqtk` sample for random subsampling of reads to a desired percentage or absolute number.
```bash
#seqtk sample -s100 input.fastq 0.1 > downsampled.fastq

#-s100 specifies a random seed for reproducibility.
#0.1 specifies 10% of the total reads (adjust according to needs).
```

Use [`bbnorm.sh`](http://bbnorm.sh/) in [`BBMap`](https://sourceforge.net/projects/bbmap/) for read normalization, which reduces redundancy while keeping unique reads.

```bash
#bbnorm.sh in=input.fastq out=downsampled.fastq target=20 min=2

# target=20 controls coverage normalization depth (can be adjusted based on data).
```

# **Metagenome assembly with metaSPAdes**<a name='metaspades'></a>
**metaSPAdes** is a high-performance, open-source de novo metagenomic assembler designed for assembling complex, uneven-coverage sequencing data, such as soil or gut microbiome samples. It is optimized for metagenomic data and assembles reads into contigs, reconstructing genome fragments from complex microbial communities. metaSPAdes is part of the [SPAdes](https://github.com/ablab/spades) toolkit and is described in the paper by Nurk et al. 2017 (doi: [10.1101/gr.213959.116](https://doi.org/10.1101/gr.213959.116)).

**With the output from fastp**

```
metaspades.py -1 SRR14297772_cpe107_1_ds_filtered.fastq.gz -2 SRR14297772_cpe107_2_ds_filtered.fastq.gz -o SRR14297772_cpe107_metaspades_output/ --only-assembler # fastp-cleaned only
```

**If you have removed host reads with `hostile`**

```
metaspades.py -1 clean.SRR14297772_cpe107_1.fastq.gz -2 clean.SRR14297772_cpe107_2.fastq.gz -o clean_SRR14297772_cpe107_metaspades_output/ --only-assembler # fastp and hostile-cleaned
```

- **What It Does**: metaSPAdes assembles contigs by building a de Bruijn graph adapted for metagenomic data.
- **Output**: Assembled contigs are saved in the `metaspades_output/` directory (In our case the output is in `SRR14297772_cpe_107_metaspades_output/`).
- **Warning**: This step is usually time consuming and memory intensive.

Inspect `contigs.fasta` in `SRR14297772_cpe_107_metaspades_output/` to check contig lengths and quality. 

What are the N50 and L50 values? [Hint: use python script `find_assembly_stats.py` from the `Metagenomics` folder]. You can also download it from [here](https://github.com/WCSCourses/AMR_2026/blob/main/course_modules_2026/Metagenomics/find_assembly_stats.py):
```
wget https://github.com/WCSCourses/AMR_2026/blob/main/course_modules_2026/Metagenomics/find_assembly_stats.py
```

Another tool that can be used is [Quast](https://github.com/ablab/quast), which we learned about during [Computational Practical 4 - Genome assembly and annotation](https://github.com/WCSCourses/AMR_2026/blob/main/course_modules_2026/genome_assembly/AMR_2026_Genome_assembly.md).

# **Binning the Contigs**<a name='binning'></a>

Binning groups of contigs into bins representing putative genomes. **MetaBAT2** performs binning based on sequence composition and read coverage.

1. **Run MetaBAT2**:
```
metabat2 -i SRR14297772_cpe_107_metaspades_output/contigs.fasta -o bins_folder/bin -m 1500
```
   
* **What It Does**: MetaBAT2 clusters contigs into bins that represent draft genomes.
* **Key Option**:
	- `m 1500`: Sets the minimum contig length to 1500 bp for binning.

2. **Examine Binning Results**:
The binned genomes are saved in `bins_folder/`, with each bin corresponding to a draft genome.

## Quality Assessment of Bins
Use **CheckM** to evaluate the quality of binned genomes, assessing completeness and contamination based on conserved marker genes.

1. **Run CheckM**:
```
checkm lineage_wf -x fa -t 8 bins_folder/ checkm_output/ --pplacer_threads 8
```
   
* **What It Does**: CheckM evaluates each bin for genome completeness and contamination.
* **Interpret Results**: Bins with >90% completeness and <5% contamination are considered high-quality.
  
Q: What is the completeness and contamination of bins? [**Hint**: Look at bin_stats_ext.tsv]

# **Taxonomic classification of Contigs (MAGs) and/or Reads**<a name='taxclassification'></a>
Taxonomic classification allows annotation of reads or contigs with taxonomic information. This is performed by identifying the contigs taxonomic origin with [**Kraken2**](https://ccb.jhu.edu/software/kraken2/), which compares contigs to a taxonomic database.

Annotation of reads or contigs with taxonomic information using e.g. blast based methods against reference databases. Quality of taxonomic assignments depends on:
1. Choice of tools
2. Reference database

## **Run Kraken2 to identify microbial diversity**:
```
kraken2 --db /home/data/data/kraken2/ --threads 8 --output kraken_output.txt --report kraken_report.txt SRR14297772_cpe_107_metaspades/contigs.fasta
```
    
* **What It Does**: Kraken2 assigns taxonomic classifications by matching sequences against a reference database.
* **Output**: Results are saved in `kraken_output.txt` with a summary report in `kraken_report.txt`.
* Alternatively, run Kraken 2 on the reads after host contamination removal (`hostile`).

> [!NOTE]
> DO NOT run the command below
```
kraken2 --db /home/data/kraken2/ clean.SRR14297772_cpe107_1.fastq.gz clean.SRR14297772_cpe107_2.fastq.gz --threads 8 --output kraken_output_reads.txt --report kraken_report_reads.txt    
```

# **Genome Annotation**<a name='magsannotation'></a>
We can now use `Prokka` to annotate each bin to identify genes and other genomic features.

```
prokka --outdir annotation_output --prefix bin_1_annotation bins_folder/bin.1.fa
```
    
* **What It Does**: Prokka annotates genes and functional elements in each bin.
* **Output**: Annotations are saved in `annotation_output/


# **AMR Prediction**<a name='amrpred'></a>
We can now proceed to identify antimicrobial resistance (AMR) genes using **ABRicate**, which screens genomes against known AMR gene databases. By default it uses NCBI database, which is a subset of the AMRFinderPlus database to do AMR gene detection. To exploit the complete functionality of AMR prediction, use AMRFinderPlus. See note [here](https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/AMRFinder/). 

**Run ABRicate for AMR Prediction**:
List all available databases:
```
abricate --list
```

To run ABRicate on the bins [Default database is ncbi]
```
abricate bins_folder/bin.1.fa > abricate_output.txt
```
* **What It Does**: ABRicate searches for known AMR genes by comparing genome sequences against the ResFinder database.
* **Output**: Results in `abricate_output.txt` list detected AMR genes, their identities, and resistance classes.
   
**Question**: Can you compare the results from Prokka and ABRicate? Do you find anything in common? Can you explain your observation?


# **Visualization of Taxonomy with Pavian or Krona**<a name='metavisualization'></a>
Now, with these results we can visualize taxonomic classifications interactively using **Pavian** or **Krona**:

* [**Pavian**]((https://github.com/fbreitwieser/pavian)) is a interactive browser application for analyzing and visualization metagenomics classification results from classifiers such as Kraken, KrakenUniq, Kraken 2, Centrifuge and MetaPhlAn. Pavian also provides an alignment viewer for validation of matches to a particular genome. Read the publication: Breitwieser and Salzberg 2020 - doi: [10.1093/bioinformatics/btz715](https://doi.org/10.1093/bioinformatics/btz715).
* [**Krona**](https://github.com/marbl/Krona/wiki) allows hierarchical data to be explored with zooming, multi-layered pie charts. Krona charts can be created using an Excel template or KronaTools, which includes support for several bioinformatics tools and raw data formats. The interactive charts are self-contained and can be viewed with any modern web browser. Read the publication: Ondov et al. 2011 - doi: [10.1186/1471-2105-12-385](https://doi.org/10.1186/1471-2105-12-385).

## Option 1: Visualization with Pavian
Start the pavian server from your terminal or upload the kraken reports on the [web server](https://fbreitwieser.shinyapps.io/pavian/).
    
* **What It Does**: Pavian launches a local server for visualizing taxonomic classifications in your web browser.
* **Upload**: Load `kraken_report.txt` into Pavian for an interactive visualization.

### Option 2: Visualization with Krona)
Documentation: https://github.com/marbl/Krona/wiki/Installing
```
# Installation
cd /home/data/data/
git clone https://github.com/marbl/Krona.git
cd Krona/KronaTools
./install.pl
```

**Convert Kraken2 Output for Krona**:
```
cut -f2,3 kraken_output.txt > krona_input.txt
```
    
* **What It Does**: Extracts only the taxonomic ID and classification from Kraken2 output, creating a format compatible with Krona.

**Generate Krona Plot**:
```
# Update taxonomy index
ktUpdateTaxonomy.sh
```
    
```
ktImportTaxonomy -m 1 -o krona-test.html
ktImportTaxonomy krona_input.txt -o krona_output.html
```
    
* **What It Does**: Krona generates an HTML file (`krona_output.html`) with a multi-level circular plot for exploring taxonomic data.
* **View the Plot**: Open `krona_output.html` in any web browser.

**Exploring the Krona Plot**:
* Click on different sections to zoom into taxonomic levels.
* Hover over sections to view specific taxonomic details.

# Exercises
1. Test this workflow on the sample Illumina dataset we provided.
2. Experiment with different assembly parameters in metaSPAdes.
3. Compare taxonomic classifications generated by Kraken2 with other tools, such as Centrifuge.
4. Visualize different datasets in Pavian or Krona to identify any microbial community trends or outliers.
