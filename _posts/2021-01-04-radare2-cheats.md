---
layout: post
title: Radare2-cheats
---

r2 has an embedded webserver and ships some	basic user interfaces written in html/js.
$ r2 -c=H <binary_file_name>

'seek' command is abbreviated as 's'  
ex:-  
	[0x000000]> s + 10   
	[0x000000]> s +0x25  
	[0x000000]> s + [0x100+ptr_table]

[0x000000]> s++		:- seek forward  
[0x000000]> s--		:- seek backward

'print' alias as 'p' <- it takes number of submodes - the 2nd letter secifying a desired mode.

ex:-
	[0x000000]> px :- to print in hexadecimal  
	[0x000000]> pd :- for disassembling

to be allowed to write files (-w) option to r2 when opening a file.('x' subcommand for hexpairs),('a' subcommand for even assembly opcodes)
ex :-
	[0x000000]> w hello world		:- string
	[0x000000]> wx 90 90 90 90	:- hexpairs
	[0x000000]> wa jmp 0x808140	:-	assemble  
	[0x000000]> wf inline.bin 		:- write contents of file  

append '?' to a command will show its help message  
ex:-  
	[0x000000]> a? 		:- will show all commands starting with a

[0x000000]> VV		:- To enter block Visual  mode  
[0x000000]> q 		:- To exit block Visual mode  
in visual mode we can use HJKL keys to navigate(left,down,up,right ,respectively)

cursor mode :- toggled by 'c' key
in toggle mode we can arrange the alignment of the code

$ 'TAB' 		:- to toggle between differnt parts of the code(blue border shows on which block you are)



To enter Visual  mode(hex representation) :- $ V
To exit block Visual mode :- $ q
in visual mode we can use HJKL keys to navigate(left,down,up,right ,respectively)
To overwrite the bytes:-
	$ i
'TAB':- To switch between the hex(middle) and string(right) columns

to scroll different visual mode representation:-
	$ p or P

***********************
MOST IMPORTANT VISUAL MODE  curses-like panels interfaces:-
	$ V!

	'F7' or 's' :- step into current instruction
	'F8' or 'S' :- step over current instruction
	'F2'		:- to set breakpoints

This mode contains many options on the top.You can use it like an application
and navigate to different part of code

***********************

cursor mode :- toggled by 'c' key
to select a byte range in cursor mode :- SHIFT + H
										 SHIFT + J
										 SHIFT + K
										 SHIFT + L

