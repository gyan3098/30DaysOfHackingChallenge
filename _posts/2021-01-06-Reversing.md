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
value of argv = ['arg1', 'arg2', 'arg3']

When disassembling the binary with any of the reverse engineering tools(like, ghidra, radare2, cutter, gdb or any other). To get to a specific location of the array(here to know the value of second argument i.e. arg1, the compiler do the below works)

The below is an example of

<img src="{{'/public/understanding_argv.png' | absolute_url}}" alt="understanding_argv"/>

Let me explain it in easy way   
int main(int argc, char \*\*argv){/* ... */}  

When running the program  
-> ./easy abcd  

so, argv[0] = 'easy'  
and argv[1] = 'abcd'

To get value of `argv[1]` to the `eax` register, assembler do the following operations.   
```
  mov eax, dword[argv]
  add eax, 4
  mov eax, dword[eax]      
```
So, Let me explain this to you, first line moves the address of `argv` to `eax` i.e. address of `argv[0]` {since address of first index of array = starting address of array}.   
Second line increments the value of `eax` by 4, so now it points to the address of `argv[1]`.  
Now, address of `argv[1]` is stored in `eax`, third line moves the contents of value at the memory location of `eax` to `eax`. Here `dword[eax]` has the value of `argv[1]`. So now `eax` has the value 0x64636261.

[Reference link to understand above with an example](https://maxkersten.nl/binary-analysis-course/introduction/secura-grand-slam-ctf-easy-reverse/)
