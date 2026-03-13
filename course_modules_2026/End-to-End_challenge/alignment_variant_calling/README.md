Commands to be adapted:

cd /home/data/data/end-to-end/
mkdir snippy
cd snippy

### Replace sample Id ERR4095885 with your assigned sample Id
### Replace the reference file below (cpe058_Kpn-ST78-NDM1.chr.fasta) with the following one: 22420_1_10_Pak60006_2016.LT882486.1.fasta

fastp -i ERR4095885_1.fastq.gz -I ERR4095885_2.fastq.gz -o out.ERR4095885_1.fastq.gz -O out.ERR4095885_2.fastq.gz

snippy --cpus 4 --outdir ERR4095885_snippy --reference cpe058_Kpn-ST78-NDM1.chr.fasta --R1 out.ERR4095885_1.fastq.gz --R2 out.ERR4095885_2.fastq.gz

python3 create_snippy_consensus.py --reference pe058_Kpn-ST78-NDM1.chr.fasta --consensus_subs ./ERR4095885_snippy/snps.consensus.subs.fa --aligned ./ERR4095885_snippy/snps.aligned.fa --output ERR4095885.consensus.fa --sample_id ERR4095885 --mapping_stats ERR4095885.consensus.stats.csv



