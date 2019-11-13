"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        # 256 byte RAM
        self.ram = [0] * 256

        # Register (R0 - R8)
        self.register = [0] * 8

        # Program Counter
        self.pc = self.register[0]

        # Instruction Register
        self.ir = None

        # set up branchtable
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[MUL] = self.handle_mul

    
    def handle_hlt(self, a, b):
        sys.exit()

    def handle_ldi(self, a, b):
        self.register[a] = b
        self.pc += 3
    
    def handle_prn(self, a, b):
        print(self.register[a])
        self.pc += 2

    def handle_mul(self, a, b):
        self.alu("MUL", a, b)
        self.pc += 3

    def load(self, filename):
        """Load a program into memory."""

        if filename[-4:] != ".ls8":
            full_filename = f"examples/{filename}.ls8"
        else: full_filename = f"examples/{filename}"
        try:
            address = 0
            with open(full_filename) as f:
                for line in f:
                    # deal with comments
                    # split before and after any comment symbol '#'
                    comment_split = line.split("#")

                    # convert the pre-comment portion (to the left) from binary to a value
                    # extract the first part of the split to a number variable
                    # and trim whitespace
                    num = comment_split[0].strip()

                    # ignore blank lines / comment only lines
                    if len(num) == 0:
                        continue

                    # set the number to an integer of base 2
                    value = int(num, 2)
                    # print the value in binary and in decimal
                    # print(f"{value:08b}: {value:d}")
                    
                    # add the value in to the memory at the index of address
                    self.ram[address] = value

                    # increment the address
                    address += 1


        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

    def ram_read(self, location):
        """Read avalue stored at specified address."""
        return self.ram[location]

    def ram_write(self, location, value):
        """Writes value to RAM at the address specified."""
        self.ram[location] = value


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        #elif op == "SUB": etc
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
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        while True:
            self.ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.branchtable[self.ir](operand_a, operand_b)

