from shell import *
from decode import *
from cpu import *
from sched import *
from process import *

if __name__ == '__main__':
    myshell = Shell()
    print("============================================================================")
    print("                           CONTEXT SWITCH SIMULATOR                         ")
    print("============================================================================")
    print("boot - Khởi tạo CPU")
    print("create - Tạo tiến trình với file mã code được chỉ định")
    print("run - Bắt đầu mô phỏng các tiến trình")
    print("help - Xem các lệnh có thể sử dụng")
    print("exit - Thoát khỏi chương trình")
    print("============================================================================")
    print("")
    while(1):
        in_cmd = input(">> ")
        res = myshell.excute_cmd(in_cmd)
        
        # exit
        if res == 1:
            break