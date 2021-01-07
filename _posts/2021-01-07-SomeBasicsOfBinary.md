---
layout: post
title: Binary
---


### Patching binary
In this post we will discuss about how to patch a binary with the help of `radare2` and it's plugin `r2dec`.

The link of the binary to be patched is <a href="{{'/hacking/PatchMe0x01.zip' | absolute_url }}" >this </a>.

To patch the binary run the radare2 in write mode.
```bash
r2 -w ./PatchMe0x01.bin
```
Here some functions are not named properly, creating a little bit confusion.
To understand the detailed explanation of the patching of binary, here is the [link](https://maxkersten.nl/binary-analysis-course/assembly-basics/practical-case-patch-me-0x01/)
Here I am showing the before and after assembly code along with the decompiled code.
Run the following commands in `r2` and make sure `r2dec` is correctly installed to see the expected output.
```radare2
[0x08048310]> aaaa
[0x08048310]> afl
[0x08048310]> s main
[0x08048424]> pdda
```
So, the below image shows the assembly code along with the decompiled code which is a very helpful and interesting features of `r2dec` for the beginners.
<img src="{{'/public/Patchme1.png' | absolute_url}}" alt="Patchme Disassembled and Decompiled"/>
So, in above figure if we see that the value of argc is stored into register `ecx` which is then moved to `eax` and then `eax` is compared with 0. Since value of argc will always be greater than 1( to understand it see the [page]({% post_url 2021-01-06-Reversing %})), the condition at location `0x08048443` always evaluates to false. And also then 1 is assigned to variable `var_ch` and then compared with 2 which also evaluates to false, therefore the condition at `0x80485b` always evaluates to zero. Also there is no any buffer overflow or string or any type of vulnerability. Therefore we have to patch the binary.


So, starting at the address, we would invert the condition.`wa` (write assembly)
First seek to the address where we have to write by using s(seek) followed by address (0x0804843a)
```radare2
[0x08048424]> s 0x0804843a
```
Now writing the assembly code(inverting the 1st condition)
```radare2
[0x0804843a]> wa je 0x8048462
Written 2 byte(s) (je 0x8048462) = wx 7426
```
Seeking to second writing location
```radare2
[0x0804843a]> s 0x08048447
```
Now writing the assembly code again here to invert the 2nd condition
```radare2
[0x08048447]> wa je 0x804845b
Written 2 byte(s) (je 0x804845b) = wx 7412
```
To check the binary is patched or not, seek to the main function and run `pdda`.
```radare2
[0x08048447]> s main
[0x08048424]> pdda
```

<img src="{{'/public/Patchme2.png' | absolute_url}}" alt="Patchme, patched Disassembled and Decompiled"/>
So now run the patched binary and hurray, we patched it.
<img src="{{'/public/patchMeRun.png' | absolute_url}}" alt="Patchme, patched"/>
