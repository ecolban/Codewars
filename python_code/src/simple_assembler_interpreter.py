def simple_assembler(program):
    registers = {}

    def constant(x):
        return registers[x] if x in registers else int(x)

    pc = 0
    while pc < len(program):
        instruction = program[pc].split()[:3]
        cmd, *args = instruction
        if cmd == 'mov':
            reg, n = args
            registers[reg] = constant(n)
            pc += 1
        elif cmd in ('inc', 'dec'):
            reg, = args
            registers[reg] += (1 if cmd == 'inc' else -1)
            pc += 1
        elif cmd == 'jnz':
            reg, n = args
            pc = pc + (constant(n) if constant(reg) != 0 else 1)
    return registers
