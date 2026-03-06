# Computational Practical 1 - Introduction to Command Line and Unix - Exercises
Developed by: Collins Kigen, Augusto Messa Jr., Silondiwe Nzimande and Miriam Mwama

# Linux file system and files manipulation
Go to your home directory, create a directory called _cp2_exercises_ and go into it using the **_cd_** command. 

1. Create the following 5 files: `file1.txt file2.txt file3.txt fileA.dat fileB.txt`

2. Write the commands necessary as to:

    a) Create a directory named "new" within the _cp2_exercises_.

    b) Copy all files created to the new directory at once (hint: use the wildcards we discussed earlier).

4. Write the commands necessary to:

    a) Change the name of the _new_ directory to "old".

    b) Change the name of _file1.txt_ to "file4.txt".


# Linux text processing tools
Begin by downloading a file from these two files [alice.txt](https://github.com/WCSCourses/AMR_2026/blob/aemjunior-patch-1/course_modules_2026/Introduction_to_command_line/images_and_data/alice.txt) and [samplefasta.fasta](https://github.com/WCSCourses/AMR_2026/blob/aemjunior-patch-1/course_modules_2026/Introduction_to_command_line/images_and_data/samplefasta.fasta) using commands we have just dicussed in previous class.

4. After downloading the `alice.txt` file, explain what the following commands do:

    a) `head alice.txt -n 100 > alice100.txt`

    b) `grep -c -E "^the" alice.txt`

    c) `wc -l alice.txt`

    d) `cat alice100.txt | tr -d 'AEIOUaeiou'` 

5. Still with the `alice.txt` file, write both the command and the response:

    a) How many characters are within the `alice.txt` file?

    b) How many instances of the word "the" are within the `alice.txt` file? 

    c) What is the difference with the `grep -cw "the" alice.txt` and the command you wrote in the previous question?

6. The `samplefasta.fasta` is a file with DNA sequences in FASTA format (we discussed this in the previous module).
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


7. Bonus questions:

    a) Compute the total amount of As, C, Gs, Ts and Ns in the `samplefasta.fasta` using pipes and redirections (A.K.A a one-liner)?

    b) What is the GC content? 

# Answers - for your own benefit, try completing the exercises and getting the responses by your self first, then compare them with these.
## Linux file system and files manipulation
| Question | Answer |
| --- | --- |
| 1 | `mkdir cp1_exercises` then `cd cp1_exercises` and finally `touch file1.txt file2.txt file3.txt fileA.dat fileB.txt` |
| 2 | `mkdir -p cp1_exercises/new`; then `touch file1.txt file2.txt file3.txt fileA.dat fileB.txt`; then `cp file* new/` |
| # | From within _cp1_exercises_, `mv new old` and from within the _old_ directory (just renamed as such) `mv file1.txt file4.txt` |

## Linux text processing tools
| Question | Answer |
| --- | --- |
| 4a | It takes the first 100 lines from the _alice.txt_ file, then redirects the output (instead of printing it to the screen/STDOUT) to the file _alice100.txt_ (which is created by this command) |
| 4b | Counts the number of lines that start with the word "the". There are 88 instances |
| 4c | It counts the number of lines contained in the _alice.txt_ file |
| 4d | Removes all the vowels from the text and prints it to the screen |
| 5a | `wc -c alice.txt`; There are 151191 characters |
| 5b | `grep -c "the" alice.txt`. There are 1433 instances |
| 5c | It counts just the instances where "the" is a word; i.e. it does not count instances such as "o**the**r", "ei**the**r", etc |
| 6a | `grep -c -E "^>" samplefasta.fasta`. There are 100 FASTA records (sequences) |
| 6b | `wc -L samplefasta.fasta`. The largest lenght sequence has 100 characters. The file is pretty much uniform, so we can try again with another file |
| 6c | `echo $(cat samplefastq.fastq \| wc -l) / 4 \| bc` |
| 7a | `cat samplefasta.fasta \| grep -vE "^>" \| fold -w 1 \| sort \| uniq -c`. Which returns 3062 As, 2020 Cs, 2064 Gs, 13 Ns and 2841 Ts |
| 7b | 40.84% |


