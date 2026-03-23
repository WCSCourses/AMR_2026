# <img src="https://coursesandconferences.wellcomeconnectingscience.org/wp-content/themes/wcc_courses_and_conferences/dist/assets/svg/logo.svg" width="300" height="50"> 
# Antimicrobial Resistance in Bacterial Pathogens - Africa Informatics Guide 2026


## Docker Command Summary 
| Command                                | Description                                                                                           |
|----------------------------------------|-------------------------------------------------------------------------------------------------------|
| `docker --version`                     | Displays the installed version of Docker.                                                              |
| `docker run hello-world`               | Runs the "hello-world" container to verify Docker is installed and functioning.                        |
| `docker ps`                            | Lists all running containers.                                                                          |
| `docker ps -a`                         | Lists all containers, including stopped ones.                                                          |
| `docker pull <image_name>`             | Pulls a Docker image from Docker Hub.                                                                  |
| `docker run -i -t <image_name> /bin/bash` | Runs a container in interactive mode with a Bash shell.                                                |
| `docker stop <container_id_or_name>`   | Stops a running container.                                                                            |
| `docker rm <container_id_or_name>`     | Removes a container (must be stopped first).                                                           |
| `docker rmi <image_name_or_id>`        | Removes a Docker image from your local machine.                                                       |
| `docker images`                        | Lists all Docker images installed locally.                                                             |
| `docker image prune`                   | Removes unused (dangling) Docker images to free up space.                                             |
| `docker logs <container_id_or_name>`   | Displays the logs of a running or stopped container.                                                   |
| `docker start <container_id_or_name>`  | Starts a stopped container.                                                                           |
| `docker stats`                         | Displays real-time statistics for running containers (CPU, memory usage, etc.).                       |
| `docker build -t <image_name> .`       | Builds a Docker image from a Dockerfile in the current directory.                                      |
| `docker image import <file>`           | Imports a Docker image from a previously exported file (typically a .tar file).                                      |
| `docker run --link <container_name>`   | Links one container to another, allowing them to communicate.                                          |
| `docker-compose up`                    | Starts multi-container applications defined in a `docker-compose.yml` file.                           |
| `docker info`                          | Displays detailed information about the Docker installation and system.                               |
| `docker --version`                     | Shows the installed version of Docker.                                                                 |

### Specific Commands to Run During the Course

Start the Docker engine if stopped (Click Docker icon and wait a short while), open a terminal (e.g. Windows PowerShell) and run:

`docker run -i -t --mount type=bind,source=C:\Users\User\Desktop\amr25_data,target=/home/data amr:Dockerfile`

Note: This is for Windows PCs. Syntax varies for Mac and Linux. The location after source may vary for Overflow Room participants.

Once your docker image is running, you will need to change directory (cd) into the data directory for the course:

`cd /home/data/data`


### Helpful Links for Docker

