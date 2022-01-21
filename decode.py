class Decoder:
    """Giải mã và thực thi các lệnh khi tiến trình đươc chạy
    """
    def __init__(self, cpu):
        self.cpu = cpu
    
    def convert_to_number(self, variable):
        """Kiểm tra xem tham số hàm là chữ só, biến hay thanh ghi, nếu là biến hoặc thành ghi thì sẽ trả về giá trị của nó

        Args:
            variable (string): Tên tham số  hàm (ví dụ a, b, _R1)

        Returns:
            int: giá trị tương ứng với tham số
        """
        if variable.isnumeric():
            return int(variable)
        if variable.startswith("_R"):
            return self.cpu.register[variable]
        else:
            return self.cpu.CurTask.stack[variable]
    
    def set_instr(self, instr):
        """Thực thi hàm set gán một giá trị cho biến

        Args:
            instr (string): Câu lệnh set [] []

        Returns:
            [None]: None
        """
        args = instr.split(" ")
        if args[1].startswith("_R"):
            self.cpu.register[args[1]] = self.convert_to_number(args[2])
        else:
            self.cpu.CurTask.stack[args[1]] = self.convert_to_number(args[2])
        return None
    
    def add_instr(self, instr):
        """Thực thi lệnh add

        Args:
            instr (string): Câu lệnh add [] [] []

        Returns:
            [None]: None
        """
        args = instr.split(" ")
        if args[3].startswith("_R"):
            self.cpu.register[args[3]] = self.convert_to_number(args[1]) + self.convert_to_number(args[2])
        else:
            self.cpu.CurTask.stack[args[3]] = self.convert_to_number(args[1]) + self.convert_to_number(args[2])
        return None
    
    def sub_instr(self, instr):
        """Thực hiện lệnh sub

        Args:
            instr (string): Câu lệnh sub

        Returns:
            [None]: None
        """
        args = instr.split(" ")
        if args[3].startswith("_R"):
            self.cpu.register[args[3]] = self.convert_to_number(args[1]) - self.convert_to_number(args[2])
        else:
            self.cpu.CurTask.stack[args[3]] = self.convert_to_number(args[1]) - self.convert_to_number(args[2])
        return None
            
    def mul_instr(self, instr):
        """Thực hiện lệnh mul

        Args:
            instr ([type]): Câu lệnh mul

        Returns:
            None: None
        """
        args = instr.split(" ")
        if args[3].startswith("_R"):
            self.cpu.register[args[3]] = self.convert_to_number(args[1]) * self.convert_to_number(args[2])
        else:
            self.cpu.CurTask.stack[args[3]] = self.convert_to_number(args[1]) * self.convert_to_number(args[2])
        return None
    
    def IOrq_instr(self, instr):
        """Yêu cầu I/O

        Args:
            instr (string): Câu lệnh iorequest

        Returns:
            [int]: trả về 2 để đánh giá 
        """
        args = instr.split(" ")
        self.cpu.IO_FLAG = 1
        return 2
            
    def end_instr(self, args):
        """Kết thúc chương trình

        Args:
            args (string): Câu lệnh end

        Returns:
            int: Báo hiệu tiến trình kêt thúc
        """
        return 1
    
    def excute(self):
        """Thực thi lệnh

        Returns:
            int: Trả về giá trị thông báo cho hệ thống 1 là tiến trình kết thúc 2 yêu cầu IO
        """
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
    