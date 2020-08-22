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

                # Not being used to read file at the moment:

        address = 0
        with open(program) as file:
            for line in file:
                split_line = line.split('#')[0]
                command = split_line.strip()
                if command == '':
                    continue
                instruction = int(command, 2)
                self.ram[address] = instruction
                address += 1

        """
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
        """


    def cmp(self, op, reg_a=0, reg_b=0):
        #if op == "CMP":
            #self.FL &= 0b00000000
            if self.reg[reg_a] == self.reg[reg_a]:
                self.FL = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            self.pc += 3

    def hlt(self):
        self.running = False

    def jmp(self, reg_index):
        self.pc = self.reg[reg_index]

    def jeq(self, reg_index):
        if self.FL & 1 is 1:
            self.pc = self.reg[reg_index]
        else:
            self.pc += 2

    def jne(self, reg_index):
        if self.FL & 1 is 0:
            self.pc = self.reg[reg_index]
        else:
            self.pc += 2

    def ldi(self, reg_index, value):
        self.reg[reg_index] = value
        self.pc += 3

    def prn(self, reg_index):
        print(self.reg[reg_index])
        self.pc += 2

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
            #print(instruction)
            #print(self.pc)

            if instruction == CMP:
                #Compare the values in two registers.
                #* If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
                #* If registerA is less than registerB, set the Less-than `L` flag to 1, otherwise set it to 0.
                #* If registerA is greater than registerB, set the Greater-than `G` flag to 1, otherwise set it to 0.
                #Machine code:
                #10100111 00000aaa 00000bbb
                #A7 0a 0b
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.cmp("CMP", reg_a, reg_b)

            elif instruction == JMP:
                #Jump to the address stored in the given register.
                #Set the `PC` to the address stored in the given register.
                #Machine code:
                #01010100 00000rrr
                #54 0r
                reg_num = self.ram[self.pc + 1]
                self.jmp(reg_num)

            elif instruction == JEQ:
                #If `equal` flag is set (true), jump to the address stored in the given register.
                #Machine code:
                #01010101 00000rrr
                #55 0r
                reg_num = self.ram[self.pc + 1]
                self.jeq(reg_num)

            elif instruction == JNE:
                #If `E` flag is clear (false, 0), jump to the address stored in the given register.
                #Machine code:
                #01010110 00000rrr
                #56 0r
                reg_num = self.ram[self.pc + 1]
                self.jne(reg_num)

            elif instruction == HLT:
                #Halt the CPU (and exit the emulator).
                #Machine code:
                #00000001 
                #01
                self.hlt()

            elif instruction == LDI:
                # `LDI register immediate`
                # Set the value of a register to an integer.
                # Machine code:
                # 10000010 00000rrr iiiiiiii
                # 82 0r ii
                reg_index = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.ldi(reg_index, value)

            elif instruction == PRN:
                # `PRN register` pseudo-instruction
                # Print numeric value stored in the given register.
                # Print to the console the decimal integer value that is stored in the given register.
                # Machine code:
                # 01000111 00000rrr
                # 47 0r````
                reg_index = self.ram[self.pc + 1]
                self.prn(reg_index)

            else:
                self.pc += 1
    
    #def ram_read(self, address):
    #    return self.ram[address]

    #def ram_write(self, address, value):
    #    self.ram[address] = value