-------------------------------
Important command line options
-------------------------------
-A 				:- run 'aaa' command to analyze all referenced code
-B [addr] 		:- set base address for PIE binaries
-c 'cmd..' 		:- execute radare command
-C 				:- file is host:port(alias for -c=https://%s/cmd/)
-d 				:- debug the executable 'file' for running 'pid'
-D [backend]	:- enable debug mode
-H ([var])		:- display variable
-K [OS/kern]	:- set asm.os (linux,macos,w32,netbsd,...)
-m [addr]		:- map file at given address(loadaddr)
-M 				:- do not demangle symbol names
-p [prj]		:- use project ,list if no arg,load if no file
-P [file]		:- apply repatch file and quit
-s [addr]		:- initial seek
-w 				:- open file in write mode

--------------------------------
Common usage patterns
--------------------------------
Open a file in write mode without parsing the file format headers
$ r2 -nw file

Quickly get into an r2 shell without opening any file
$ r2 -

Set the configuration variable
$ r2 -e scr.color=0 blah.bin

Use an existing project file
$ r2 -p test

-----------------------------------
Command Format
-----------------------------------
general format
[.][times][cmd][~grep][@[@iter]addr!size][|>pipe]	;

to repeatedly execute a command,prefix the command with a number
px 		#run px
3px		#run px 3 times

To execute a command in shell context  :- prefix  '!'
To use the cmd callback from the I/O plugin :- prrfix with '=!'

ex:-
	$ ds 					:- call the debugger's 'step' command
	$ px 200 @ esp 			:- show 200 hex bytes at esp
	$ pc > file.c 			:- dump buffer as a C byte array to file.c
	$ wx 90 @@ sym.*		:- write a nop on every symbol
	$ pd 2000 | grep eax 	:-	grep opcodes that use the 'eax' register
	$ px 20 ; pd 3 ; px 40 	:- multiple commands in a single line

pipe ('|') is available in r2 shell
can be used to filter the output with commands like wc,grep,less

there is also built-in grep(~)

$ ~? 		:- for help
'~' character enables internal grep-like function used to filter output of any command

ex:-
	pd 20~call 		:- disassemble 20 instructions and grep output for 'call'
	pd 20~call:0	:- get first row
	pd 20~call:1	:- get second row
	pd 20~call[0]	:- get first column
	pd 20~call[1]	:- get second column
	pd 20~call:0[0]	:- grep the fist column of the first row matching 'call'

'@' character is used to specify a temporary offset at which command to its left will be executed

ex:-
	$ pd  @ 0x100000fce		:- to disasemble 5 instructions at address 0x10000fce

$ !~...	:-to see the history


--------------------------------
EXPRESSIONS
--------------------------------
to evaluate mathematical expressions pretend them with command '?'

[0xb7f9d810]>	?vi	0x8048000
134512640
[0xv7f9d810]>	?vi	0x8048000+34
134512674
[0xb7f9d810]>	?vi	0x8048000+0x34
134512692
[0xb7f9d810]>	?	1+2+3-4*3
hex					0xfffffffffffffffa
octal			01777777777777777777772
unit				17179869184.0G
segment	fffff000:0ffa
int64			-6
string		"\xfa\xff\xff\xff\xff\xff\xff\xff"
binary		0b1111111111111111111111111111111111111111111111111111111111111010 fvalue:	-6.0
float:		nanf
double:	nan
trits			0t11112220022122120101211020120210210211201

supporte arithmetic:-
'+','-','*','/','%'
'>'		:- shift right
'<'		:- shift left

To use of logical OR , quote the whole comman to avoid executing | pipe:
ex:-
	$ "? 1 | 2"


$ $$	:- here(the current virtual seek)
$ $1	:- opcode length
$ $s 	:- file size
$ $j 	:- jump address(e.g. jmp 0x10)
$ $f 	:- jump fail address (e.g. jz 0x10 => next instruction)
$ $m 	:- opcode memory reference(e.g. mov eax,[0x10] => 0x10)
$ $b 	:- block size

ex:-
	[0x4A13B8C0]>	pd	1	@	+$l
	0x4A13B8C2			call	0x4a13c000

-------------------------------------------------
	Basic Debugger Session
------------------------------------------------
To debug a program ,start with '-d' option
$ pidof <binaryname>		:- to know the process id of binary
32220
$r2 -d 32220 			:- to attach to that process

$ r2 -d <binaryname>	:- to attach r2 directly to the binary(in debug mode)

$ r2 -a arm -b 16 -d gdb://192.168.1.43:9090

To continue program until a specific address is reached
'dcu' (debug continue until) takes the address of the placee to stop at
$ dcu main

Common commands used with debugger:-
$ ds 3			:- step 3 times
$ db 0x8048920	:- setup a breakpoint
$ db -0x8048920 :- remove a breakpoint
$ dc 			:- continue process execution
$ dcs 			:- continue until syscall
$ dd 			:- manipulate file descriptors
$ dm 			:- show process maps
$ dmp A S rwx	:- change permissions of page at A and size S
$ dr eax=33		:- set register value, eax = 33

To enter visual debugger mode use 'Vpp':
[0xb7f0c8c0]>	Vpp

Pressing 'p' will allow you to cycle through the rest of visual mode views
'F7' or 's' :- step into current instruction
'F8' or 'S' :- step over current instruction
'c'			:- to toggle the cursor mode
'F2'		:- to set breakpoints

To see value of variable and its location
$ .afvd <variablename>	:- to see value of variable
$ afvd		 			:- to see value of all variables of that function


In visual mode we can enter regular radare commands by prepending them with
':' .
ex:-
	<Press ':'>
	x @ esi

To get help on visual mode


Most strings are zero terminated.When we recover the control over the process,we get the arguments passed to syscall,pointed by %ebx.

[0x000000]> dcs open 		:- to continue the execution of a program until it executes the 'open' syscall

[0x000000]> dr
eax		0xffffffda		esi		0xffffffff	eip		0x4a14fc24
ebx		0x4a151c91		edi		0x4a151be1	oeax	0x00000005
ecx		0x00000000		esp		0xbfbedb1c	eflags	0x200246		
edx		0x00000000		ebp		0xbfbedbb0	cPaZstIdor0	(PZI)

[0x000000]>	psz	@	0x4a151c91
/etc/ld.so.cache

-----------------------------
Print memory contents
-----------------------------
[0x000000]> pf 'format memory string' @ 'address'
ex:-
	[0x000000]> pf xxS @ rsp


-------------
Disassembly
-------------
[0x000000]> pd 1		:- 	To disassemble code, it accepts a numeric value to specify how many instructions should be disassembled

[0x000000]> pD 	0x16	:- same as 'pd' but it takes a given number of bytes

--------------------
Disassembly Syntax
--------------------
[0x000000]> e asm.arch=?? 			:- to list all the available architecture
[0x000000]> e asm.arch=dalvik		:- to set the architecture flavor for the disassembler

[0x000000]> e asm.syntax = intel 	:- to set the flavor of the assembly syntax used by a disassembler engine

-----
XREF
-----
When r2 has discovered a XREF during the analysis, it will show you the information in the Visual Disassembly using 'XREF' tag:

;DATA XREF from 0x00402e0e (unk)
str.David_Mackenzie:

To see where this string is called, press 'x',if you want to the location where data is used then pressng the corresponding number [0-9] on your keyboard
'X' corresponds to the reverse operation aka 'axf'

To enable this view use this config var 'e dbg.funcarg = true'

-------------------------
Visual Ascii Art Panels
-------------------------
$ | 	:- split the current panel vertically
$ - 	:- split the current panel horizontally
$ * 	:- show pseudo code/r2dec in the current panel
$ : 	:- run r2 commands in prompt
$ G 	:- show graph in the current panel
$ m 	:- select the menu pannel
$ sS 	:- step in /step over
$ t 	:- rotate related commands in a panel
$ w 	:- start window mode
$ X 	:- close current panel
$ z 	:- swap current panel with the first one



Search is initiated by '/' command
[0x000000]> /?		:- for help

r2 generates a "hit" flag for every entry found. We can then use the 'ps'
commands to see the strings stored at the offsets marked by the flags in this group,and they will have names of the form 'hit0_<index>'.

[0x000000]> ps @ hit0_0

[0x000000]> /w Hello 		:- to search for wide-char strings(use '/w' command)

[0x000000]> /i Stallman 	:- to perform a case-insensitive search for strings

[0x000000]> /x 7f454c46 	:- to search for hexadecimal values

[0x000000]> f 				:- To see the hits

[0x000000]> f- hit* 		:- to remove all hit flags
[0x000000]>  //				:- repeat last search

---------------------------
Configuring search options
---------------------------
[0x000000]> e search.from = 0		:- start address
[0x000000]> e search.to = 0			:- end address
[0x000000]> e search.flags = true 	:- if enabled, create flags on hits

-------------------------------
Search automation
------------------------------
'cmd.hit' configuration variable is used to define a r2 command to be executed when a matching entry is found by the search engine
to run several commands,separate them with ';'
[0x000000]> e cmd.hit = p8 8
[0x000000]> / lib

[0x000000]> /b gyan		:- to search the string backwards
'/b' is doing same as '/' but backward ,so everything that applies for '/' can be used with '/b'.
[0x000000]> /bx 90 		:- to seach hex 90 backward

[0x000000]> e asm.pseudo = true 	:- to enable pseudo syntax
[0x000000]> asm.pseudo 	:- experimental pseudocode view

To add the comment to a particular line/addres we can use 'Ca' command
[0x00000000]> CCa 0x0000002	this guy seems legit


 ---------------------------
 Recursive analysis
 ---------------------------
 [0x000000]> aab 	:- perform basic-block analysis
 [0x000000]> aac 	:- analyze function calls from one
 [0x000000]> aaf 	:- analyze all function calls
 [0x000000]> aar 	:- analyze data references
 [0x000000]> aad 	:- analyze pointers to pointers references

[0x000000]> axt [addr] 	:- find data/code references to this address
[0x000000]> axf [addr] 	:- find data/code references from this address

----------------------------------
Managing variables
--------------------------------
the main variables commands are located in 'afv' namespace:
[0x000000]> afvR [varname]	:- list addresses where vars are accessed (READ)
[0x000000]> afvW [varname] 	:- list addresses where vars are accessed (WRITE)
[0x000000]> afva 			:- analyze function arguments/locals
[0x000000]> afvd name 		:- output r2 command for displaying the value of args/locals in the debugger
[0x000000]> afvb[?] 		:- manipulate bp based arguments/locals
[0x000000]>afvs[?]			:- manipulate sp based arguments/locals


We can rename variable affecting all places it was referenced
[0x000000]> afvn [old_name] [new_name]	:- rename argument/local
[0x000000]> afv- 						:- to simply remove the variable or argument


'afvt' which allows you to change the type of variable
[0x000000]> afvt local_10h char*

-------------------------
Macros
-------------------------
r2 allows to write simple macros, using this contruction

[0x000000]> (qwe; pd 4; ao)		:- this will define a macro called qwe' which runs sequentially first 'pd 4' then 'ao'

[0x000000]> .(qwe)				:- calling the macro
[0x000000]> (-qwe)				:- deleting the macro
[0x000000]> (* 					:- listing all available macros


It's possible to create a macro that takes arguments
[0x000000]> (foo x y; pd $0; s +$1)

the arguments are named by index,starting from 0: $0,$1,..


------------------
R2pipe
------------------
$ pip install r2pipe

import r2pipe
r2 = r2pipe.open("/bin/ls")
r2.cmd('aa')
print(r2.cmd("afl"))
print(r2.cmdj("aflj"))	# evaluate JSONs and returns an object

---------------
To script radare2
------------------
r2 -i <scriptfile> ...	:- run a script after loading the file
r2 -I <scriptfile> ...	:- run a script before loading the file

[0x000000]> . scriptfile :- interpret the file

refer radare2 book PAGE 219,220,221

---------------------
Registers
---------------------
[0x000000]> dr 			:- display value of all registers
[0x000000]> dr rip 		:- get value of 'rip'
[0x000000]> dr rip = esp :- set 'rip' as esp
[0x000000]> dr* 		:- Appending '*' will show radare commands

An old copy of registers is stored all the time to keep track of the changes during execution of a program being analyzed.
[0x000000]> oregs 		:- to see old copy of registers

CTF solving using Radare2 link:-
https://r2wiki.readthedocs.io/en/latest/home/ctf-solving-using-radare2/


[0x000000]> dm.			:-(See the dot) To know the memory-map we are currently in

[0x000000]> dmm 		:- to list modules(libraries,binaries loaded in memory)

[0x000000]> dmi. 	 	:- to see the closest symbol to the current adress

------------------
HEAP
------------------
[0x000000]> dmh 		:- to display a map of the heap which is useful for thosse who are interesting in inspecting the heap and its content

[0x000000]> dmhg 		:- to see a graph layout of heap


--------------------------
Reverse Debugging
--------------------------
radare2 has reverse debugger,that can seek the program counter backward
Firstly you need to save program state at the point you want to start recording

[0x000000]> dts+ 	:- syntax for recording
[0x000000]> dts 	:- for recording and managing program states

After recording the states, we can seek pc back and forth to any points after saved address.
ex:-
	[0x000000]> 2dso
	[0x000000]> dr rip
	0x004028ae
	[0x000000]> dsb
	continue	until	0x004028a2
	hit	breakpoint	at:	4028a2
	[0x000000]> dr rip
	0x004028a2

'dcb' seeks program counter until hit the latest breakpoints.So once set a breakpoint, you can back to it any time


[0x000000]> dts 	:- to see current recorded program states
session:	0			at:0x004028a0			""
session:	1			at:0x004028c2			""

we can also add comment
'dtsC' to add comment to saved states
[0x000000]> dtsC 0 program start
[0x000000]> dtsC 1 decryption start
[0x000000]> dts
session:	0			at:0x004028a0			"program	start"
session:	1			at:0x004028c2			"decryption	start


Program records can exported to file and of course import it
[0x000000]> dtst records_for_test
Session	saved in records_for_test.session and dump in records_for_test.dump
[0x000000]> dtsf records_for_test
