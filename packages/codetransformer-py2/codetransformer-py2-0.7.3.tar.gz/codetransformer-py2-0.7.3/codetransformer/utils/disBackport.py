from dis import findlinestarts, findlabels

from opcode import *
from opcode import __all__ as _opcodes_all

import collections
import six

__all__ = ["get_instructions"] + _opcodes_all

_Instruction = collections.namedtuple("_Instruction",
     "opname opcode arg argval argrepr offset starts_line is_jump_target")

class Instruction(_Instruction):
    """Details for a bytecode operation
       Defined fields:
         opname - human readable name for operation
         opcode - numeric code for operation
         arg - numeric argument to operation (if any), otherwise None
         argval - resolved arg value (if known), otherwise same as arg
         argrepr - human readable description of operation argument
         offset - start index of operation within bytecode sequence
         starts_line - line started by this opcode (if any), otherwise None
         is_jump_target - True if other code jumps to here, otherwise False
    """

def _get_code_object(x):
    """Helper to handle methods, functions, generators, strings and raw code objects"""
    if hasattr(x, '__func__'): # Method
        x = x.__func__
    if hasattr(x, '__code__'): # Function
        x = x.__code__
    if hasattr(x, 'gi_code'):  # Generator
        x = x.gi_code
    # if isinstance(x, str):     # Source code
    #     x = _try_compile(x, "<disassembly>")
    if hasattr(x, 'co_code'):  # Code object
        return x
    raise TypeError("don't know how to disassemble %s objects" %
                    type(x).__name__)


def get_instructions(x, first_line=None, *_):
    """Iterator for the opcodes in methods, functions or code
    Generates a series of Instruction named tuples giving the details of
    each operations in the supplied code.
    If *first_line* is not None, it indicates the line number that should
    be reported for the first source line in the disassembled code.
    Otherwise, the source line information (if any) is taken directly from
    the disassembled code object.
    """
    co = _get_code_object(x)
    cell_names = co.co_cellvars + co.co_freevars
    linestarts = dict(findlinestarts(co))
    if first_line is not None:
        line_offset = first_line - co.co_firstlineno
    else:
        line_offset = 0
    return _get_instructions_bytes(co.co_code, co.co_varnames, co.co_names,
                                   co.co_consts, cell_names, linestarts,
                                   line_offset)

def _get_const_info(const_index, const_list):
    """Helper to get optional details about const references
       Returns the dereferenced constant and its repr if the constant
       list is defined.
       Otherwise returns the constant index and its repr().
    """
    argval = const_index
    if const_list is not None:
        argval = const_list[const_index]
    return argval, repr(argval)

def _get_name_info(name_index, name_list):
    """Helper to get optional details about named references
       Returns the dereferenced name as both value and repr if the name
       list is defined.
       Otherwise returns the name index and its repr().
    """
    argval = name_index
    if name_list is not None:
        argval = name_list[name_index]
        argrepr = argval
    else:
        argrepr = repr(argval)
    return argval, argrepr

def _unpack_opargs(code):
    # enumerate() is not an option, since we sometimes process
    # multiple elements on a single pass through the loop
    extended_arg = 0
    n = len(code)
    i = 0
    while i < n:
        op = ord(code[i])
        offset = i
        i = i+1
        arg = None
        if op >= HAVE_ARGUMENT:
            arg = ord(code[i]) + ord(code[i+1])*256 + extended_arg
            extended_arg = 0
            i = i+2
            if op == EXTENDED_ARG:
                extended_arg = arg*65536
        yield (offset, op, arg)

def _get_instructions_bytes(code, varnames=None, names=None, constants=None,
                      cells=None, linestarts=None, line_offset=0):
    """Iterate over the instructions in a bytecode string.
    Generates a sequence of Instruction namedtuples giving the details of each
    opcode.  Additional information about the code's runtime environment
    (e.g. variable names, constants) can be specified using optional
    arguments.
    """
    labels = findlabels(code)
    starts_line = None
    free = None
    for offset, op, arg in _unpack_opargs(code):
        if linestarts is not None:
            starts_line = linestarts.get(offset, None)
            if starts_line is not None:
                starts_line += line_offset
        is_jump_target = offset in labels
        argval = None
        argrepr = ''
        if arg is not None:
            #  Set argval to the dereferenced value of the argument when
            #  available, and argrepr to the string representation of argval.
            #    _disassemble_bytes needs the string repr of the
            #    raw name index for LOAD_GLOBAL, LOAD_CONST, etc.
            argval = arg
            if op in hasconst:
                argval, argrepr = _get_const_info(arg, constants)
            elif op in hasname:
                argval, argrepr = _get_name_info(arg, names)
            elif op in hasjrel:
                argval = offset + 3 + arg
                argrepr = "to " + repr(argval)
            elif op in haslocal:
                argval, argrepr = _get_name_info(arg, varnames)
            elif op in hascompare:
                argval = cmp_op[arg]
                argrepr = argval
            elif op in hasfree:
                argval, argrepr = _get_name_info(arg, cells)
        yield Instruction(opname[op], op,
                          arg, argval, argrepr,
                          offset, starts_line, is_jump_target)