Link to multiple alignment:
https://drive.google.com/file/d/10M4CitN2mF2toFx9c4IhMA8C2G-9u2LA/view?usp=drive_link 

First, unzip the multiple aligment

```bash
gunzip klemm2018_selected_and_contextual.mfa.gz
```

From now on, adapt the command below to work on the klemm2018_selected_and_contextual.mfa alignment

```bash
seqkit stats Kpn_ST78.cpe058.fas --all --gap-letters "- . N"
```

```bash
snp-sites -c -m -o Kpn_ST78.cpe058.strain_ids.snps.fas Kpn_ST78.cpe058.strain_ids.fas
```

```bash
pairsnp -c Kpn_ST78.cpe058.strain_ids.snps.fas > Kpn_ST78.cpe058.pairsnp.csv
```

Replace the outgroup with XXX

```bash
conda activate gubbins
align="Kpn_ST78.cpe058.strain_ids.fas";
prefix="Kpn_ST78.cpe058.gubbins";
run_gubbins.py $align --prefix $prefix --use-time-stamp --threads 4 --first-tree-builder fasttree --tree-builder raxml --outgroup Germany_2019_Kpn_ST78
```

```bash
ls -l Kpn_ST78.cpe058.gubbins*
```

```bash
mask_gubbins_aln.py --aln Kpn_ST78.cpe058.strain_ids.fas --gff Kpn_ST78.cpe058.gubbins.recombination_predictions.gff --out Kpn_ST78.cpe058.rmRCB.fas
conda deactivate
```

```bash
iqtree2 -s Kpn_ST78.cpe058.rmRCB.fas -T 4 --mem 4G --ufboot 1000 --prefix Kpn_ST78.cpe058.rmRCB_iqtree -wbtl
```
