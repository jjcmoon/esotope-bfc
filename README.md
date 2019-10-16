# ESOTOPE BRAINFUCK COMPILER

By Kang Seonghoon <esotope+bfc@mearie.org>


This is the Esotope Brainfuck Compiler: the world's most optimizing Brainfuck-
to-something compiler. Well, it is not a Something-to-Brainfuck compiler like
Jeffry Johnston's BFBASIC, but it translates the Brainfuck code into efficient
target language code (and possibly human-readable), so in this sense it is
actually a _decompiler_ rather than compiler.

There are many Brainfuck-to-C compilers (or Brainfuck-to-ELF compiler, and so
on) available, but there are almost no compiler which can translate the
following Brainfuck code:

    >+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[
    <++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.

...into something like the following code:

    /* generated by esotope-bfc */
    #include <stdio.h>
    #include <stdint.h>
    #define PUTS(s) fwrite(s, 1, sizeof(s)-1, stdout)
    static uint8_t m[30000], *p = m;
    int main(void) {
        PUTS("Hello World!");
        return 0;
    }

Surprisingly I had seen no compiler reached this one! So I started to make my
own compiler; Esotope Brainfuck Compiler is the result. (Actually, there are
now one or two other compilers reached this state, but they are inspired by
Esotope Brainfuck Compiler.)

## Usage

You will need to have python3 installed to run Esotope-bfc:

    > python3 ./esotope-bfc helloworld.bf > helloworld.c
    
After Esotope has compiled to C, you can invoke your favourite C compiler and run the program.
   
    > gcc -O3 helloworld.c -o helloworld
    > ./helloworld
    Hello World!

## Licence

Esotope Brainfuck Compiler is written by Kang Seonghoon. It can be freely
used and redistributable under the terms of MIT license.

