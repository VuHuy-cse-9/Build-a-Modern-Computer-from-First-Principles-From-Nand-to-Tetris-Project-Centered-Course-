import numpy as np
import sys

class SymbolTable:
    """
    Manage symbols table
    """
    def __init__(self):
        self.table = {
            #C-comp-instruction
            "comp": {
                "0"  :"101010",
                "1"  :"111111",
                "-1" :"111010",
                "D"  :'001100',
                "A"  :'110000',
                "M"  :'110000',
                "!D" :"001101",
                "!A" :"110001",
                "!M" :"110001",
                "-D" :"001111",
                "-A" :"110011",
                "-M" :"110011",
                "D+1":"011111",
                "A+1":"110111",
                "M+1":"110111",
                "D-1":"001110",
                "A-1":"110010",
                "M-1":"110010",
                "D+A":"000010",
                "D+M":"000010",
                "D-A":"010011",
                "D-M":"010011",
                "A-D":"000111",
                "M-D":"000111",
                "D&A":"000000",
                "D&M":"000000",
                "D|A":"010101",
                "D|M":"010101"
            },
            "dest": {
                "null":"000",
                "M"   :"001",
                "D"   :"010",
                "MD"  :"011",
                "A"   :"100",
                "AM"  :"101",
                "AD"  :"110",
                "AMD" :"111" 
            },
            "jump": {
                "null":"000",
                "JGT" :"001",
                "JEQ" :"010",
                "JGE" :"011",
                "JLT" :"100",
                "JNE" :"101",
                "JLE" :"110",
                "JMP" :"111" 
            },
            "symbols": {
                #Virtuals symbols:
                "R0":0,
                "R1":1,
                "R2":2,
                "R3":3,
                "R4":4,
                "R5":5,
                "R6":6,
                "R7":7,
                "R8":8,
                "R9":9,
                "R10":10,
                "R11":11,
                "R12":12,
                "R13":13,
                "R14":14,
                "R15":15,
                #Predefined pointers:
                "SP":0,
                "LCL":1,
                "ARG":2,
                "THIS":3,
                "THAT":4,
                #IO Pointers
                "SCREEN":16384,
                "KBD":24576
            },
            "variables": {}
        }
        self.next_variable_address = 16
    
    def find(self, type="", key=""):
        assert key != "" and type !=""
        return self.table[type].get(key)

    def add(self, key="", value=-1, type=""):
        assert key != "" and  type!=""
        if type=="variables": 
            self.table[type].update({key: self.next_variable_address})
            self.next_variable_address += 1 #Edit here    
        else:
            self.table[type].update({key: value})

def fields_to_code(fields_list, table):
    """
    Translate each field into its corresponding binary values
    2 loops:
    - First loops: Add symbold to table
    - Second loops: Instruction -> code
    """
    #First loop:
    symbol_count = 0
    for index in np.arange(len(fields_list)):
        if (fields_list[index][0] == "("):
            #Add symbol to tables
            table.add(
                type="symbols",
                key=fields_list[index][1],
                value=index - symbol_count
            )
            #Remove symbols instruction virtually
            symbol_count += 1
    #Second loop:
    code_list = []
    for fields in fields_list:
        code = ""
        if fields[0] == "@":
            #Variable code /  Constant code
            code_list.append(A_translate(fields[1], table))
        elif fields[0] == "(":
            #Symbold code: Ignore
            continue
        else:
            #C instuction
            code_list.append(C_translate(fields, table))
    return code_list

def C_translate(fields, table):
    """
    Translate C instruction to code
    fields[0] = dest
    fields[1] = comp
    fields[2] = jump
    """
    code = "111" #default value
    #Get comp bits
    code += get_comp_a_bits(fields[1])
    code += table.find("comp", fields[1])#Translate comp -> code
    #Get dest bits:
    if (len(fields[0]) == 0):
        code += table.find("dest", "null")
    else:
        code += table.find("dest", fields[0])
    #Get jump bits:
    if (len(fields[2]) == 0):
        code += table.find("jump", "null")
    else:
        code += table.find("jump", fields[2]) 
    return code
    
def get_comp_a_bits(field):
    """
    Get a bit in C instruction code
    field == comp: String
    """
    #Get a bit:
    a_is_zero_fields = ["0", "1", "-1", "D", "A", "!D", "!A", "-D", "-A", "D+1", "A+1", "D-1", "A-1", "D+A", "D-A", "A-D", "D&A", "D|A"]
    for item in a_is_zero_fields:
        if item == field:
            return'0'
    return '1'

def A_translate(field, table):
    """
    Translate A instruciton to code
    field == xxx (in @xxx)
    @END
    @12
    """
    #Check whether symbol or constant
    isSymbol = False
    for char in field:
        if char < '0' or '9' < char:
            #Symbol variable:
            isSymbol = True
            break
    #Get address / value:
    address = 0
    if isSymbol:
        address = table.find("symbols",field)
        if address == None:
            address = table.find("variables", field)
            if address == None:
                table.add(
                    type="variables",
                    key=field,
                )
                address = table.find("variables", field)
    else:
        address = int(field) #                      Edit here
    
    #Get code:
    return int_to_binary(address)
    
def int_to_binary(number):
    """
    Convert int to binary 16 bit in string 
    """
    return f'{number:016b}'


def instruction_to_fields(instructions):
    """
    Unpacks each instruction into its underlying fields
    """
    fields_list = []
    for instruction in instructions:
        fields = []
        if instruction[0] == "@":
            #@xxx
            fields.append("@")  #Identify variable
            fields.append(instruction[1:])
        elif instruction[0] == '(':
            #Symbols instruction
            fields.append("(")  #Identify Symbols
            fields.append(instruction[1:len(instruction) - 1])
        else:
            #dest=comp;jump:
            #M=A
            #M=A+B
            #D;Jump
            #M=A+B;Jump
            list = instruction.split("=")
            #Add dest fields
            if len(list) > 1:
                #Contain dest fields
                fields.append(list[0])
            else:
                fields.append("")
            if len(list) == 1:
                list = list[0].split(";")
            else:
                list = list[1].split(";")
            #Add comp fields
            fields.append(list[0])
            #Add jump fields
            if len(list) > 1:
                #contain jump fields
                fields.append(list[1])
            else:
                fields.append("")
        fields_list.append(fields)
    return fields_list
    
    
def getCleanInstruction(file_name):
    """
    Read instructions, remove space, \n, comment:
    """
    raw_instructions =  []
    #Read all instructions
    with open(file_name) as file:
        raw_instructions = file.readlines()
    file.close()
    #Remove space, Remove comment, \n"
    clean_instructions = []
    for line in raw_instructions:
        #Remove space:
        line = ''.join(line.split())
        #Remove comment:
        index = line.find("//")
        if (index >= 0):
            #line has a comment
            line = line[0:index]
        if len(line) == 0:
            #line is comment or vertical space
            continue
        #Remove \n
        clean_instructions.append(line.removesuffix("\n"))        
    return clean_instructions


def main():
    """
    Start Assembler
    """
    file_name = sys.argv[1]
    #Get clean instructions
    instructions = getCleanInstruction(file_name)
    #Parse instructions to fields:
    fields_list = instruction_to_fields(instructions)
    table = SymbolTable()
    code_list = fields_to_code(fields_list, table)
    for index in np.arange(len(code_list)):
        if index != len(code_list) - 1:
            code_list[index] = code_list[index] + '\n'
    machine_code = ''.join(code_list)        
    
    outfile = sys.argv[2]
    with open(outfile, "w") as file:
        file.write(machine_code)
    file.close()
    
    
if __name__ == "__main__":
    main()
    