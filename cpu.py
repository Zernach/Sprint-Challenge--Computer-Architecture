"""CPU functionality."""
# SPRINT CHALLENGE NOTES:
# [x] Add the `CMP` instruction and `equal` flag to your LS-8.
# [x] Add the `JMP` instruction.
# [x] Add the `JEQ` and `JNE` instructions.

import sys

CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # the amount of working memory in the hardware
        self.reg = [0] * 8
        self.pc = 0  # program counter - which instruction, or which line is curently being read
        self.fl = 0b00000000  # flag - integer, always eight bits
        self.running = True
        # bitwise - binary conversion equivalent

    def load(self, program=''):
        """Load a program into memory."""

        self.ram = [0b10000010,
        0b00000000,
        0b00001010,
        0b10000010,
        0b00000001,
        0b00010100,
        0b10000010,
        0b00000010,
        0b00010011,
        0b10100111,
        0b00000000,
        0b00000001,
        0b01010101,
        0b00000010,
        0b10000010,
        0b00000011,
        0b00000001,
        0b01000111,
        0b00000011,
        # # TEST1 (address 19):
        0b10000010, # LDI R2,TEST2
        0b00000010,
        0b00100000,
        0b10100111, # CMP R0,R1
        0b00000000,
        0b00000001,
        0b01010110, # JNE R2
        0b00000010,
        0b10000010, # LDI R3,2
        0b00000011,
        0b00000010,
        0b01000111, # PRN R3
        0b00000011,
        # TEST2 (address 32):
        0b10000010, # LDI R1,10
        0b00000001,
        0b00001010,
        0b10000010, # LDI R2,TEST3
        0b00000010,
        0b00110000,
        0b10100111, # CMP R0,R1
        0b00000000,
        0b00000001,
        0b01010101, # JEQ R2
        0b00000010,
        0b10000010, # LDI R3,3
        0b00000011,
        0b00000011,
        0b01000111, # PRN R3
        0b00000011,
        # TEST3 (address 48):
        0b10000010, # LDI R2,TEST4
        0b00000010,
        0b00111101,
        0b10100111, # CMP R0,R1
        0b00000000,
        0b00000001,
        0b01010110, # JNE R2
        0b00000010,
        0b10000010, # LDI R3,4
        0b00000011,
        0b00000100,
        0b01000111, # PRN R3
        0b00000011,
        # TEST4 (address 61):
        0b10000010, # LDI R3,5
        0b00000011,
        0b00000101,
        0b01000111, # PRN R3
        0b00000011,
        0b10000010, # LDI R2,TEST5
        0b00000010,
        0b01001001,
        0b01010100, # JMP R2
        0b00000010,
        0b01000111, # PRN R3
        0b00000011,
        # TEST5 (address 73):
        0b00000001] # HLT

        # Not being used to read file at the moment:

        #address = 0
        #with open(program) as file:
        #    for line in file:
        #        split_line = line.split('#')[0]
        #        command = split_line.strip()
        #        if command == '':
        #            continue
        #        instruction = int(command, 2)
        #        self.ram[address] = instruction
        #        address += 1

    def alu(self, op, reg_a = 0, reg_b = 0):
        """ALU operations."""

        def iterate():
            self.pc += 1

        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]

        if op == 'CMP':
            value_a = self.reg[reg_a]
            value_b = self.reg[reg_b]
            if value_a == value_b:
                self.reg[self.fl] = 0b00000001 # 1
            elif value_a > value_b:
                self.reg[self.fl] = 0b00000010 # 2
            else:
                self.reg[self.fl] = 0b00000100 # 4
            iterate()

        if op == 'JMP':
            self.pc = self.reg[reg_a]
            iterate()
            return True

        if op == 'JNE':
            value = self.reg[self.fl]
            if value == 0b00000010 or value == 0b00000100:
                iterate()
                return self.alu('JMP', reg_a)

        if op == 'JEQ':
            if self.reg[self.fl] == 0b00000001:
                iterate()
                return self.alu('JMP', reg_a)

        else:
            raise Exception("Unsupported ALU operation")

# Currently Un-Used Function:

#    def trace(self):
#        """
#        Handy function to print out the CPU state. You might want to call this
#        from run() if you need help debugging.
#        """
#
#        print(f"TRACE: %02X | %02X %02X %02X |" % (
#            self.pc,
#            #self.fl,
#            #self.ie,
#            self.ram_read(self.pc),
#            self.ram_read(self.pc + 1),
#            self.ram_read(self.pc + 2)
#        ), end='')
#
#        for i in range(8):
#            print(" %02X" % self.reg[i], end='')
#        print()

    def run(self):
        """Run the CPU."""
        while self.running == True:

            instruction = self.ram[self.pc]
            print(instruction)
            print(self.pc)

            if instruction == CMP:
                self.alu("CMP", reg_a=self.ram[self.pc+1], reg_b=self.ram[self.pc+2])
                #self.pc += 3

            if instruction == JMP:
                self.alu("JMP", reg_a=self.ram[self.pc+1])
                #self.pc += 2

            if instruction == JEQ:
                self.alu("JEQ", reg_a=self.ram[self.pc+1])
                #self.pc += 2

            if instruction == JNE:
                self.alu("JNE", reg_a=self.ram[self.pc+1])
                #self.pc += 2

            if instruction == HLT:
                self.running = False

            if instruction == LDI:
                # `LDI register immediate`
                # Set the value of a register to an integer.
                # Machine code:
                # 10000010 00000rrr iiiiiiii
                # 82 0r ii
                self.reg[self.ram[self.pc+1]] = self.ram[self.pc + 2]
                #self.pc += 3

            if instruction == PRN:
                # `PRN register` pseudo-instruction
                # Print numeric value stored in the given register.
                # Print to the console the decimal integer value that is stored in the given register.
                # Machine code:
                # 01000111 00000rrr
                # 47 0r````
                print(self.reg[self.ram[self.pc+1]])
                #self.pc += 2
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value