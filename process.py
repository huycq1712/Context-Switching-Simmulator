TASK_STATE = {
    "RUNNING": 0, 
    "READY":1,
    "WAITING":2
}
class task_struct:
    """Chứa thông tin của tiến trihf
    """
    def __init__(self, 
                    state,
                    pid = 0,
                    excute_code=None,
                    arrival_time=0):
        """Khởi tạo thông tin một tiến trình

        Args:
            state (int): Trạng thái tiến trình
            pid (int, optional): Mã định danh của tiến trình. Defaults to 0.
            excute_code (string, optional): Tên file chứa mã code cho tiến trình. Defaults to None.
            arrival_time (int, optional): Thời gian đến của tiến trình. Defaults to 0.
        """
        self.state = state
        self.pid = pid
        self.pc = 0;
        self.stack = {}
        self.excute_code = excute_code
        self.process_context = ProcessContext()
        self.arrival_time = arrival_time
        self.instrucMem = load_instruct(self.excute_code)


class ProcessContext:
    """Chứa ngữ cảnh phần cứu khi xảy ra context switch
    """
    def __init__(self):
        self.register = {"_R1":0,
                          "_R2":0,
                          "_R3":0,
                          "_R4":0}
        self.switched = False
        
def load_instruct(file_name):
    """Tải mã code từ file code

    Args:
        file_name (string): Địa chỉ file chứa code

    Returns:
        List: Danh sách các lệnh
    """
    instructors = []
    file = open(file_name, 'r')
    lines = file.readlines()
    for line in lines:
        instructors.append(line.replace("\n", ""))
    return instructors