---
layout: post
title: Basics of Reversing
---

### Understanding the assembly of inline arguments
```C
  int main(int argc, char **argv){ /* .....*/ }
  OR
  int main(int argc, char *argv[]) { /* ... */ }
```
So `argc` means (ARGument Count) is int and stores number of command-line arguments passed by the user including the name of the program.
And `argv` means (ARGument Vector) is array of character pointers listing all the arguments.

Ex:- ./binary arg1 arg2 arg3  
value of argc = 4 (3 values + 1 binary-name)  
value of argv = ['arg1','arg2','arg3']

When disassembling the binary with any of the reverse engineering tools(like, ghidra, radare2, cutter, gdb or any other). To get to a specific location of the array(here to know the value of second argument i.e. arg1, the compiler do the below works)

The below is an example of
![Understanding_argv](/public/understanding_argv.png)
```assembly
  ; start location of array is equal to the address of argv
  mov eax, dword[argv]  ;here address of *argv is being moved to eax.
  add eax, 4            ;to get to the second index of the array
```

https://maxkersten.nl/binary-analysis-course/introduction/secura-grand-slam-ctf-easy-reverse/
