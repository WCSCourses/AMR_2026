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
Begin by downloading a file from these two files from [here]() and [here]() using commands we have just dicussed in previous class.

3. After downloading the `alice.txt` file, explain what the following commands do:
a) `head alice.txt -n 20 > alice20.txt`
b) `grep -c -E "^>" alice.txt`
c) `wc -L alice.txt`
d) `cat alice20.txt | tr -d 'AEIOUaeiou'` 

4. Still will the `alice.txt` file, write both the command and the response:
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

# Answers
## Linux file system and files manipulation
1. as
2. 
## Linux text processing tools
3.a
3.b.
3.c.
3.d.
4.a.
4.b.
4.c.
5.a. `grep -c -E "^>" samplefasta.fasta`
5.b. `wc -L samplefasta.fasta` 
