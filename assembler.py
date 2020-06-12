import re  #importing the regular expres library to basically use to replicate a lexor 

destination = {'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101',
               'AD': '110', 'AMD': '111'}    #dest dictionary

computation = {'0': '101010', '1': '111111', '-1': '111010', 'D': '001100',
               'A': '110000', '!D': '001101', '!A': '110001', '-D': '001111',
               '-A': '110011', 'D+1': '011111', 'A+1': '110111',
               'D-1': '001110', 'A-1': '110010', 'D+A': '000010',
               'D-A': '010011', 'A-D': '000111', 'D&A': '000000',
               'D|A': '010101', 'M': '110000', '!M': '110001', '-M': '110011',
               'M+1': '110111', 'M-1': '110010', 'D+M': '000010','M+D':'000010',
               'D-M': '010011', 'M-D': '000111', 'D&M': '000000',
               'D|M': '010101'}    #c dictionary

jumps = {'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101',
         'JLE': '110', 'JMP': '111'}    #jmp dictionary

set_a_bit = set(["M", "!M", "-M", "M+1", "M-1", "D+M", "D-M", "M-D", "D&M", "D|M","M+D"])    # for the 4th part of the binary symbol

builtin_symbols = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5,
                   'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
                   'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SP': 0,
                   'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'SCREEN': 16384,
                   'KBD': 24576}    #these are adresses set for the pre defined symbols 

symbol_table = {}
user_def_vars = {}    

next_program_address = 0
next_memory_address = 16    


def stage1_symbol_table_generator(line):
    """
    Process a single line of Hack assembly. If the line contains a symbol
    check if it is in the global symbol_table. If not add it and return.
    If line is not a symbol incriment next_program_address and return.
    """
    global symbol_table
    global next_program_address
  
            
    
    token = re.split('(\(|\)|=|;|@)', line)
    if token[1] == '(':
        if token[2].isdigit():
            return
        if token[2] not in symbol_table:
            symbol_table[token[2]] = next_program_address
        return
    next_program_address += 1    


def stage2_code_generator(line):
    """
    Process a single line of Hack assembly. If the line contains a symbol
    look it up in the global symbol_table. Generate Hack machine code from
    Hack assembly code.
    """
    global next_memory_address
    global user_def_vars
   
         
    token = re.split('(\(|\)|=|;|@)',line)
    if token[1] == '(':
        return
    if token[1] == '=':
        if token[2] in set_a_bit:
            a = '1'
        else:
            a= '0'
        print('111' + a + computation[token[2]] + destination[token[0]] + '000')
        return
    if token[1] == ';':
        print('111' + '0' + computation[token[0]] + '000' + jumps[token[2]])
        return
    if token[1] == '@':
        if token[2].isdigit():
            print('0' + format(int(token[2]), '015b'))
            return
        if token[2] in symbol_table:
            print('0' + format(symbol_table[token[2]], '015b'))
            return
        if token[2] in builtin_symbols:
            print('0' + format(builtin_symbols[token[2]], '015b'))
            return
        if token[2] in user_def_vars:
            print('0' + format(user_def_vars[token[2]], '015b'))
            return
        user_def_vars[token[2]] = next_memory_address
        print('0' + format(next_memory_address, '015b'))
        next_memory_address += 1
        return
    else:
        return    


if __name__ == "__main__":
    for line in open("C:\\Users\\srina\\Desktop\\mult.asm", 'r'):
       
        a=line.replace(" ","")
           
        if a.strip():
            if not a.startswith("//"):
                stage1_symbol_table_generator(a.strip())
    for line in open("C:\\Users\\srina\\Desktop\\mult.asm", 'r'):
        if a.strip():
            if not a.startswith("//"):
                stage2_code_generator(a.strip())
               