# Computational Practical 10 - Metagenomics

**Adapted form Modules originally developed by**: Dr. Stanford Kwena, Dr. Ewan Harrison (2024 edition) & Dr. Aarthi Ravikrishnan, Dr. Arun Gonzales Decano (2025 edition)

Modified by: Dr. Stanford Kwenda, Augusto Messa Jr., Miriam Mwamba

## Table of contents (To be updated)
1. [Learning objectives](#objectives)
2. [Introduction](#intro)
3. [Set-up and Dataset](#setup)
    - [Aligning reads to reference](#alignment)
    - [Quiz 1](#quiz1)
    - [Variant calling](#variants)
    - [Creating a pseudogenome](#pseudogenomes)
    - [Creating a whole-geome alignment](#wgalignment)
    - [Quiz 2](#quiz2)
4. [Using snippy](#snippy)
    - [Data preparation](#dataprep)
    - [Quality control](#qcshort)
    - [Cleaning the reads (if necessary)](#cleaningshort)
    - [Short Read Alignment and SNP calling with snippy](#usesnippy)
    - [Examining the output](#snippyoutput)
    - [Post-processing and Analysis](#postshort)
5. [Long reads](#longreads)
    - [Data preparation](#datapreplong)
    - [Running Medaka](#medaka)
    - [Run DeepVariant](#deepvariant)
    - [PEPPER DeepVariant for nanopore reads](#pepperdeepvariant)
    - [Post-processing and Analysis](#postlong)
6. [References](#refs)

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

## **Set-up and Dataset** <a name="setup"></a>
Go to the `/home/data/data/` directory and create a directory called `cp10` by running:
```
mkdir /home/data/data/cp10
cd /home/data/data/cp10
```

To download the raw read files, you would run the following commands. However, the data is already in the machine, we just need to copy it to our working directory `cp10`
> NOTE
> DO NOT RUN these commands for the tutorial during this practical. The files we will be using have already been downloaded, we will just copy them. 

```
# Raw
wget <ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR142/072/SRR14297772/SRR14297772_1_ds.fastq.gz>
wget <ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR142/072/SRR14297772/SRR14297772_2.fastq.gz>
```

For this tutorail, we will be using a custom set of sequences (which were spiked-in) that can be obtained from [here](https://tinyurl.com/mvr3d263). Let's copy them into our working directory:
```
cp /home/data/data/metagenomics/mgx_sequences/SRR14297772_cpe107_* .
ls
```
We should now have within our working directory the following files:
```
# Spiked: c/o Aarthi and Arun: Download from <https://tinyurl.com/mvr3d263>
# Filenames: SRR14297772_cpe107_1_ds.fastq.gz and SRR14297772_cpe107_2.fastq.gz
```

