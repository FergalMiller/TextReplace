# Text Replacer

Incredibly simple, but universally useful text replacement Python application.

Text Replacer is an easy to use program to quickly replace large amounts of text in as many files as you would like.
It is easy to modify and generate your own re-writer modules and include them in the project.

## How it works

Text Replacer uses two profiles to complete a text rewrite;
A run profile and and a file rewrite profile.
Each profile takes a set of arguments to affect its behaviour.
Some arguments are required.

### Run profiles
The run profile carries out a set of instructions and invokes a file rewrite profile.
Two run profiles are supplied as default:

`-s` Single file run profile
- arg: `-p` the path of the file to be rewritten
    - example: `-p /Users/my.user/Documents/mydocument.txt`
    - example (running from the Documents directory): `-p mydocument.txt`
    

`-b` Bulk file run profile
- arg: `-d` the directory to traverse to find files within
    - example: `-d /Users/my.user/Documents/`
- arg: `-e` a file extension filter
    - example: `-e txt`
- arg: `-r` a regex pattern  filter for file names 
    - example: `-r document$`
    

### File Rewrite Profile
The file rewrite profile carries out a set of instructions and rewrites a file accordingly.
Two file rewrite profiles are supplied as default:


`-uc` Unicode replacer profile

Replaces specified illegal characters with their unicode escaped counterpart.
Note: Does require `native2ascii` to be installed on your system.
- arg: `-i` location of the illegal characters file
    - example: `-i /Users/my.user/Documents/illegal_characters.txt`

`-rr` Regex replacer profile
- arg: `-p` the regex pattern to match within the file text
    - example: `-p ^(\w)\.$`
- arg: `-c` the regex rewrite command
    - command that indicates how to modify the regex matches found
    - multiple commands can be supplied. They will be run in the order that they are given as input.
    - example: `-c 1(2,{0})`
        - "1" is the regex group to replace
        - "(2, {0})" are the replacement parameters. Solo integers are used to represent a group in the match, bracketed integers are used to represent a user supplied parameter. 
- arg: `-param` a parameter for the rewrite command
    - parameterised string that can be used in the regex rewrite command
    - example: `-param 'myword'`
        - string is delimited using apostrophes
        - apostrophes can be escaped with a backslash if they are wanted within the parameter
            - example: `-param 'John\'s apple'`

Example regex replacer profile argument inputs:

Replace all occurrences of "word" with "o"

`-p w(o)rd -c 0(1)`

or

`-p word -c 0({0}) -param 'o'`

### Example uses

In all .java files, replace multi-line block java comments that only require a single line, and place a period at the end of the line:

`-b`

`-d /Users/user/Documents/MyProject/ -e java` 

`-rr` 

`-p (\/\*\*)\s*\n\s*\*(.*)\n\s*(\*\/) -c 0(1,2,{0},3) -param '.'`

Replacing all occurrences of the letters "ä", "ö", and "ü" with their escaped counterparts ("\u00e4", "\u00f6", "\u00fc").
Assumes a target text file `myfile.txt` and illegal character file `chars.txt` with these letters present at location `/Users/user/Documents/` and running the program from that location:

`-s`

`-p myfile.txt`
 
 `-uc`
 
 `-i chars.txt`

## Creating your own profiles

To create and use your own profiles simply create a new Python class that extends the relevant abstract profile class in package `common.profile.abstract`.

If your profile requires a schema there is also a SchemaGenerator abstract class you may use as a guideline in package `common.schema_generator.abstract`, although this is not strictly necessary.

Once created, all you need to do is add the class type to the list (`run_profiles` or `file_rewrite_profiles`) found in TextReplacer.py. 
Now the program can be run any time with your custom profiles!

## Software requirements

Python 3.x

## Testing

Unit tests utilise `pytest`.
From the root program directory, use command `python3 -m pytest` to run all tests.