| Resource | Description |
|----------|-------------|
| [Docker Official Documentation](https://docs.docker.com/) | The official Docker documentation with comprehensive guides, tutorials, and reference material. |
| [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/docker/) | A reference guide for all Docker commands available in the command-line interface (CLI). |
| [Docker Cheatsheet](https://dockerlabs.collabnix.com/docker/cheatsheet/) | A quick reference guide for common Docker commands and usage scenarios. |
| [Docker for Beginners - YouTube](https://www.youtube.com/watch?v=3c-iBn73dDE) | A YouTube video tutorial that helps you get started with Docker by building a simple project. |
| [Docker Community Forums](https://forums.docker.com/) | Docker's official community forums where you can ask questions and get help from other Docker users. |

If you encounter any issues while using Docker or working with related tools, don't hesitate to search for solutions online. A quick Google search often leads to useful documentation, forums, or blog posts that can help you resolve the problem. Additionally, if you need further assistance, feel free to ask [ChatGPT](https://chatgpt.com/) for support. 

**Software used during the course**      
| Software | Version | Module | Notes |
|-------------|---------|--------|-------|
| [Porechop](https://github.com/rrwick/Porechop) | 0.2.4 | Assembly | |
| [NanoPlot](https://github.com/wdecoster/NanoPlot) | 1.40.0 | Assembly | |
| [Flye](https://github.com/fenderglass/Flye) | 2.9 | Assembly | |
| [Unicycler](https://github.com/rrwick/Unicycler) | 0.4.9 | Assembly | |
| [Prokka](https://github.com/tseemann/prokka) | 1.14.6 | Assembly/Annotation | |
| [Medaka](https://github.com/nanoporetech/medaka) | 1.6.0 | | |
| [Polypolish](https://github.com/rrwick/Polypolish/wiki/Installation) | 0.5.0 | | |
| [BWA](https://sourceforge.net/projects/bio-bwa/files/) | 0.7.17 | Variant calling | |
| [Samtools](https://sourceforge.net/projects/samtools/files/samtools/) | 1.15 | | |
| [BCFtools](https://sourceforge.net/projects/samtools/files/samtools/) | 1.15 | Variant calling | |
| [Artemis](https://www.sanger.ac.uk/tool/artemis/) | 18.1.0 | | |
| [Shovill](https://github.com/tseemann/shovill) | 1.1.0 | Assembly | |
| [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) | 0.11.9 | Data QC | |
| [Minimap2](https://github.com/lh3/minimap2) | 2.24 | | |
| [Racon](https://github.com/isovic/racon) | 1.4.20 | | |
| [Quast](https://quast.sourceforge.net/install.html) | 5.0.2 | Assembly | |
| [Bandage](http://rrwick.github.io/Bandage/) | 0.8.1 | Assembly | |
| [Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic) | 0.39 | Data QC | |
| [Trycycler](https://github.com/rrwick/Trycycler) | 0.5.3 | Assembly | |
| [SNP-sites](https://github.com/sanger-pathogens/snp-sites) | 2.5.1 | Variant calling | |
| [SNP-dists](https://github.com/tseemann/snp-dists) | 0.7.0 | Variant calling | |
| [AMRFinder](https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/AMRFinder/) | 3.10.45 | AMR Prediction | |
| [CARD RGI](https://github.com/arpcard/rgi) | 5.2.0 | AMR Prediction | |
| [ResFinder](https://bitbucket.org/genomicepidemiology/resfinder/src/master/) | 4.1 | AMR Prediction | |
| [fasterq-dump](https://github.com/ncbi/sra-tools) | 2.11.0 | Fastq download | |
| [Fastp](https://github.com/OpenGene/fastp) | 0.23.2 | | |
| [MEGA](https://www.megasoftware.net/) | 11.0.13 | Phylogenetics | |
| [IQ-TREE 2](http://www.iqtree.org/) | 2.1.4 | Phylogenetics | |
| [Figtree](http://tree.bio.ed.ac.uk/software/figtree/) | 1.4.4 | Phylogenetics | |
| [SplitsTree](https://software-ab.cs.uni-tuebingen.de/download/splitstree6/welcome.html) | 6.0 | Phylogenetics | |
| [MultiQC](https://multiqc.info/modules/) | 1.11 | Metagenomics CLI | |
| [Hocort](https://github.com/ignasrum/hocort) | 1.0.0 | Metagenomics CLI | (own env) |
| [Kraken2](https://github.com/DerrickWood/kraken2) | 2.1.2 | Metagenomics CLI | |
| [Bracken](https://ccb.jhu.edu/software/bracken/) | 2.6.2 | Metagenomics CLI | |
| [Krona](https://github.com/marbl/Krona) | 2.8 | Metagenomics CLI | |
| [SPAdes](https://github.com/ablab/spades) | 3.15.4 | Metagenomics CLI | |
| [KMA](https://anaconda.org/bioconda/kma) | 1.4.1 | Metagenomics CLI | |
| [Kraken2 Standard Database](https://benlangmead.github.io/aws-indexes/k2) | | Metagenomics CLI | |
| [ResFinder DB](https://bitbucket.org/genomicepidemiology/resfinder/src/master/) | | Metagenomics CLI | |
| [SeqTK](https://github.com/lh3/seqtk) | 1.3 | Metagenomics | |
| [Abricate](https://github.com/tseemann/abricate) | 1.0.1 | Metagenomics | |
| [MetaBAT2](https://bitbucket.org/berkeleylab/metabat/src/master/) | 2.15 | Metagenomics | |
| [CheckM](https://github.com/Ecogenomics/CheckM) | 1.1.3 | Metagenomics | |
| [BBMap](https://sourceforge.net/projects/bbmap/) | 38.90 | Metagenomics | |
| [Snippy](https://github.com/tseemann/snippy) | 4.6.0 | Mapping | |
| [create_snippy_consensus.py](https://github.com/francesccoll/scripts/blob/main/create_snippy_consensus.py) | | Phylogenetics | |
| [SeqKit](https://bioinf.shenwei.me/seqkit/) | 2.0.0 | Phylogenetics | |
| [replace_fasta_ids.py](https://github.com/francesccoll/scripts/blob/main/replace_fasta_ids.py) | | Phylogenetics | |
| [Gubbins](https://github.com/nickjcroucher/gubbins) | 3.2 | Phylogenetics | |
| [PairSNP](https://github.com/gtonkinhill/pairsnp) | | Phylogenetics | |
| [RAxML](https://cme.h-its.org/exelixis/web/software/raxml/index.html) | | Phylogenetics | |
| [Screen](https://www.gnu.org/software/screen/) | | General Use | |

## Citing and Re-using Course Material

The course data are free to reuse and adapt with appropriate attribution. All course data in these repositories are licensed under the <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)</a>. <a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /> 

Each course landing page is assigned a DOI via Zenodo, providing a stable and citable reference. These DOIs can be found on the respective course landing pages and can be included in CVs or research publications, offering a professional record of the course contributions.

## Interested in attending a course?

Take a look at what courses are coming up at [Wellcome Connecting Science Courses & Conference Website](https://coursesandconferences.wellcomeconnectingscience.org/our-events/).

---

[Wellcome Connecting Science GitHub Home Page](https://github.com/WCSCourses) 

For more information or queries, feel free to contact us via the [Wellcome Connecting Science website](https://coursesandconferences.wellcomeconnectingscience.org).<br /> 
Find us on socials [Wellcome Connecting Science Linktr](https://linktr.ee/eventswcs)

---
