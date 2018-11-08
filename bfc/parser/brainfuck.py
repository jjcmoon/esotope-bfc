# This is a part of Esotope Brainfuck Compiler.

from bfc.nodes import *
from bfc.expr import *
from bfc.cond import *

from bfc.parser.base import BaseParser

def reader(fp):
    for line in fp:
        for ch in line:
            yield ch


class Parser:
    """The basic Brainfuck parser.

    It handles eight basic Brainfuck commands, and calls the handler for unknown
    character. Basically unknown handler does nothing, but one can handle other
    commands (like #) via subclassing.

    The only operation besides simple parsing is the merging of repeated operations. 
    (This is only basic optimization, and doesn't account for +- or >< sequences. 
    flatten pass isused for that.)
    
    The rationale behind this, is to preserve the original code
    as much as possible, while limiting the memory usage. 
    You can recover the original code without comments quickly: 
    e.g. MovePointer[+3] represents >>> and MovePointer[-2]
    represents <<. Even >>><< is represented with two nodes.

    """

    def __init__(self, compiler):
        self.compiler = compiler


    def parse(self, fp):

        def update_rep():
            if repcount > 0:
                if last_char == '+':
                    nodestack[-1].append(AdjustMemory(0, +repcount))
                elif last_char == '-':
                    nodestack[-1].append(AdjustMemory(0, -repcount))
                elif last_char == '>':
                    nodestack[-1].append(MovePointer(+repcount))
                elif last_char == '<':
                    nodestack[-1].append(MovePointer(-repcount))



        nodestack = [Program()]
        offsetstack = [0]

        last_char = ''
        repcount = 0
        
        for cur_char in reader(fp):
            if cur_char == last_char:
                repcount += 1
            else:
                update_rep()

                last_char = ''
                if cur_char in '+-><':
                    last_char = cur_char
                    repcount = 1
                elif cur_char == '.':
                    nodestack[-1].append(Output(Expr[0]))
                elif cur_char == ',':
                    nodestack[-1].append(Input(0))
                elif cur_char == '[':
                    nodestack.append(While(MemNotEqual(0, 0)))
                elif cur_char == ']':
                    if len(nodestack) < 2:
                        raise ValueError('Brackets are not balanced')
                    loop = nodestack.pop()
                    nodestack[-1].append(loop)
                else:
                    self.unknown(cur_char, nodestack)

        update_rep()

        if len(nodestack) != 1:
            raise ValueError('Premature end of the loop')
        
        return nodestack[0]

    def unknown(self, cur_char, nodestack):
        pass

