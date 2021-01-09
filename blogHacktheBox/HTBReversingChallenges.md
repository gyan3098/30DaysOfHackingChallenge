---
layout: page
title: HTB Reversing Challenges
---

#### Challenge 1
The below is the challenge.
<img src="{{'/public/BabyHTB.png' | absolute_url}}" alt="Image of Baby on HTB" />

Decompiling the binary with [Cutter](https://github.com/rizinorg/cutter) tool.
```C
// WARNING: Could not reconcile some variable overlaps
// WARNING: [r2ghidra] Detected overlap for variable var_2ch

undefined8 main(void)
{
    int32_t iVar1;
    char *s;
    int64_t var_38h;
    int64_t var_30h;
    char *s1;
    char *var_8h;

    var_8h = "Dont run `strings` on this challenge, that is not the way!!!!";
    puts("Insert key: ");
    fgets(&s1, 0x14, _reloc.stdin);
    iVar1 = strcmp(&s1, "abcde122313\n");
    if (iVar1 == 0) {
        s = (char *)0x594234427b425448;
        var_38h = 0x3448545f5633525f;
        var_30h._0_4_ = 0x455f5354;
        var_30h._4_2_ = 0x7d5a;
        puts(&s);
    } else {
        puts("Try again later.");
    }
    return 0;
}
```
Here we can easily see that the input is taken and compared with `abcde122313`. So, this is the required input.
