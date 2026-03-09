# Computational Practical 1 - Introduction to Command Line and Unix - Exercises
Developed by: Collins Kigen, Augusto Messa Jr., Silondiwe Nzimande and Miriam Mwama
## Open Terminal, the run this command to activate docker
```
docker run -it --mount "type=bind,source=C:\Users\User\Desktop\amr25_data,target=/home/data/" amr:Dockerfile
```

## Linux file system and files manipulation
Go to your home cp2 directory
```
cd /home/data/data/cp2
```

### Question 1: Create a directory called _cp2_exercises_ and go into it using the **_cd_** command. 

Note: In Bash, spaces act as argument separators. Don't use spaces in names!!

### Question 2: Create the following 5 files: `file1.txt file2.txt file3.txt fileA.dat fileB.txt`

### Question 3: Create a directory named "new" within the _cp2_exercises_.

### Question 4: Copy all files created to the new directory at once (hint: use the wildcards we discussed earlier).

### Question 5: Change the name of the _new_ directory to "old".

### Question 6: Change the name of _file1.txt_ to "file4.txt".

### Question 6b: Delete `file2.txt file3.txt file4.txt fileA.dat fileB.txt`


# Linux text processing tools
Begin by downloading a file from these two files 

1. [alice.txt](https://github.com/WCSCourses/AMR_2026/blob/aemjunior-patch-1/course_modules_2026/Introduction_to_command_line/images_and_data/alice.txt)

```
wget https://raw.githubusercontent.com/WCSCourses/AMR_2026/refs/heads/aemjunior-patch-1/course_modules_2026/Introduction_to_command_line/images_and_data/alice.txt
```
2. [samplefasta.fasta](https://github.com/WCSCourses/AMR_2026/blob/aemjunior-patch-1/course_modules_2026/Introduction_to_command_line/images_and_data/samplefasta.fasta) using commands we have just dicussed in previous class.
```
wget https://raw.githubusercontent.com/WCSCourses/AMR_2026/refs/heads/aemjunior-patch-1/course_modules_2026/Introduction_to_command_line/images_and_data/samplefasta.fasta
```
### Question 7: After downloading the `alice.txt` file, explain what the following commands do:

    a) head -n 100  alice.txt > alice100.txt
    

    b) grep -c -E "^the" alice.txt
    

    c) wc -l alice.txt

    d) wc -l alice100.txt
    

    d) cat alice100.txt | tr -d 'AEIOUaeiou' 

### Question 8: Still with the `alice.txt` file, write both the command and the response:

    a) How many characters are within the `alice.txt` file?

    b) How many instances of the word "the" are within the `alice.txt` file? 

    c) What is the difference with the `grep -cw "the" alice.txt` and the command you wrote in the previous question?

### Question 9: The `samplefasta.fasta` is a file with DNA sequences in FASTA format (we discussed this in the previous module).
Reminder, this is their structure:

```
>Sequence1
ACGTTCGAGATTACA
``` 

Answer the following questions: 
 
 a) How many FASTA records are within the file?
    
 b) What is the size of the largest sequence within that file?
 
 c) If it was a FASTQ file (see example below), how would you modify the previous commands to get the same information?

![Example FASTQ file.](https://github.com/WCSCourses/AMR_2026/blob/aemjunior-patch-1/course_modules_2026/Introduction_to_command_line/images_and_data/pone.0155461.g001.png)


### Question 10: Bonus questions:

    a) Compute the total amount of As, C, Gs, Ts and Ns in the `samplefasta.fasta` using pipes and redirections (A.K.A a one-liner)?

    b) What is the GC content? 

### Bonus question
#### Exercise: Creating a Journal Directory Structure

#### Task

Create a **journal directory structure** for one year.

1. Create a directory called `journal` and `cd` into it.
2. Inside `journal`, create **12 directories** with one liner command, one for each month:

```
month01  month02  month03  month04
month05  month06  month07  month08
month09  month10  month11  month12
```

3. Inside **each month directory**, create **30 text files** with one liner command, one for each day of the month.

The files should be named:

```
day01.txt
day02.txt
day03.txt
...
day30.txt
```

Assume **every month has 30 days**.

---

### Expected Structure

```
journal/
├── month01/
│   ├── day01.txt
│   ├── day02.txt
│   └── ...
├── month02/
│   ├── day01.txt
│   ├── day02.txt
│   └── ...
...
└── month12/
    ├── day01.txt
    ├── day02.txt
    └── day30.txt
```

---

### Verification

Run the following command to confirm the structure:

```bash
ls -R journal
```

You should see **12 directories**, each containing **30 text files**.












