# Computational Practical 10 - Metagenomics

**Adapted form Modules originally developed by**: Dr. Stanford Kwena, Dr. Ewan Harrison (2024 edition) & Dr. Aarthi Ravikrishnan, Dr. Arun Gonzales Decano (2025 edition)

Modified by: Dr. Stanford Kwenda, Augusto Messa Jr., Miriam Mwamba

## Table of contents (To be updated)
1. [Learning objectives](#objectives)
2. [Introduction](#intro)
3. [Manual alignment and variant calling]()
    - [Set-up](#setup)
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
| **Characteristic** | **16s rRNA sequencing** | **Shotgun metagenomic sequencing** |
| Taxonomic Resolution | Bacterial genus level (can resolve down to species level using long reads) | Bacterial species level (can include strains) |
| Taxonomic coverage | Mainly bacteria and archaea | All microbial taxa including bacteria, viruses and fungi |
| Host contamination | Low | High |
| Bioinformatics expertise | Beginner to intermediate | Intermediate to advanced |
| Functional profiling | No\* | Yes |

\* Predicted functional profiling might be possible.

In this tutorial we will be focusing on shotgun metagenomic sequencing.

For this process will need two things: 
* Sequence reads.
* Reference genome.
* Tools for working with short reads: `fastp`, `snippy`, `samtools` and `bcftools`.
* Tools for working with long reads: `minimap2`, `samtools`, `Medaka`, `DeepVariant`. 
* General tools: `FastQC`, `MultiQC` and `snpEff`.
 
Choosing a reference genome is a critical step in this process, an ideal reference should: 
* Have a complete genome (a single contiguous assembly, for most Prokaryotes) and belong to the same species as the sequenced isolate
* Be well annotated (if possible with a curated annotation)
* Be available at the NCBI/ENA databases.

# **Manual alignment and variant calling**
## **Set-up** <a name="setup"></a>
For this practical we will be analysing the sequence reads of a _S. typhi_ isolate *ERR2093239*. The sequence reads and the reference sequence
are located in the folder `cp5`.

Now, `cd` into this directory by typing:
```
cd /home/manager/course/cp5/manual_analysis
```

> [!NOTE]
> **For those in the overflow room only, the files are not there**, so run the following commands to get the files into _cp5/manual_analysis_:

```
wget https://github.com/WCSCourses/AMR_2026/edit/main/course_modules_2026/Alignment_and_Variant_Calling/downsampled_manual/ERR2093239_1.fastq.gz
wget https://github.com/WCSCourses/AMR_2026/edit/main/course_modules_2026/Alignment_and_Variant_Calling/downsampled_manual/ERR2093239_1.fastq.gz
```

> [!NOTE]
> The files you have just downloaded are not the original ones. They were downsampled to allow us proceeding with the practical.

Before going any further, let's ensure the tools are installed properly, the following commands when typed in the terminal must not generate any error.
```
bwa
samtools
bcftools
snp-dists
```

## **Alignment** <a name="alignment"></a>
The first step is to create an index of the reference genome sequence. Indexing allows the aligner to quickly identify target regions and helps
make the process quicker. This needs to be carried out only once for a reference sequence and can be reused for mapping more isolated to the
same reference.

Now type the following command in the terminal:
```
bwa index reference.fa
```
Check how many new files are created as a result using the command
```
ls -l
```
The next step is to carry out mapping using the BWA-MEM algorithm. A typical command looks like this:
```
bwa mem reference.fa read1.fastq read2.fast > output.sam # Syntax
# Note: Don't worry the command won't work as we have not provided the correct read files.
```
In the above command, `reference.fa` is the reference genome sequence and `read1.fastq` and `read2.fastq` are the two reads. The alignment gets redirected
to a specified output file, that is by this part of the command above: `> output.sam`.

Now, using the reads of isolate **ERR2093239** (`ERR2093239_1.fastq.gz` and `ERR2093239_2.fastq.gz`) to map on the reference sequence (_Salmonella typhi_ CT18; 
accession: NC_003198.1).

Now, run the following command to initiate the alignment process:
```
bwa mem reference.fa ERR2093239_1.fastq.gz ERR2093239_2.fastq.gz >ERR2093239_aln.sam
```
Note: This process could take some time to complete, so it would be good to take a look at the course material so far or read more about [BWA](https://bio-bwa.sourceforge.net/).

The output file generated is large in size therefore don’t attempt to open it on the GUI. The output file is in SAM format which is a tab-delimited file (remember the
formats we covered during the CP1 - Introduction to Computational Biology Module) containing details about each read and its alignment to the reference. The details
of SAM format can be found [here](https://samtools.github.io/hts-specs/SAMv1.pdf).

For ease of handling and to reduce the size of the alignment file the SAM file is converted to a compressed binary file called BAM file. Type the following
command in the terminal:
```
samtools view -O BAM -o ERR2093239_aln.bam ERR2093239_aln.sam
```
In the command above, the option `-O` specifies the output format and `-o` specifies the output file name. We can check the difference of sizes between the `.sam` 
and the `.bam` file using the following command: `ls -lh`.

Next, we will sort the alignment file (`.bam`) file by chromosome coordinates using the following command:
```
samtools sort -T temp -O bam -o ERR2093239_aln_sorted.bam ERR2093239_aln.bam
```
In the command above, the option `-T` specifies the name of a temporary files that are created when running the process, `-O` specifies the output file format
and `-o` specifies the output file name.

Now, this sorted `.bam` file can be used for the next steps, including exploring mapping statistics. The first step to achieve this is to index it.
```
samtools index ERR2093239_aln_sorted.bam
```
