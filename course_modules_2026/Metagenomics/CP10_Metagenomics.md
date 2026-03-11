# Computational Practical 10 - Metagenomics

**Adapted form Modules originally developed by**: Dr. Stanford Kwena, Dr. Ewan Harrison (2024 edition) & Dr. Aarthi Ravikrishnan, Dr. Arun Gonzales Decano (2025 edition)

Modified by: Dr. Stanford Kwenda, Augusto Messa Jr., Miriam Mwamba

## Table of contents (To be updated)
1. [Learning objectives](#objectives)
2. [Introduction](#intro)
3. [Set-up and Dataset](#setup)
4. [Raw data quality and QC](#rawdataqc)
5. [Host contamination removal](#contremoval)
6. [Taxonomic classification](#taxclassification)
7. [AMR profiling](#amrprofiling)

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
	-o $clean_reads/${sampleid}.1.fq.gz -O $clean_reads/${sampleid}.2.fq.gz
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
“A contaminated sequence is one that does not faithfully represent the genetic information from the biological source organism/organelle because it contains one or more sequence segments of foreign origin.” [NCBI VecScreen](https://www.ncbi.nlm.nih.gov/tools/vecscreen/contam/)
* Shotgun metagenome sequencing data obtained from a host environment will usually be contaminated with sequences from the host organism
* Host sequences should be removed before further analysis:
	- To avoid biases
	- Reduce downstream computational load
	- Data protection or unintended data sharing e.g. in the case of a human host
* Positive vs negative filtering

For the decontamination step, we will use a tool called [`hocort`](https://github.com/ignasrum/hocort) (Host Co ntamination Removal Tool developed by Rumbavicius et al. 2023 - doi: [10.1186/s12859-023-05492-w](https://doi.org/10.1186/s12859-023-05492-w)).

```
# Activate the hocort environment
conda activate hocort

# Provide path to the bowtie2 index files
bwt=~/course/cp8/databases/hocort/human
 wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/914/755/GCF_009914755.1_T2T-CHM13v2.0/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna.gz

# Create directory to save decontaminated reads
hocort=~/course/cp8/hocort # Locate this index database
mkdir -p $hocort
threads=4

for fq in $(find $clean_reads -name "*1.fq.gz"); do
	sampleid=$(basename -s ".1.fq.gz" $fq)
	read1=$(find $clean_reads -name "${sampleid}*1*f*q.gz")
	read2=$(find $clean_reads -name "${sampleid}*2*f*q.gz")
	hocort map bowtie2 --threads $threads --filter true \
	-x ${bwt}/grch38 -i $read1 $read2 \
	-o $hocort/${sampleid}.R1.fq $hocort/${sampleid}.R2.fq 2> $hocort/${sampleid}.err

	# compress reads
	gzip $hocort/${sampleid}.1.fq
	gzip $hocort/${sampleid}.2.fq
done
```

# **Taxonomic classification**<a name='taxclassification'></a>
Annotation of reads or contigs with taxonomic information using e.g. blast based methods against reference databases. Quality of taxonomic assignments depends on:
1. Choice of tools
2. Reference database

## Prepare kraken2 database
```
# First let’s create a directory to store our databases
mkdir -p ~/course/cp8/databases/kraken2_8gb
# Next we will decompress the kraken2 database into the path we created above

tar -xvzf ~/course/cp8/databases/kraken2/k2_standard_08gb_20240112.tar.gz -C ~/course/cp8/databases/kraken2_8gb/
```
\*This step takes a bit of time and should be done the day before (or overnight).

## Perform taxonomic classification using kraken2
Now let’s activate the environment with the tools that we will need to use for this section.
```
conda activate classify
# create directory for kraken2 output
mkdir -p ~/course/cp8/kraken2

krak=~/course/cp8/kraken2


# set threads
threads=4

# set path to kraken2 database and clean_reads directory

db=~/course/cp8/databases/kraken2_8gb/
clean_reads=~/course/cp8/clean_reads


# execute kraken2
for fq in $(find $hocort -name "*R1.fq.gz"); do
	sampleid=$(basename -s ".R1.fq.gz" $fq)
	read1=$(find $hocort -name "${sampleid}*R1*f*q.gz")
	read2=$(find $hocort -name "${sampleid}*R2*f*q.gz")


	kraken2 --db "$db" --threads $threads --quick --paired \
		--output $krak/${sampleid}.kraken \
		--report $krak/${sampleid}.kraken.report \
		--memory-mapping $read1 $read2 \
		--gzip-compressed \
		--unclassified-out $krak/${sampleid}#_unclassified.fq >> $krak/krak.log
done
```

## Getting relative abundances
For this exercise we will be using a tool called bracken. Bracken computes the genus/species level abundance estimates based on DNA sequences from a metagenomic sample using taxonomic annotations assigned by kraken.

```
brak=~/course/cp8/bracken
mkdir -p $brak


for file in $(find $krak -name "*kraken.report"); do 
	sampleid=$(basename -s ".kraken.report" $file)
	bracken -d "$db" -i $file -o $brak/${sampleid}.bracken.report -w ${sampleid}.bracken_species.report
done
```

## Visualize the taxonomic classification results
For easy visualization/ summarization of the bracken output, we will use 2 approaches:
1. multiqc
2. krona

```
krona=~/course/cp8/krona
mkdir -p $krona


## ****** Participants working directly from the server can skip this step ******** ##
# Download and unpack the taxonomy data
copath=$(conda info --base)

cd $copath/envs/classify/opt/krona/taxonomy
wget -c ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz

# prepare/build the tax data
ktUpdateTaxonomy.sh --only-build

## ******************************************************************************** ##

cd ~/course/cp8

ktImportTaxonomy -t 5 -m 3 -o $krona/grouped.krona.html $brak
conda deactivate
```

# **AMR profiling**<a name='amrprofiling'></a>
We can determine the resistome of each metagenomic sample by either directly mapping/aligning cleaned reads to an AMR database, or using metagenomic assemblies. In this section, we will explore the read-based mapping option using `kma` and the `resfinder` database. 

`kma` should already be available in your path, and can verify this by using any of the following command(s):
```
kma -v
which kma
```
You should either get the version of kma or the path to kma executable binary.

```
# set threads
threads=4



# path to resfinder db
res_db=~/course/cp6/resfinder_db
kma_out=~/course/cp8/resistance


mkdir -p $kma_out


# Now let’s run kma

for fq in $(find $hocort -name "*R1.fq.gz"); do
	sampleid=$(basename -s ".R1.fq.gz" $fq)
	read1=$(find $hocort -name "${sampleid}*R1*f*q.gz")
	read2=$(find $hocort -name "${sampleid}*R2*f*q.gz")


	kma -mem_mode -ef -cge -nf -vcf -t $threads -ipe $read1 $read2 -t_db $res_db/all -o $kma_out/amr -1t1
done
```

**Output files**:

For downstream analysis, the following output files can be used e.g. in R, as input for differential abundance analysis, generation of graphs and other analyses.
1. amr.mapstat
2. Amr.res
3. amr.vcf.gz
