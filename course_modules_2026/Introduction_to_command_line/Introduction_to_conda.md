# Practical: Installing and Using Conda for Bioinformatics

## Objective

In this practical you will:

1. Install Miniconda
2. Configure Conda channels
3. Create a Conda environment
4. Install a bioinformatics tool (**FastQC**)
5. Verify the tool works

---

# Step 1: Download Miniconda

Download the Miniconda installer for Linux:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Check that the file downloaded correctly:

```bash
ls -lh
```

You should see a file similar to:

```
Miniconda3-latest-Linux-x86_64.sh
```

---

# Step 2: Install Miniconda

Run the installer:

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

Follow the prompts:

1. Press **Enter** to read the license
2. Type **yes** to accept the license
3. Choose installation location (default is usually fine)
4. Type **yes** when asked to initialize Conda

---

# Step 3: Activate Conda

Reload your shell configuration:

```bash
source ~/.bashrc
```

Check that Conda is installed:

```bash
conda --version
```

Example output:

```
conda 24.x.x
```

---

# Step 4: Configure Bioinformatics Channels

Conda installs bioinformatics tools from special repositories called **channels**.

Add the recommended channels:

```bash
conda config --add channels conda-forge
conda config --add channels bioconda
conda config --set channel_priority strict
```

Check channels:

```bash
conda config --show channels
```

---

# Step 5: Create a Conda Environment

Create an environment for this course:

```bash
conda create -n fastqc
```

Activate the environment:

```bash
conda activate fastqc
```

Your terminal should now show:

```
(fastqc)
```

---

# Step 6: Install FastQC

Install **FastQC** from Bioconda:

```bash
conda install fastqc
```

Confirm installation:

```bash
fastqc --version
```

Example output:

```
FastQC v0.11.x
```

---

# Step 7: Verify

Download a small FASTQ file:

```
fastqc --help
```

- GC content
- Sequence length distribution
- Adapter contamination

---

