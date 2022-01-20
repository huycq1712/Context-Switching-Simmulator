from process import *     
from lib import *    
from cpu import *

import time

class Shell:
    """Mô phỏng shell dùng để xử lý là chạy các lệnh do người dùng nhập
    """
    def __init__(self, cpu=None):
        """Khỏi tạo Shell

        Args:
            cpu (CPU, optional): CPU được sử dụng để thực hiện các lệnh trên shell. Defaults to None.
        """
        self.cpu = cpu
    
    def boot_cmd(self, cmd):
        """Khởi tạo CPU cho quá trình mô phỏng

        Args:
            cmd (string): Các tham số cho từ command
        """
        args = cmd.split(" ")
        self.cpu = CPU(int(args[1]))
        print("Khởi tạo CPU - Ok")
        print("Khởi tạo Decoder - Ok")
        print("Khởi tạo Scheduler - ok")
        print("Time Quantum: {}".format(args[1]))
        print("")
    
    def create_cmd(self, cmd):
        """Khởi tạo tiến trình

        Args:
            cmd (string): Các tham số cho từ command
        """
        args = cmd.split(" ")
        process = task_struct(state=TASK_STATE["READY"],
                              excute_code=args[1],
                              arrival_time=int(args[2]))
        self.cpu.pidmanager.createPid(process)
        if int(args[2]) in self.cpu.preQueue.keys():
            self.cpu.preQueue[int(args[2])].append(process)
        else:
            self.cpu.preQueue[int(args[2])] = [process,]
        
        print("Tạo tiến trình thành công: Process {}".format(process.pid))
        print("file excute code: {}".format(args[2]))
    
    def run_cmd(self, cmd):
        """Khởi chạy chương trình mô phỏng

        Args:
            cmd (string): Các tham số cho từ command
        """
        print("============================================================================")
        print(">>>>>>>>>>>>>>>>>>>>>         Start Running         <<<<<<<<<<<<<<<<<<<<<<<<")
        print("============================================================================")
        while(1):
            print("")
            if self.cpu.RunQueue.num + self.cpu.WaitQueue.num + len(self.cpu.preQueue) == 0:
                print("============================================================================")
                print(">>>>>>>>>>>>>>>>>>>>>>>      DONE ALL TASK!!!      <<<<<<<<<<<<<<<<<<<<<<<<<")
                print("============================================================================")
                break
            print("clock:", self.cpu.clock)
            # Kiểm tra hàng đợi xem có tiến trình nào muốn vào tại clock 
            if self.cpu.clock in self.cpu.preQueue.keys():
                for process in self.cpu.preQueue[self.cpu.clock]:
                    self.cpu.RunQueue.enQueue(Node(process))
                    print("Process {} dến => RunQueue".format(process.pid))
                del self.cpu.preQueue[self.cpu.clock]
                self.cpu.CurTask = self.cpu.RunQueue.header.next.task_struct

            print("RunQueue: Fontier =>", self.cpu.RunQueue.get_id_process())
            print("WaitQueue: Fontier =>", self.cpu.WaitQueue.get_id_process())

            # Nếu tiến chỉ còn tiến trình đang đợi thì sẽ tiếp tục đợi IO
            if self.cpu.WaitQueue.num !=0 and self.cpu.RunQueue.num == 0 and self.cpu.IO_FLAG:
                self.cpu.clock = self.cpu.clock + 1
                file = open("io.txt", "r")
                lines = file.readlines()
                for line in lines:
                    if line == "in":
                        wakeup_task = self.cpu.WaitQueue.deQueue().task_struct
                        wakeup_task.state = TASK_STATE["RUNNING"]
                        print("Wake up process: ", wakeup_task.pid)
                        self.cpu.RunQueue.enQueue(Node(wakeup_task))
                        self.cpu.CurTask = self.cpu.RunQueue.header.next.task_struct
                        self.cpu.IO_FLAG = 0
                time.sleep(1)
                continue
            
            # In ra thông tin tiến trình đang chạy
            print("Process ID {} || Process counter {} || Running instructer {}".format(self.cpu.CurTask.pid,
                                                                                    self.cpu.CurTask.pc,
                                                                                    self.cpu.CurTask.instrucMem[self.cpu.CurTask.pc]))
            #thực thi câu lệnh
            flag = self.cpu.decoder.excute()
            
            #nếu chạy đến lệnh end => tiến trình hoàn  => cần phải tải tiến trình tiếp theo lên nếu có
            if flag == 1:
                print("Finish Process: Process {}".format(self.cpu.CurTask.pid))
                print("============================Finish Process {}===============================".format(self.cpu.CurTask.pid))
                print("============================CONTEXT SWITCH=================================")
                self.cpu.release()
                self.cpu.scheduler.time_slice = 0
                self.cpu.rescheduler()
                print("===========================================================================")
                self.cpu.pidmanager.removePid(self.cpu.FinishTask)
                self.cpu.remove_from_tasklist(self.cpu.FinishTask)
            
            # nếu có câu lệnh yêu cầu IO
            elif flag == 2:
                print("                               IO request                           ")
                self.cpu.IO_handle()
                if self.cpu.RunQueue.num + self.cpu.WaitQueue.num + len(self.cpu.preQueue) == 0:
                    print("done")
                    continue
            
            # nếu yêu cầu IO vẫn chưa được thỏa mãn
            elif self.cpu.IO_FLAG:
                file = open("io.txt", "r")
                lines = file.readlines()
                for line in lines:
                    if line == "in":
                        wakeup_task = self.cpu.WaitQueue.deQueue().task_struct
                        wakeup_task.state = TASK_STATE["RUNNING"]
                        print("Wake up process: ", wakeup_task.pid)
                        self.cpu.RunQueue.enQueue(Node(wakeup_task))
                        self.cpu.IO_FLAG = 0
                
            # hết time slice mà tiến trình vẫn chưa xong
            if self.cpu.scheduler.time_slice == self.cpu.scheduler.QT_time and self.cpu.RunQueue.num > 1 and flag != 1:
                print("============================Time Quantum Out===============================")
                print("============================CONTEXT SWITCH=================================")
                self.cpu.scheduler.time_slice = 0
                self.cpu.FinishTask = self.cpu.RunQueue.deQueue().task_struct
                self.cpu.CurTask = self.cpu.RunQueue.header.next.task_struct
                self.cpu.RunQueue.enQueue(Node(self.cpu.FinishTask))
                
                self.cpu.swap_out(self.cpu.FinishTask)
                print("Swap out process: Process {}".format(self.cpu.FinishTask.pid))
                print("stack:",self.cpu.FinishTask.stack)
                print("regis:",self.cpu.FinishTask.process_context.register)
                self.cpu.swap_in(self.cpu.CurTask)
                print("Swap in process: Process {}".format(self.cpu.CurTask.pid))
                print("stack:",self.cpu.CurTask.stack)
                print("regis:",self.cpu.CurTask.process_context.register)
                print("============================================================================")
                
            # Nếu mà không còn tiên trình nào thì kết thúc
            
            time.sleep(1)
        
    def exit_cmd(self, cmd):
        """Thực hiện lệnh exit thoát khỏi chương trình

        Args:
            cmd (string): Các tham số cho từ command

        Returns:
            int: trả về 1 để đánh dấu cho chương trình kêt thúc
        """
        print("log out")
        return 1
    
    def excute_cmd(self, cmd):
        args = cmd.split(" ")
        cmd_lib = {
            "run":self.run_cmd,
            "boot": self.boot_cmd,
            "create": self.create_cmd,
            "exit": self.exit_cmd
        }
        return cmd_lib[args[0]](cmd)