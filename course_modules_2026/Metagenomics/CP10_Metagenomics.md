# Computational Practical 10 - Metagenomics

**Adapted form Modules originally developed by**: Dr. Stanford Kwena, Dr. Ewan Harrison (2024 edition) & Dr. Aarthi Ravikrishnan, Dr. Arun Gonzales Decano (2025 edition)

Modified by: Dr. Stanford Kwenda, Augusto Messa Jr., Miriam Mwamba

## Table of contents (To be updated)
1. [Learning objectives](#objectives)
2. [Introduction](#intro)
3. [Set-up and Dataset](#setup)
4. [Raw data quality and QC](#rawdataqc)
5. [Host contamination removal](#contremoval)
    - [Aligning reads to reference](#alignment)
    - [Quiz 1](#quiz1)
    - [Variant calling](#variants)
    - [Creating a pseudogenome](#pseudogenomes)
    - [Creating a whole-geome alignment](#wgalignment)
    - [Quiz 2](#quiz2)
6. [Using snippy](#snippy)
    - [Data preparation](#dataprep)
    - [Quality control](#qcshort)
    - [Cleaning the reads (if necessary)](#cleaningshort)
    - [Short Read Alignment and SNP calling with snippy](#usesnippy)
    - [Examining the output](#snippyoutput)
    - [Post-processing and Analysis](#postshort)
7. [Long reads](#longreads)
    - [Data preparation](#datapreplong)
    - [Running Medaka](#medaka)
    - [Run DeepVariant](#deepvariant)
    - [PEPPER DeepVariant for nanopore reads](#pepperdeepvariant)
    - [Post-processing and Analysis](#postlong)
8. [References](#refs)

# **Learning objectives** <a name="objectives"></a>
This tutorial provides a step by step command line workflow for analyzing bacterial genomes from Illumina short-read metagenomica data. By following the steps, you will be able to:

1. Conduct quality control on Illumina reads
2. 

# **Introduction**<a name="intro"></a>
Metagenomics provides a culture-independent approach to investigate whole microbial communities (i.e. metagenomes). The word [ "Meta" comes from from Ancient Greek (μετά = metá, 'after, beyond') is an adjective meaning 'more comprehensive' or 'transcending'](https://en.wikipedia.org/wiki/Meta_(prefix)). Metagenomics is often used to study a specific community of microorganisms, such as those residing on human skin, in the soil or in a water sample.

There are two major approaches to metagenomic studies:
*  Amplicon sequencing (e.g. targetting the 16S rRNA gene; either entirely or specific regions).
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
* Tools to perform different taks: `fastqc`, `multiqc` `fastp`, `seqtk`, `Bbmap`, `hocort`, `Kraken2`, **ADD MORE TOOLS HERE**

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
wget <ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR142/072/SRR14297772/SRR14297772_1_ds.fastq.gz>
wget <ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR142/072/SRR14297772/SRR14297772_2.fastq.gz>
```

For this tutorail, we will be using a custom set of sequences (which were spiked-in) that can be obtained from [here](https://tinyurl.com/mvr3d263). Let's copy them into our working directory:
```
mkdir /home/data/data/cp10/raw_reads
cp /home/data/data/metagenomics/mgx_sequences/SRR14297772_cpe107_* raw_reads/
ls
```
We should now have within our working directory the following files:
```
# Spiked: c/o Aarthi and Arun: Download from <https://tinyurl.com/mvr3d263>
# Filenames: SRR14297772_cpe107_1.fastq.gz and SRR14297772_cpe107_2.fastq.gz
```

# **Raw data quality and QC**<a name="rawdataqc"></a>
This initial QC step can be performed using the same approaches introduced in [Computational Practical 3 - Accessing Data and Quality Control](https://github.com/WCSCourses/AMR_2026/blob/main/course_modules_2026/Data_access_QC/Computational_Practical_2_Accessing_Data_and_Quality_Control.md).
However, we will be using different tools to perform the raw read quality control, filtering and visualization. 

~~Before we proceed we should note the following:~~

QC of raw reads is often a standard first step used to assess the quality of reads and to identify potential problems or other quality related issues:
1. Sequencing technologies can produce reads with varying quality.
2. Some sample-specific issues such as contamination with adapter sequences.
3. Base composition biases.
4. Low base quality.

> [!NOTE]
> Its IMPORTANT to monitor key metrics at different steps of the data analysis workflow. Always remember one of the golden rules in Computational Biology: Garbage in :arrow_right: Garbage out

Since we are performing read filtering and QC of metagenomic data, it might be beneficial to perform read deduplication during the initial QC step. This will be done in a single step as we perform our standard QC step. We will perform read QC and filtering based on the steps below:

```
# Create output directory for fastp output
clean_reads=/home/data/data/cp10/clean_reads
mkdir -p $clean_reads

# Provide path to the raw reads directory
raw_reads=/home/data/data/cp10/raw_reads

# Execute the for loop to perform QC on all samples in the raw_reads directory
for fq in $(find $raw_reads -name "*1.fq.gz"); do
	sampleid=$(basename -s "_1.fq.gz" $fq)
	read1=$(find $raw_reads -name "${sampleid}*1*f*q.gz")
	read2=$(find $raw_reads -name "${sampleid}*2*f*q.gz")
	
	fastp -i "$read1" -I "$read2" \
	-q 20 -l 36 --cut_front -M 10 -W 4 \
	-R "$sampleid" -j $clean_reads/${sampleid}.fastp.json \
	-h $clean_reads/${sampleid}.fastp.html \
	--correction --dedup --overrepresentation_analysis --thread 4 \
	-o $clean_reads/${sampleid}.R1.fq.gz -O $clean_reads/${sampleid}.R2.fq.gz
done >> $clean_reads/qc_step1.log 2>&1
```
**Key points**:

Including a read deduplication step can potentially:
1. Increase the number of metagenome-assembled contigs (might be sample dependent).
2. Improve the length of the metagenome-assembled contigs (might be sample dependent).
3. Improve metagenomic binning yields (i.e. can contribute to the better recovery of MAGs from complex metagenomes).
4. Decrease the maximum memory requirement and time consumption during the computationally intensive meta-assembly step.
5. Enhance the coverage abundance profiles of contigs.

## Read QC visualization
For read QC visualization, we will use `multiqc`. We have used this in previous practicals.
```
qc_reports=/home/data/data/cp10/multiqc
multiqc -f --no-data-dir $clean_reads --outdir $qc_reports
```

**Group activity 1**

Navigate to the `multiqc` output directory/folder and open the report in your browser. In groups of 2 or 3 discuss the following:
1. Number of reads in each sample?
2. Percentage of reads which passed filters in each sample?
3. What was the duplication rate before filtering?
4. The average quality after filtering?
5. What is the average length of the reads?

# **Host contamination removal**<a name="contremoval"></a>
