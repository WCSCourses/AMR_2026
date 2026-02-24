# Conda Cheat Sheet  
**Module Developers:** Collins Kigen, Augusto Messa Jr., Silondiwe Nzimande, Miriam Mwamba

---

## 1. Check Conda & System Info

| Command | Description |
|---------|-------------|
| `conda --version` | Show Conda version |
| `conda info` | Show Conda installation + env details |
| `conda config --show` | Show Conda configuration |
| `conda config --show channels` | Show configured channels |

---

## 2. Environment Management (Core Skills)

| Command | Description |
|---------|-------------|
| `conda env list` | List all environments |
| `conda create -n <env>` | Create a new environment |
| `conda create -n <env> python=3.10` | Create env with specific Python version |
| `conda activate <env>` | Activate environment |
| `conda deactivate` | Exit current environment |
| `conda remove -n <env> --all` | Delete an environment |



---

## 3. Installing Packages

| Command | Description |
|---------|-------------|
| `conda search <pkg>` | Search for a package |
| `conda install <pkg>` | Install a package |
| `conda install <pkg1> <pkg2>` | Install multiple packages |
| `conda install -c conda-forge <pkg>` | Install from conda-forge |
| `conda install -c bioconda <pkg>` | Install from bioconda |

### Example (Bioinformatics Tools)
```bash
conda install -c bioconda fastqc fastp porechop filtlong nanoqc
```

---

## 4. Updating Packages & Conda

| Command | Description |
|---------|-------------|
| `conda update conda` | Update Conda itself |
| `conda update <pkg>` | Update a specific package |
| `conda update --all` | Update all packages in current env |

---

## 5. Listing & Removing Packages

| Command | Description |
|---------|-------------|
| `conda list` | List installed packages in active environment |
| `conda list | grep <pkg>` | Find a specific package (Linux/macOS) |
| `conda remove <pkg>` | Uninstall a package |

---

## 6. Channels (Very Important in Bioinformatics)

Bioinformatics tools often come from **bioconda** and **conda-forge**.

| Command | Description |
|---------|-------------|
| `conda config --add channels conda-forge` | Add conda-forge channel |
| `conda config --add channels bioconda` | Add bioconda channel |
| `conda config --set channel_priority strict` | Use strict channel priority (recommended) |

### Recommended channel setup
```bash
conda config --add channels conda-forge
conda config --add channels bioconda
conda config --set channel_priority strict
```

---

## 7. Exporting & Reproducing Environments (For Reproducibility)

| Command | Description |
|---------|-------------|
| `conda env export > env.yml` | Export environment to YAML |
| `conda env create -f env.yml` | Create environment from YAML |

### Example
```bash
conda env export > amr_env.yml
conda env create -f amr_env.yml
```

---

## 8. Best Practices for This Course

**DO**
- Create one environment per workflow/toolset
- Use `bioconda` for bioinformatics tools
- Keep environments clean and task-specific

**AVOID**
- Installing everything into `base`
- Mixing `pip` and `conda` unless necessary
- Random channel mixing without `strict` priority

---

## 9. Help & Troubleshooting

| Command | Description |
|---------|-------------|
| `conda --help` | Show general help |
| `conda <command> --help` | Help for a specific command |
| `conda clean --all` | Clean cache (fixes storage issues sometimes) |

---

## Core Conda Commands You’ll Use Throughout this course

```
conda env list
conda create -n <env> python=3.10
conda activate <env>
conda install -c bioconda <tool>
conda list
conda deactivate
```

---

