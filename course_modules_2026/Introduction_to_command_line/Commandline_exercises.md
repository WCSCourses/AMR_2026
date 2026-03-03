# Computational Practical 1 - Introduction to Command Line and Unix - Exercises
Developed by: Collins Kigen, Augusto Messa Jr., Silondiwe Nzimande and Miriam Mwama

# Linux file system and files manipulation
Go to your home directory, create a directory called _cp1_exercises_ and go into it using the **_cd_** command. Then create 5 files by executing the following command:
```
touch file1.txt file2.txt file3.txt fileA.dat fileB.txt
```
1. Write the commands necessary as to:
* Create a directory named "new" within the _cp1_exercises_.
* Copy all files created to the new directory at once (hint: use the wildcards we discussed earlier).

2. Write the commands necessary to:
* Change the name of the _new_ directory to "old".
* Change the name of _file1.txt_ to "file4.txt".


# Linux text processing tools
Begin by downloading a file from these two files [alice.txt](https://github.com/WCSCourses/AMR_2026/blob/aemjunior-patch-1/course_modules_2026/Introduction_to_command_line/alice.txt) and [samplefasta.fasta](https://github.com/WCSCourses/AMR_2026/blob/aemjunior-patch-1/course_modules_2026/Introduction_to_command_line/samplefasta.fasta) using commands we have just dicussed in previous class.

3. After downloading the `alice.txt` file, explain what the following commands do:
a) `head alice.txt -n 100 > alice100.txt`

b) `grep -c -E "^the" alice.txt`

c) `wc -l alice.txt`

d) `cat alice100.txt | tr -d 'AEIOUaeiou'` 

4. Still with the `alice.txt` file, write both the command and the response:
a) How many characters are within the `alice.txt` file?

b) How many instances of the word "the" are within the `alice.txt` file? 

c) What is the difference with the `grep -cw "the" alice.txt` and the command you wrote in the previous question?

5. The `samplefasta.fasta` is a file with DNA sequences in FASTA format (we discussed this in the previous module).
Reminder, this is their structure:
```
>Sequence1
ACGTTCGAGATTACA
```
a) How many FASTA records are within the file?

b) What is the size of the largest sequence within that file?

6. Bonus questions:
a) Compute the total amount of As, C, Gs, Ts and Ns in the `samplefasta.fasta` using pipes and redirections (A.K.A a one-liner)?
b) What is the GC content? 

# Answers - for your own benefit, try completing the exercises and getting the responses by your self first, then compare them with these.
## Linux file system and files manipulation
| Question | Answer |
| --- | --- |
| 1 | `mkdir -p cp1_exercises/new`; then `touch file1.txt file2.txt file3.txt fileA.dat fileB.txt`; then `cp file* new/` |
| 2 | From within _cp1_exercises_, `mv new old` and from within the _old_ directory (just renamed as such) `mv file1.txt file4.txt` |

## Linux text processing tools
| Question | Answer |
| --- | --- |
| 3a | It takes the first 100 lines from the _alice.txt_ file, then redirects the output (instead of printing it to the screen/STDOUT) to the file _alice100.txt_ (which is created by this command) |
| 3b | Counts the number of lines that start with the word "the". There are 88 instances |
| 3c | It counts the number of lines contained in the _alice.txt_ file |
| 3d | Removes all the vowels from the text and prints it to the screen |
| 4a | `wc -c alice.txt`; There are 151191 characters |
| 4b | `grep -c "the" alice.txt`. There are 1433 instances |
| 4c | It counts just the instances where "the" is a word; i.e. it does not count instances such as "o**the**r", "ei**the**r", etc |
| 5a | `grep -c -E "^>" samplefasta.fasta`. There are 100 FASTA records (sequences) |
| 5b | `wc -L samplefasta.fasta`. The largest lenght sequence has 100 characters. The file is pretty much uniform, so we can try again with another file |
| 6a | `cat samplefasta.fasta \| grep -vE "^>" \| fold -w 1 \| sort \| uniq -c`. Which returns 3062 As, 2020 Cs, 2064 Gs, 13 Ns and 2841 Ts |
| 6b | 40.84% |


# This is redundant (already in the tables), ignore it.
## Linux file system and files manipulation
1. `mkdir -p cp1_exercises/new`; then `touch file1.txt file2.txt file3.txt fileA.dat fileB.txt`; then `cp file* new/`.
2. From within _cp1_exercises_, `mv new old` and from within the _old_ directory (just renamed as such) `mv file1.txt file4.txt`.

## Linux text processing tools
3.a. It takes the first 100 lines from the _alice.txt_ file, then redirects the output (instead of printing it to the screen/STDOUT) to the file _alice100.txt_ (which is created by this command).

3.b. Counts the number of lines that start with the word "the". There are 88 instances.

3.c. It counts the number of lines contained in the _alice.txt_ file.

3.d. Removes all the vowels from the text and prints it to the screen.

4.a. `wc -c alice.txt`; There are 151191 characters.

4.b. `grep -c "the" alice.txt`. There are 1433 instances.

4.c. It counts just the instances where "the" is a word; i.e. it does not count instances such as "o**the**r", "ei**the**r", etc.

5.a. `grep -c -E "^>" samplefasta.fasta`. There are 100 FASTA records (sequences).

5.b. `wc -L samplefasta.fasta`. The largest lenght sequence has 100 characters. The file is pretty much uniform, so we can try again with another file.

6.a. `cat samplefasta.fasta | grep -vE "^>" | fold -w 1 | sort | uniq -c`. Which returns 3062 As, 2020 Cs, 2064 Gs, 13 Ns and 2841 Ts.

6.b. 40.84%

