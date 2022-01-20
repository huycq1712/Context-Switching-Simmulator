class Decoder:
    def __init__(self, cpu):
        self.cpu = cpu
    
    def convert_to_number(self, variable):
        if variable.isnumeric():
            return int(variable)
        if variable.startswith("_R"):
            return self.cpu.register[variable]
        else:
            return self.cpu.CurTask.stack[variable]
    
    def set_instr(self, instr):
        args = instr.split(" ")
        if args[1].startswith("_R"):
            self.cpu.register[args[1]] = self.convert_to_number(args[2])
        else:
            self.cpu.CurTask.stack[args[1]] = self.convert_to_number(args[2])
        return None
    
    def add_instr(self, instr):
        args = instr.split(" ")
        if args[3].startswith("_R"):
            self.cpu.register[args[3]] = self.convert_to_number(args[1]) + self.convert_to_number(args[2])
        else:
            self.cpu.CurTask.stack[args[3]] = self.convert_to_number(args[1]) + self.convert_to_number(args[2])
        return None
    
    def sub_instr(self, instr):
        args = instr.split(" ")
        if args[3].startswith("_R"):
            self.cpu.register[args[3]] = self.convert_to_number(args[1]) - self.convert_to_number(args[2])
        else:
            self.cpu.CurTask.stack[args[3]] = self.convert_to_number(args[1]) - self.convert_to_number(args[2])
        return None
            
    def mul_instr(self, instr):
        args = instr.split(" ")
        if args[3].startswith("_R"):
            self.cpu.register[args[3]] = self.convert_to_number(args[1]) * self.convert_to_number(args[2])
        else:
            self.cpu.CurTask.stack[args[3]] = self.convert_to_number(args[1]) * self.convert_to_number(args[2])
        return None
    
    def IOrq_instr(self, instr):
        args = instr.split(" ")
        self.cpu.IO_FLAG = 1
        return 2
            
    def end_instr(self, args):
        return 1
    
    def excute(self):
        instr = self.cpu.CurTask.instrucMem[self.cpu.CurTask.pc]
        args = instr.split(" ")
        instr_list = {
            "set":self.set_instr,
            "add":self.add_instr,
            "sub":self.sub_instr,
            "mul":self.mul_instr,
            "end":self.end_instr,
            "iorequest": self.IOrq_instr
        }
        res = instr_list[args[0]](instr)
        self.cpu.clock = self.cpu.clock + 1
        self.cpu.scheduler.time_slice = self.cpu.scheduler.time_slice + 1
        self.cpu.CurTask.pc = self.cpu.CurTask.pc + 1
        return res
    