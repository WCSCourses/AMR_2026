# 🧬Command Line Cheat Sheet  
**Module Developers:** Collins Kigen, Augusto Messa Jr., Silondiwe Nzimande, Miriam Mwamba

---

## 1. Navigation — Always Know Where You Are

| Command | Description |
|----------|------------|
| `pwd` | Print current working directory |
| `ls` | List files and directories |
| `ls -lh` | Long format + human-readable file sizes |
| `ls -a` | Show hidden files |
| `cd <dir>` | Change directory |
| `cd ..` | Move up one level |
| `cd ~` | Go to home directory |

### Always start analysis with:
```bash
pwd
ls -lh
```

---

## 2. File & Directory Management

| Command | Description |
|----------|------------|
| `mkdir <dir>` | Create a directory |
| `mkdir -p <dir/subdir>` | Create nested directories |
| `touch <file>` | Create empty file |
| `cp <src> <dest>` | Copy file |
| `mv <src> <dest>` | Move or rename file |
| `rm <file>` | Remove file |
| `rm -r <dir>` | Remove directory and its contents |

### Dangerous command
```bash
rm -r *
```
Deletes **everything** in the current directory.

---

## 3. Viewing Files (FASTQ / FASTA Safe)

| Command | Best Used For |
|----------|--------------|
| `head <file>` | First 10 lines |
| `tail <file>` | Last 10 lines |
| `less <file>` | Scroll large files |
| `cat <file>` | Small files only |
| `zcat <file.gz>` | View compressed files |

### Example (Sequencing Data)
```bash
zcat sample.fastq.gz | head
```

Do **not** use `cat` on large FASTQ files.

---

## 4. Searching & Counting

| Command | Purpose |
|----------|----------|
| `grep "text" file` | Search for text |
| `grep -r "text" dir/` | Recursive search |
| `wc -l file` | Count lines |
| `zcat file.gz \| wc -l` | Count lines in compressed file |

### Count FASTQ Reads
```bash
zcat sample.fastq.gz | wc -l
```
FASTQ reads = total lines ÷ 4

---

## 5. Permissions & Scripts

| Command | Description |
|----------|------------|
| `ls -l` | View file permissions |
| `chmod +x script.sh` | Make script executable |
| `./script.sh` | Run script |

Permission example:
```
-rwxr-xr--
```

---

## 6. Help & Self-Sufficiency

| Command | Description |
|----------|------------|
| `man <command>` | Full manual |
| `<command> --help` | Quick help |
| `history` | Show previous commands |

Exit manual:
```
q
```

---

## 7. Productivity Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Auto-complete |
| `Ctrl + C` | Stop running process |
| `Ctrl + L` | Clear screen |
| `↑` | Previous command |
| `Ctrl + R` | Search command history |

---

## 8. Recommended Project Structure

```
AMR_project/
│
├── raw_data/
├── qc/
├── assembly/
├── annotation/
└── results/
```

Create instantly:
```bash
mkdir -p AMR_project/{raw_data,qc,assembly,annotation,results}
```

---

## Golden Rules for This Course

1. Always know where you are → `pwd`
2. Always check files → `ls -lh`
3. Keep directories organized
4. Use `--help` before asking
5. Never delete without checking
6. Never run tools in the wrong directory

---

## Core Commands You’ll Use Throughout this course

```
pwd
ls -lh
cd
mkdir
cp
mv
rm
head
tail
less
zcat
grep
wc
chmod
```

---

