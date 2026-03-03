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
Begin by downloading a file from this [link]() using commands we have just dicussed in previous class.

1. Explain what the following commands do
a) `head alice.txt -n 20 > alice20.txt`
b) `grep -c -E "^>" alice.txt`
c) `wc -L alice.txt`
d) `cat alice20.txt | tr -d 'AEIOUaeiou'` 

2. How many characters are within the `alice.txt` file
