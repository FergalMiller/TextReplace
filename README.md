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
- `-s` Single file run profile
    - arg: `-p` the path of the file to be rewritten
    

- `-b` Bulk file run profile
    - arg: `-d` the directory to traverse to find files within
    - arg: `-e` a file extension filter
    - arg: `-r` a regex pattern  filter for file names 
    

### File Rewrite Profile
The file rewrite profile carries out a set of instructions and rewrites a file accordingly.
Two file rewrite profiles are supplied as default:


`-uc` Unicode replacer profile

Replaces specified illegal characters with their unicode escaped counterpart.
Note: Does require `native2ascii`.
- arg: `-i` location of the illegal characters file


`-rr` Regex replacer profile
- arg: `-p` the regex pattern to match within the file text
- arg: `-c` the regex rewrite command
- arg: `-param` a parameter for the rewrite command


