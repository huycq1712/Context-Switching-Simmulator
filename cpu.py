from lib import *
from process import *
from decode import *
from sched import * 


class CPU:
    def __init__(self, QTtime):
        self.clock = 0
        self.pidmanager = PIDmanager()
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
        self.FinishTask = self.RunQueue.deQueue().task_struct
        self.CurTask = self.RunQueue.header.next.task_struct
        if self.RunQueue.num != 0:
            print("------------------------------------------------------------------------")
            print("Load process: process", self.CurTask.pid)
            self.swap_in(self.CurTask)
            print("------------------------------------------------------------------------")
        
    def swap_in(self, process):
        self.register["_R1"] = process.process_context.register["_R1"]
        self.register["_R2"] = process.process_context.register["_R2"]
        self.register["_R3"] = process.process_context.register["_R3"]
        self.register["_R4"] = process.process_context.register["_R4"]
        
    def swap_out(self, process):
        process.process_context.register["_R1"] = self.register["_R1"]
        process.process_context.register["_R2"] = self.register["_R2"]
        process.process_context.register["_R3"] = self.register["_R3"]
        process.process_context.register["_R4"] = self.register["_R4"]
        
    def remove_from_tasklist(self, process):
        for indx ,task in enumerate(self.task_list):
            if task.pid == process.pid:
                self.task_list.pop(indx)
    
    def IO_handle(self):
        print("------------------------------------------------------------------------")
        self.CurTask.state = TASK_STATE["WAITING"]
        self.RunQueue.deQueue()
        self.WaitQueue.enQueue(Node(self.CurTask))
        self.swap_out(self.CurTask)
        print("stack:",self.CurTask.stack)
        print("regis:",self.CurTask.process_context.register)
        
        if self.RunQueue.num != 0:
            self.CurTask = self.RunQueue.header.next.task_struct
        else:
            self.CurTask = None
        print("RunQueue:", self.RunQueue.get_id_process())
        print("WaitQueue:", self.WaitQueue.get_id_process())
        print("-------------------------------------------------------------------------")
        
    def release(self):
        self.register["_R1"] = 0
        self.register["_R2"] = 0
        self.register["_R3"] = 0
        self.register["_R4"] = 0
    
    
class PIDmanager:
    def __init__(self):
        self.max = 100
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