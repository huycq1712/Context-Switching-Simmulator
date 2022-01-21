from lib import *
from process import *
from decode import *
from sched import * 


class CPU:
    """Mô phỏng một CPU với bộ lập dịch, bộ decoder và các hàng đợi
    """
    def __init__(self, QTtime, maxPID = 100):
        self.clock = 0
        self.pidmanager = PIDmanager(maxPID)
        self.decoder = Decoder(self)
        self.register = { "_R1":0,
                          "_R2":0,
                          "_R3":0,
                          "_R4":0}
        self.task_list = []
        self.RunQueue = Queue()
        self.WaitQueue = Queue()
        self.preQueue = dict()
        self.FinishTask = None
        self.scheduler = Scheduler(QTtime)
        self.IO_FLAG = 0
        self.CurTask = None
    
    def rescheduler(self):
        """Tái lập lịch
        """
        self.FinishTask = self.RunQueue.deQueue().task_struct
        self.CurTask = self.RunQueue.header.next.task_struct
        if self.RunQueue.num != 0:
            print("============================CONTEXT SWITCH=================================")
            print("------------------------------------------------------------------------")
            print("Load process: Process", self.CurTask.pid)
            print("Swap in: Process", self.CurTask.pid)
            print("stack:",self.CurTask.stack)
            print("regis:",self.CurTask.process_context.register)
            self.swap_in(self.CurTask)
            print("------------------------------------------------------------------------")
            print("===========================================================================")
        
    def swap_in(self, process):
        """Cơ chế Swap in trong context switch

        Args:
            process (task_struct)): Tiến trình được swap in
        """
        self.register["_R1"] = process.process_context.register["_R1"]
        self.register["_R2"] = process.process_context.register["_R2"]
        self.register["_R3"] = process.process_context.register["_R3"]
        self.register["_R4"] = process.process_context.register["_R4"]
        
    def swap_out(self, process):
        """Cơ chế Swap out trong context switch

        Args:
            process (task_struct): Tiến trình bị swap out
        """
        process.process_context.register["_R1"] = self.register["_R1"]
        process.process_context.register["_R2"] = self.register["_R2"]
        process.process_context.register["_R3"] = self.register["_R3"]
        process.process_context.register["_R4"] = self.register["_R4"]
        
    def remove_from_tasklist(self, process):
        """Xóa một tiến trình khỏi TaskList khi nó hoàn thành

        Args:
            process (task_struct): task_struct của tiến trình cần xóa
        """
        for indx ,task in enumerate(self.task_list):
            if task.pid == process.pid:
                self.task_list.pop(indx)
    
    def IO_handle(self):
        """Xử lý tiến trình khi có yêu cầu I/O
        """
        print("------------------------------------------------------------------------")
        print("                                IO request                              ")
        print("------------------------------------------------------------------------")
        print("                Đưa tiến trình Process {} vào WaitQueue                 ".format(self.CurTask.pid))
        self.CurTask.state = TASK_STATE["WAITING"]
        self.RunQueue.deQueue()
        self.WaitQueue.enQueue(Node(self.CurTask))
        self.swap_out(self.CurTask)
        print("Swap out process: Process {}".format(self.CurTask.pid))
        print("stack:",self.CurTask.stack)
        print("regis:",self.CurTask.process_context.register)
        
        if self.RunQueue.num != 0:
            self.CurTask = self.RunQueue.header.next.task_struct
            self.swap_in(self.CurTask)
            print("Swap in process: Process {}".format(self.CurTask.pid))
            print("stack:",self.CurTask.stack)
            print("regis:",self.CurTask.process_context.register)
        else:
            self.CurTask = None
        print("RunQueue:", self.RunQueue.get_id_process())
        print("WaitQueue:", self.WaitQueue.get_id_process())
        print("------------------------------------------------------------------------")
        
    def release(self):
        """Giải phóng thanh ghi khi tiến trình chạy xong
        """
        self.register["_R1"] = 0
        self.register["_R2"] = 0
        self.register["_R3"] = 0
        self.register["_R4"] = 0
    
    def wake_up(self, io_file):
        file = open(io_file, "r")
        lines = file.readlines()
        for line in lines:
            if line == "respone":
                wakeup_task = self.WaitQueue.deQueue().task_struct
                wakeup_task.state = TASK_STATE["RUNNING"]
                print("                               IO respone                           ")
                print("===> Wake up process: Process ", wakeup_task.pid)
                self.RunQueue.enQueue(Node(wakeup_task))
                self.CurTask = self.RunQueue.header.next.task_struct
                self.IO_FLAG = 0
    
    
class PIDmanager:
    """Quản lý các giá trị PID
    """
    def __init__(self, maxPid=100):
        self.max = maxPid
        self.max_cur = 0
        self.used_pid = [0]*self.max
    
    def createPid(self, process):
        if self.max_cur == self.max:
            process.pid = self.used_pid.index(0)
            self.used_pid[self.used_pid.index(0)] = 1
        else:
            process.pid = self.max_cur
            self.max_cur = self.max_cur + 1
    
    def removePid(self, process):
        self.used_pid[process.pid] = 0
        if self.max_cur == process.pid:
            self.max_cur = self.used_pid.reverse().index(1) - 1 + self.max
            self.used_pid.reverse()