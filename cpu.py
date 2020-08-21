"""CPU functionality."""
# SPRINT CHALLENGE NOTES:
# [ ] Add the `CMP` instruction and `equal` flag to your LS-8.
# [ ] Add the `JMP` instruction.
# [ ] Add the `JEQ` and `JNE` instructions.

import sys

cmp = 0b10100111
jmp = 0b01010100
jeq = 0b01010101
jne = 0b01010110
hlt = 0b00000001
ldi = 0b10000010
prn = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # the amount of working memory in the hardware
        self.reg = [0] * 8
        self.pc = 0  # program counter - which instruction, or which line is curently being read
        self.fl = 0  # flag - integer, always eight bits
        self.running = True
        # bitwise - binary conversion equivalent

    def load(self, program):
        """Load a program into memory."""

        address = 0

        with open(program) as file:
            for instruction in file:
                if instruction[0] == '0' or instruction[0] == '1':
                    self.ram[address] = int(instruction[0:7], 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        # # # SPRINT CHALLENGE MVP # # # 
        elif op == 'CMP':
            value_a = self.reg[reg_a]
            value_b = self.reg[reg_b]
            if value_a == value_b:
                self.reg[self.fl] = 1
            elif value_a > value_b:
                self.reg[self.fl] = 2
            else:
                self.reg[self.fl] = 4

        elif op == 'JMP':
            self.pc = self.reg[reg_a]
            return True
        # # # SPRINT CHALLENGE MVP # # # 

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self, address, value):
        """Run the CPU."""
        while self.running == True:

            instruction = self.ram[self.pc]

            if instruction == hlt:
                self.running = False

            elif instruction == ldi:
                # `LDI register immediate`
                # Set the value of a register to an integer.
                # Machine code:
                # 10000010 00000rrr iiiiiiii
                # 82 0r ii
                self.ram[address] = value

            elif instruction == prn:
                # `PRN register` pseudo-instruction
                # Print numeric value stored in the given register.
                # Print to the console the decimal integer value that is stored in the given register.
                # Machine code:
                # 01000111 00000rrr
                # 47 0r````
                print(float(self.ram[address]))
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value