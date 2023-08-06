def NARGS(o):
    return (((o) % 256) + 2*((o) / 256))

def opcodeStackEffect(opCode, oparg=None):
    if opCode == 'POP_TOP':
        return -1
    if opCode == 'ROT_TWO' or \
                    opCode == 'ROT_THREE':
        return 0
    if opCode == 'DUP_TOP':
        return 1
    if opCode == 'ROT_FOUR':
        return 0

    if opCode == 'UNARY_POSITIVE' or \
                    opCode == 'UNARY_NEGATIVE' or \
                    opCode == 'UNARY_NOT' or \
                    opCode == 'UNARY_CONVERT' or \
                    opCode == 'UNARY_INVERT':
        return 0

    if opCode == 'SET_ADD' or \
                    opCode == 'LIST_APPEND':
        return -1

    if opCode == 'MAP_ADD':
        return -2

    if opCode == 'BINARY_POWER' or \
                    opCode == 'BINARY_MULTIPLY' or \
                    opCode == 'BINARY_DIVIDE' or \
                    opCode == 'BINARY_MODULO' or \
                    opCode == 'BINARY_ADD' or \
                    opCode == 'BINARY_SUBTRACT' or \
                    opCode == 'BINARY_SUBSCR' or \
                    opCode == 'BINARY_FLOOR_DIVIDE' or \
                    opCode == 'BINARY_TRUE_DIVIDE':
        return -1
    if opCode == 'INPLACE_FLOOR_DIVIDE' or \
                    opCode == 'INPLACE_TRUE_DIVIDE':
        return -1

    if opCode == 'SLICE+0':
        return 0
    if opCode == 'SLICE+1':
        return -1
    if opCode == 'SLICE+2':
        return -1
    if opCode == 'SLICE+3':
        return -2

    if opCode == 'STORE_SLICE+0':
        return -2
    if opCode == 'STORE_SLICE+1':
        return -3
    if opCode == 'STORE_SLICE+2':
        return -3
    if opCode == 'STORE_SLICE+3':
        return -4

    if opCode == 'DELETE_SLICE+0':
        return -1
    if opCode == 'DELETE_SLICE+1':
        return -2
    if opCode == 'DELETE_SLICE+2':
        return -2
    if opCode == 'DELETE_SLICE+3':
        return -3

    if opCode == 'INPLACE_ADD' or \
                    opCode == 'INPLACE_SUBTRACT' or \
                    opCode == 'INPLACE_MULTIPLY' or \
                    opCode == 'INPLACE_DIVIDE' or \
                    opCode == 'INPLACE_MODULO':
        return -1
    if opCode == 'STORE_SUBSCR':
        return -3
    if opCode == 'STORE_MAP':
        return -2
    if opCode == 'DELETE_SUBSCR':
        return -2

    if opCode == 'BINARY_LSHIFT' or \
                    opCode == 'BINARY_RSHIFT' or \
                    opCode == 'BINARY_AND' or \
                    opCode == 'BINARY_XOR' or \
                    opCode == 'BINARY_OR':
        return -1
    if opCode == 'INPLACE_POWER':
        return -1
    if opCode == 'GET_ITER':
        return 0

    if opCode == 'PRINT_EXPR':
        return -1
    if opCode == 'PRINT_ITEM':
        return -1
    if opCode == 'PRINT_NEWLINE':
        return 0
    if opCode == 'PRINT_ITEM_TO':
        return -2
    if opCode == 'PRINT_NEWLINE_TO':
        return -1
    if opCode == 'INPLACE_LSHIFT' or \
                    opCode == 'INPLACE_RSHIFT' or \
                    opCode == 'INPLACE_AND' or \
                    opCode == 'INPLACE_XOR' or \
                    opCode == 'INPLACE_OR':
        return -1
    if opCode == 'BREAK_LOOP':
        return 0
    if opCode == 'SETUP_WITH':
        return 4
    if opCode == 'WITH_CLEANUP':
        return -1
    if opCode == 'LOAD_LOCALS':
        return 1
    if opCode == 'RETURN_VALUE':
        return -1
    if opCode == 'IMPORT_STAR':
        return -1
    if opCode == 'EXEC_STMT':
        return -3
    if opCode == 'YIELD_VALUE':
        return 0

    if opCode == 'POP_BLOCK':
        return 0
    if opCode == 'END_FINALLY':
        return -3
    if opCode == 'BUILD_CLASS':
        return -2

    if opCode == 'STORE_NAME':
        return -1
    if opCode == 'DELETE_NAME':
        return 0
    if opCode == 'UNPACK_SEQUENCE':
        return oparg - 1
    if opCode == 'FOR_ITER':
        return 1
    if opCode == 'STORE_ATTR':
        return -2
    if opCode == 'DELETE_ATTR':
        return -1
    if opCode == 'STORE_GLOBAL':
        return -1
    if opCode == 'DELETE_GLOBAL':
        return 0
    if opCode == 'DUP_TOPX':
        return oparg
    if opCode == 'LOAD_CONST':
        return 1
    if opCode == 'LOAD_NAME':
        return 1
    if opCode == 'BUILD_TUPLE' or \
                    opCode == 'BUILD_LIST' or \
                    opCode == 'BUILD_SET':
        return 1 - oparg
    if opCode == 'BUILD_MAP':
        return 1
    if opCode == 'LOAD_ATTR':
        return 0
    if opCode == 'COMPARE_OP':
        return -1
    if opCode == 'IMPORT_NAME':
        return -1
    if opCode == 'IMPORT_FROM':
        return 1

    if opCode == 'JUMP_FORWARD' or \
                    opCode == 'JUMP_IF_TRUE_OR_POP' or  \
     opCode == 'JUMP_IF_FALSE_OR_POP' or \
     opCode == 'JUMP_ABSOLUTE':
        return 0

    if opCode == 'POP_JUMP_IF_FALSE' or \
                    opCode == 'POP_JUMP_IF_TRUE':
        return -1

    if opCode == 'LOAD_GLOBAL':
        return 1

    if opCode == 'CONTINUE_LOOP':
        return 0
    if opCode == 'SETUP_LOOP' or \
                    opCode == 'SETUP_EXCEPT' or \
                    opCode == 'SETUP_FINALLY':
        return 0

    if opCode == 'LOAD_FAST':
        return 1
    if opCode == 'STORE_FAST':
        return -1
    if opCode == 'DELETE_FAST':
        return 0

    if opCode == 'RAISE_VARARGS':
        return -oparg

    if opCode == 'CALL_FUNCTION':
        return -NARGS(oparg)
    if opCode == 'CALL_FUNCTION_VAR' or \
                    opCode == 'CALL_FUNCTION_KW':
        return -NARGS(oparg) - 1
    if opCode == 'CALL_FUNCTION_VAR_KW':
        return -NARGS(oparg) - 2
    # undef NARGS
    if opCode == 'MAKE_FUNCTION':
        return -oparg
    if opCode == 'BUILD_SLICE':
        if (oparg == 3):
            return -2
        else:
            return -1

    if opCode == 'MAKE_CLOSURE':
        return -oparg - 1
    if opCode == 'LOAD_CLOSURE':
        return 1
    if opCode == 'LOAD_DEREF':
        return 1
    if opCode == 'STORE_DEREF':
        return -1
