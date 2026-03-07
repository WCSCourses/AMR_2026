# Computational Practical 5 - Alignment and Variant Calling

**Adapted form Modules originally developed by**: Dr. Narender Kumar, Dr. Fahad Khokar (2024 edition) & Dr. Arun Gonzales Decano (2025 edition)

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
1. How to align short and long reads from a sequencing experiments to a reference genome.
2. How to identify variants within the reads from a sequencing experiment and a reference genome.


# **Introduction**<a name="intro"></a>
Variant calling involves crucial steps in comparative genomics that researchers use to identify genetic variations between bacterial strains. Short-read sequencing data (from Illumina) and long-read sequencing data (from PacBio or Oxford Nanopore) have distinct characteristics, each with specific tools and methods for optimal processing. In this CP we will learn how to identify variants: single nucleotide polymorphisms (SNPs) and small insertions and deletions (indels). 
For this purpose, we will use the sequence reads and align them to a reference genome (genome sequence of an isolate which is already well
characterised and annotated).

Over the years, a number of bioinformatic tools have been developed to enable mapping of sequence reads to a reference genome (doi: 
[10.3389/fpls.2021.657240](https://www.frontiersin.org/articles/10.3389/fpls.2021.657240/full)). We will use the [**_BWA_** (Burrows-Wheeler
Aligner)](https://bio-bwa.sourceforge.net/), followed by variant calling using [**_samtools_**](https://samtools.org/) and [**_bcftools_**](https://github.com/samtools/bcftools) to perform these tasks "manually". Then we will also explore doing it using [`snippy`](https://github.com/tseemann/snippy) tool for short reads. Steps to perform alignment and variant calling for long reads are also provided. 

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

> [!NOTE]
> **For those in the overflow room only the files are not there**, so run the following commands to get the files into _cp5/manual_analysis_:

```
wget 
wget
```

Now, `cd` into this directory by typing:
```
cd /home/manager/course/cp5/manual_analysis
```
Note: to ensure the tools are installed properly, the following commands when typed in the terminal must not generate any error.
```
bwa
samtools
bcftools
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

Once the alignment is indexed, we can extract the mapping statistics using `samtools stats`. This provides details on how many reads mapped to the reference,
how much of the reference is covered by the sequenced reads and more. The statistics generated could reveal a lot of intormation about the choice of reference
and the quality of the sequenced data as well. Let's gather the statistics by running these commands:
```
samtools stats ERR2093239_aln_sorted.bam > ERR2093239_bamstats.txt
grep “^SN” ERR2093239_bamstats.txt > stats.txt
```
## **Quiz 1**<a name="quiz1"></a>
1. What is the total number of mapped reads?
2. What is the total number of unmapped reads?
3. What is the total number of mapped and properly paired reads?
4. What is the average insert size?
5. What is the percentage of reads properly paired?

## **Variant calling** <a name="variants"></a>
Once the sequence reads have been successfully aligned to the chosen reference, we can use it to identify variants present in the isolate.

The first step is to convert the `_sorted.bam` alignment file to `.bcf` ([Binary Call Format - BCF](https://github.com/samtools/hts-specs/blob/master/VCFv4.3.pdf)) using the following command:
```
bcftools mpileup -Ob -m 4 -f reference.fa ERR2093239_aln_sorted.bam > ERR2093239_variants.bcf
```
Note: You might see a few warnings, you can ignore them!

In the command above, the option `-Bug` specifies different run parameters which can be read here (http://www.htslib.org/doc/samtools-mpileup.html), `-m` specifies the minimum
number of reads required for indel calling and `-f` specifies the reference file.

Now we convert the bcf file to vcf (variant calling format). This step converts the binary file into the text file containing the variants identified from the alignment.
```
bcftools call -mv -O v -o ERR2093239_variants.vcf ERR2093239_variants.bcf
```

Once finished we can see the first 10 variants of the "ERR2093239_variants.vcf" file.
```
grep -A 10 "#CHROM" ERR2093239_variants.vcf
```

### Filtering the variants
At this stage the variants include both SNPs and short Indels identified from the alignment of reads. The following process describes how we can identify high
quality SNPs (only) from the file applying different metrics using bcftools filter function:

**Filter only SNPs from the `MD--1_variants.vcf` file.**
```
bcftools filter -i 'type="snp"' -g10 -G10 ERR2093239_variants.vcf -o ERR2093239_SNPs.vcf
```
In the command above options `-g` removes any SNPs that fall within the indicated bp distance (10bp) from an indel and `-G` removes indels that are less
than the indicated bp distance (10bp).

**Filter the SNPs with base quality (QUAL) >=50, MQ >=30 and read depth (DP)>5.**
```
bcftools filter -i 'type="snp" && QUAL>=50 && INFO/DP>5 && MQ>=30' -g10 -G10 ERR2093239_variants.vcf -o ERR2093239_SNPs_try1.vcf
```

**Filter all homozygous SNPs (alternate base ratio >= 0.80)**
```
bcftools filter -i 'type="snp" && QUAL>=50 && INFO/DP>5 && MQ>=30 && DP4[2]/(DP4[2]+DP4[0])>=0.80 && DP4[3]/(DP4[3]+DP4[1])>=0.80' -g10 -G10 ERR2093239_variants.vcf -o ERR2093239_SNPs_filtered.vcf
```

## **Creating a pseudogenome** <a name="pseudogenomes"></a>
Now that we have filtered the SNPs that we identified in the previous steps, we can use these SNPs to generate a pseudogenome which is essentially the reference
genome sequence but the nucleotides are replaced by the SNPs identified at the corresponding positions.

The first step is to create a zipped `.vcf` file which can be achieved by using the following command followed by indexing it.
```
bcftools view -O z -o ERR2093239_filtered.vcf.gz ERR2093239_SNPs_filtered.vcf
bcftools index ERR2093239_filtered.vcf.gz
```
Now we use the zipped file to generate the pseudogenome that will contain the SNPs. Type the following command in the terminal:
```
bcftools consensus -f reference.fa ERR2093239_filtered.vcf.gz > ERR2093239_consensus.fa
```

By default the pseudogenome created will have header similar to reference but we can replace it by using the following command:
```
sed 's|^>.*|>ERR2093239|' ERR2093239_consensus.fa > ERR2093239_pseudogenome.fa
```

Now we have created pseudogenome sequence for the isolate ERR2093239. The next exercise would be to repeat the entire process from 4.1 until 4.4.3 to generate
pseduogenomes for the isolates ERR2093237, ERR2093241 and ERR2093244 using the same reference. Please create a separate folder for each isolate within the 
same directory.

## **Creating a whole-genome alignment** <a name="wgalignment"></a>
The pseudogenome we generated in the above exercise has exactly the same length as the reference, therefore the pseudogenomes can be concatenated to create a
whole genome alignment.
```
cat reference.fa ERR2093239_pseudogenome.fa > concatenated_alignment.fa
# cat reference.fa ERR2093237_pseudogenome.fa ERR2093241_pseudogenome.fa ERR2093244_psedudogenome.fa > concatenated_alignment.fa
```
From the whole genome alignment that we created above we can select just the variable sites (snp-sites) only, this is really helpful when running computationally
intensive processes such as phylogenetic tree generation. We can use the tool [snp-sites](https://github.com/tseemann/snp-sites) for this:
```
snp-sites -o snpsitesOut.fa concatenated_alignment.fa
```
You can determine the length of the alignment using the following bash command:
```
sed -n ‘2p’ snpsitesOut.fa | wc
```

In the above command `-n` allows printing lines, `‘2p’` states 2nd line to print and `wc` counts the words in the line.

Finally, we can use the file with the SNP sites to determine the pairwise genetic distance among all the sequences (3 in this example).
```
snp-dists snpsitesOut.fa >matrix.tsv
```
The output file is a tab-delimited file which displays the pairwise SNP difference as a matrix.

## **Quiz 2**<a name="quiz2"></a>
What is the length of the alignment in `snpsitesOut.fa` file?

# **Using snippy**<a name="snippy"></a>
[`snippy`](https://github.com/tseemann/snippy) is a rapid haploid variant calling and core genome alignment. It was developed by [Torsten Seeman](https://github.com/tseemann) (who by the way has developed a lot of great pipelines and tools). It finds SNPs between a haploid reference genome and NGS sequence reads, and will find both substitutions (SNPs) and insertions/deletions (indels). It is designed with speed in mind, and produces a consistent set of output files in a single folder. 

`snippy` input requirements:
* a reference genome in FASTA or GENBANK format (can be in multiple contigs)
* sequence read file(s) in FASTQ or FASTA format (can be .gz compressed) format
* a folder to put the results in

`snippy` output files (per isolate given as input):
Extension | Description
----------|--------------
.tab | A simple [tab-separated](http://en.wikipedia.org/wiki/Tab-separated_values) summary of all the variants
.csv | A [comma-separated](http://en.wikipedia.org/wiki/Comma-separated_values) version of the .tab file
.html | A [HTML](http://en.wikipedia.org/wiki/HTML) version of the .tab file
.vcf | The final annotated variants in [VCF](http://en.wikipedia.org/wiki/Variant_Call_Format) format
.bed | The variants in [BED](http://genome.ucsc.edu/FAQ/FAQformat.html#format1) format
.gff | The variants in [GFF3](http://www.sequenceontology.org/gff3.shtml) format
.bam | The alignments in [BAM](http://en.wikipedia.org/wiki/SAMtools) format. Includes unmapped, multimapping reads. Excludes duplicates.
.bam.bai | Index for the .bam file
.log | A log file with the commands run and their outputs
.aligned.fa | A version of the reference but with `-` at position with `depth=0` and `N` for `0 < depth < --mincov` (**does not have variants**)
.consensus.fa | A version of the reference genome with *all* variants instantiated
.consensus.subs.fa | A version of the reference genome with *only substitution* variants instantiated
.raw.vcf | The unfiltered variant calls from Freebayes
.filt.vcf | The filtered variant calls from Freebayes
.vcf.gz | Compressed .vcf file via [BGZIP](http://blastedbio.blogspot.com.au/2011/11/bgzf-blocked-bigger-better-gzip.html)
.vcf.gz.csi | Index for the .vcf.gz via `bcftools index`)

`snippy` also has the `snippy-multi` script/pipeline that simplifies running a set of isolate sequences (reads or contigs) against the same reference, and at the end it will also run `snippy-core` at the end to generate the core genome SNP alignment files `core.*`. `snippy-multi` generates these outputs:

Extension | Description
----------|--------------
.aln | A core SNP alignment in the `--aformat` format (default FASTA)
.full.aln | A whole genome SNP alignment (includes invariant sites)
.tab | Tab-separated columnar list of **core** SNP sites with alleles but NO annotations
.vcf | Multi-sample VCF file with genotype `GT` tags for all discovered alleles
.txt | Tab-separated columnar list of alignment/core-size statistics
.ref.fa | FASTA version/copy of the `--ref`
.self_mask.bed | BED file generated if `--mask auto` is used.


## Data preparation<a name="dataprep"></a>
Create the directory where we will be working and `cd` into it. Then download the reads form the Sequence Reads Archive.
```
cd cp5
mkdir -p short_reads
cd short_reads
wget https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR409/005/ERR4095905/ERR4095905_1.fastq.gz
wget https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR409/005/ERR4095905/ERR4095905_2.fastq.gz
wget https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR409/005/ERR4095885/ERR4095885_1.fastq.gz
wget https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR409/005/ERR4095885/ERR4095885_2.fastq.gz
```

Download the Reference genome, which for this case is K. pneumoniae strain cpe058 "" manually as a FASTA file from this [link](). Then rename it with
```
mv sequence.fasta cpe058_Kpn-ST78-NDM1.chr.fasta
```

## Quality control<a name="qcshort"></a>
Use `FastQC` to assess the quality of the sequencing reads.
```
fastqc *.fastq.gz # Do you remember what the "*" wildcard means?
```
Aggregate all the QC results with `MultiQC`.
```
multiqc.
```

## Cleaning the reads (if necessary)<a name="cleaningshort"></a>
Use `Fastp` to remove adapters and low-quality bases.
```
fastp -i ERR4095905_1.fastq.gz -I ERR4095905_2.fastq.gz -o out.ERR4095905_1.fastq.gz -O out.ERR4095905_2.fastq.gz
fastp -i ERR4095885_1.fastq.gz -I ERR4095885_2.fastq.gz -o out.ERR4095885_1.fastq.gz -O out.ERR4095885_2.fastq.gz
```

## Short Read Alignment and SNP calling with snippy<a name="usesnippy"></a>
```
conda activate snippy

#PSA
# snippy --cpus 4 --outdir snippy_output --reference reference.fasta --R1 output_R1_paired.fastq --R2 output_R2_paired.fastq # Syntax
snippy --cpus 4 --outdir ERR4095905_snippy --reference cpe058_Kpn-ST78-NDM1.chr.fasta --R1 out.ERR4095905_1.fastq.gz --R2 out.ERR4095905_2.fastq.gz
snippy --cpus 4 --outdir ERR4095885_snippy --reference cpe058_Kpn-ST78-NDM1.chr.fasta --R1 out.ERR4095885_1.fastq.gz --R2 out.ERR4095885_2.fastq.gz
```
```
#MSA
snippy-core --prefix core --ref cpe058_Kpn-ST78-NDM1.chr.fasta *_snippy # or specify the snippy folders: ERR4095885_snippy ERR4095905_snippy

conda deactivate
```

## **Examining the output**<a name="snippyoutput"></a>
Note the formats and contents of each output file. Compare results, identify key features, and observe any patterns or unexpected findings.

The output directory will contain various files, including:
* `snps.vcf`: the called SNPs in VCF format.
* `snps.tab`: a tabular summary of SNPs.
* `alignment.bam`: the aligned reads in BAM format.
* `alignment.bam.bai`: the BAM index file.

```
# PSA
cd ERR4095905_snippy/
ls
```
```
#MSA
ls core.*
#core.aln core.tab core.tab core.txt core.vcf
grep ">" core.full.aln # view names of aligned genomes
```

## **Post-processing and Analysis (Optional)**<a name=postshort></a>
### **Filtering SNPs**
Apply filters to the VCF files to ensure high-quality SNPs using bcftools. Remove SNPs/Indels with MQ<30 and DP<10.
```
bcftools filter -s LowQual -e '%QUAL<30 || DP<10' ERR4095885_snippy/snps.vcf > ERR4095885_snippy/filtered_snps_short.vcf
bcftools filter -s LowQual -e '%QUAL<30 || DP<10' ERR4095905_snippy/snps.vcf > ERR4095905_snippy/filtered_snps_short.vcf
```

### **Annotation of SNPs** - has not been tested
The `.vcf` file can the be annotated to determine what the effect of each SNP are, i.e. are they silent, do they change something in the amino acid sequence, do they cause a stop codon to be inserted, etc and as a result that change turns a susceptible organism resistant to a specific antimicrobial agent (or an entire class). This can be achieved by using [`snpEff`](https://pcingola.github.io/SnpEff/snpeff/running/).

`snpEff` requires a database to work, and since we do not have it here, we will not perform this step.
```
#short reads
 java -Xmx8g -jar snpEff.jar <reference_database> ERR4095885_snippy/filtered_snps_short.vcf > ERR4095885_snippy/annotated_snps_short.vcf
 java -Xmx8g -jar snpEff.jar <reference_database> ERR4095905_snippy/filtered_snps_short.vcf > ERR4095905_snippy/annotated_snps_short.vcf
```

### Visualization 
The alignment and the SNPs can be visualized using tools such as the [Integrative Genomics Viewer (IGV)](https://igv.org/). A pop-up info of a selected SNP would look like this:
```
ID: .
Chr: NC_009648.1
Position: 2,803,960
Reference: C*
Alternate: T
Qual: 882.977
Type: SNP
Is Filtered Out: No
Alleles:
Alternate Alleles: T
Variant Attributes
QA: 1039
AB: 0
QR: 32
Depth: 30
RO: 1
TYPE: snp
AO: 29
```

Each metric means: 

Field | Description
----------|--------------
ID | This field is empty, indicating no specific identifier (such as a dbSNP ID) is assigned to this SNP.
Chr | NC_009648.1 is the chromosome or contig reference name from the genome assembly.
Position | 2,803,960 is the position on the chromosome where this SNP is located.
Reference | C* indicates the reference allele (the allele found in the reference genome) at this position is "C".
Alternate | T is the alternate allele observed in this SNP, meaning a "C" in the reference is replaced by "T" in the observed variant.
Qual (Quality) | 882.977 is a quality score for the variant call. It indicates the confidence in the variant being true; higher scores mean greater confidence.
Type | SNP specifies that this variant is a single nucleotide polymorphism.
Is Filtered Out | No indicates that this SNP has passed any filters applied during variant calling, suggesting it is considered a reliable call.
Alternate Alleles | T is the alternate allele for this SNP.
QA (Quality of Alternate) | 1039 is the sum of base quality scores for the reads supporting the alternate allele (T). Higher values suggest more confidence in the variant call.
AB (Allele Balance) | 0 represents the proportion of reads supporting the alternate allele relative to the total depth. Since it is 0, this may mean that the calculation could not be performed, or the data isn't available.
QR (Quality of Reference) | 32 is the sum of base quality scores for the reads supporting the reference allele (C). Lower values suggest fewer or less confident reads supporting the reference allele.
Depth | 30 is the total read depth at this position, representing the number of reads covering the SNP site.
RO (Reference Observations) | 1 indicates the number of reads supporting the reference allele (C).
TYPE | snp reaffirms that this variant is a single nucleotide polymorphism.
AO (Alternate Observations) | 29 is the number of reads supporting the alternate allele (T).

# **Long read alignment using minimap2 and SNP calling with Medaka or DeepVariant**
## Data preparation<a name="datapreplong"></a>
Create the directory where we will be working and `cd` into it. Then download the reads form the Sequence Reads Archive.
```
cd cp5 # specify the correct path from whereyer you currenly are.
mkdir -p long_reads
cd long_reads
wget https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR328/004/ERR3284704/ERR3284704.fastq.gz
```

Download the Reference genome, which for this cases is an E. coli strain, manually as a FASTA file from this [link](https://www.ncbi.nlm.nih.gov/nuccore/NZ_HG941718.1?report=fasta). Then rename it with
```
mv sequence.fasta Ecoli_ref.fasta
```

## **Run Medaka**<a name="medaka"></a>
Use `Medaka` to call SNPs from the long-read BAM file.
```
# medaka_variant -i longread.input.fastq.gz -r reference.fasta # Syntax
medaka_variant -i ERR3284704.fastq.gz -r Ecoli_ref.fasta
```
## **Run [DeepVariant](https://github.com/google/deepvariant) (Optional)** - has not been tested<a name="deepvariant"></a>
Use minimap2 for aligning long reads.
```
minimap2 -a reference.fasta long_reads.fastq > aligned_long_reads.sam
```

Convert and sort the alignment.
```
samtools view -S -b aligned_long_reads.sam > aligned_long_reads.bam
samtools sort aligned_long_reads.bam -o sorted_long_reads.bam
```
Index the BAM file.
```
samtools index sorted_long_reads.bam
```
Remove duplicates.
```
samtools rmdup sorted_long_reads.bam deduplicated.bam
```
Use DeepVariant to call SNPs from the long-read BAM file.
```
# Assuming DeepVariant is installed and properly set up
run_deepvariant --model_type PACBIO --ref reference.fasta --reads sorted_long_reads.bam --output_vcf dv_output.vcf --output_gvcf dv_output.g.vcf --num_shards 4
```

## **Use [PEPPER DeepVariant](https://github.com/kishwarshafin/pepper) for nanopore reads: (Optional)** - has not been tested<a name="pepperdeepvariant"></a> 
```
## Pull the docker image.
sudo docker pull kishwars/pepper_deepvariant:r0.8

# Run PEPPER-Margin-DeepVariant
sudo docker run \
-v "${INPUT_DIR}":"${INPUT_DIR}" \
-v "${OUTPUT_DIR}":"${OUTPUT_DIR}" \
kishwars/pepper_deepvariant:r0.8 \
run_pepper_margin_deepvariant call_variant \
-b "${INPUT_DIR}/${BAM}" \
-f "${INPUT_DIR}/${REF}" \
-o "${OUTPUT_DIR}" \
-p "${OUTPUT_PREFIX}" \
-t "${THREADS}" \
--ont_r10_q20
```
## **Post-processing and Analysis (Optional)** - has not been tested<a name="postlong"></a>
### **Filtering SNPs**
Apply filters to the VCF files to ensure high-quality SNPs using bcftools. Remove SNPs/Indels with MQ<30 and DP<10.
```
bcftools filter -s LowQual -e '%QUAL<30 || DP<10' medaka.annotated.vcf > filtered_snps_long.vcf
```

### **Annotation of SNPs**
```
#long reads
java -Xmx8g -jar snpEff.jar reference filtered_snps_long.vcf > annotated_snps_long.vcf
```

# **References**<a name="refs"></a>
Bush SJ, Foster D, Eyre DW, Clark EL, De Maio N, Shaw LP, Stoesser N, Peto TEA, Crook DW, Walker AS, Wilson DJ. (2020). Genomic diversity affects the accuracy of bacterial SNP calling pipelines. Genome Biology, 21, 20. doi: [10.1186/s13059-019-1921-9](https://doi.org/10.1186/s13059-019-1921-9)

Li H. (2018). Minimap2: pairwise alignment for nucleotide sequences. Bioinformatics, 34(18), 3094-3100. doi: [10.1093/bioinformatics/bty191](https://doi.org/10.1093/bioinformatics/bty191)

Poplin R, Chang PC, Alexander D, Schwartz S, Colthurst T, Ku A, Newburger D, Dijamco J, Nguyen N, Afshar PT, Gross SS, Dorfman L, McLean CY, DePristo MA. (2018). A universal SNP and small-indel variant caller using deep neural networks. Nature Biotechnology, 36(10), 983-987. doi: [10.1038/nbt.4235](https://doi.org/10.1038/nbt.4235)

Cingolani P, Platts A, Wang LL, Coon M, Nguyen T, Wang L, Land SJ, Lu X, Ruden DM. (2012). A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff: SNPs in the genome of Drosophila melanogaster strain w1118; iso-2; iso-3. Fly, 6(2), 80-92. doi: [10.4161/fly.19695](https://doi.org/10.4161/fly.19695)

Robinson JT, Thorvaldsdóttir H, Winckler W, Guttman M, Lander ES, Getz G, Mesirov JP. (2011). Integrative genomics viewer. Nature Biotechnology, 29(1), 24-26. doi: [10.1038/nbt.1754](https://doi.org/10.1038/nbt.1754)

Andrews S. (2010). FastQC: A quality control tool for high throughput sequence data. Available online: [http://www.bioinformatics.babraham.ac.uk/projects/fastqc](http://www.bioinformatics.babraham.ac.uk/projects/fastqc)

Ewels P, Magnusson M, Lundin S, Käller M. (2016). MultiQC: summarize analysis results for multiple tools and samples in a single report. Bioinformatics, 32(19), 3047-3048. doi: [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354)
