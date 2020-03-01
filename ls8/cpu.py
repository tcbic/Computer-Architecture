"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add list of properties to hold 256 bytes of memory.
        self.ram = [0] * 256
        # Add 8 general purpose registers.
        self.reg = [0] * 8
        # PC (Program Counter)
        self.pc = 0
        # Define stack pointer.
        self.sp = 7

        self.flag = [0] * 8

        pass

    def load(self):
        """Load a program into memory."""

        address = 0

        program = []
        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                if (len(line) > 0):
                    if "#" not in line:
                        binary_string = line.strip()
                    else:
                        binary_string = line.split(" #")[0].strip()
                    if binary_string.isnumeric():
                        integer_value = int(binary_string, 2)
                        program.append(integer_value)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # Flags

        # L
        self.flag[5]

        # G
        self.flag[6]

        # E
        self.flag[7]

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            # Compare values in the two registers.

            # If register a is less than register b...
            if self.reg[reg_a] < self.reg[reg_b]:
                # L
                self.flag[5] = 1
                # G
                self.flag[6] = 0
                # E
                self.flag[7] = 0

            # If register a is equal to register b...
            elif self.reg[reg_a] == self.reg[reg_b]:
                # L
                self.flag[5] = 0
                # G
                self.flag[6] = 0
                # E
                self.flag[7] = 1
            
            # If register a is greater than register b... 
            elif self.reg[reg_a] > self.reg[reg_b]:
                # L
                self.flag[5] = 0
                # G
                self.flag[6] = 1
                # E
                self.flag[7] = 0

            else:
                pass

        else:
            raise Exception("Unsupported ALU operation.")

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

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110        

        go = True

        # stack_pointer = self.sp

        while go:

            ir = self.ram_read(self.pc)

            stack_pointer = self.sp

            # First argument.
            operand_a = self.ram_read(self.pc + 1)
            # Second argument.
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif ir == PRN:
                reg = self.ram_read(self.pc + 1)
                self.reg[reg]
                print(f"{self.reg[reg]}")
                self.pc += 2

            elif ir == HLT:
                # print("Operations have been halted.")
                go = False
                self.pc += 1

            elif ir == PUSH:
                reg = operand_a
                value = self.reg[reg]
                self.reg[stack_pointer] -= 1
                self.ram_write(self.reg[stack_pointer], value)
                self.pc += 2

            elif ir == POP:
                reg = operand_a
                value = self.ram[self.reg[stack_pointer]]
                self.reg[reg] = value
                self.reg[stack_pointer] += 1
                self.pc += 2

            # Add CMP, JMP, JEQ and JNE.

            elif ir == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            elif ir == JMP:
                # print(f"JMP register address: {operand_a}")
                self.pc = self.reg[operand_a]
                # print(f"JMP program counter address: {self.pc}")

            elif ir == JEQ:
                if self.flag[7] == 1:
                    self.pc = self.reg[operand_a]
                else:
                    # print("else statement")
                    self.pc += 2

            elif ir == JNE:
                if self.flag[7] != 1:
                    self.pc = self.reg[operand_a]
                    # print(f"JNE program counter address: {self.pc}")
                else:
                    self.pc += 2

            else:
                print(f"Error, unknown command {ir}.")
                # Exit the program.
                sys.exit(1)