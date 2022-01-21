class Scheduler:
    """Chứa một số thông tin liên quan đến lập lịch
    """
    def __init__(self, QTtime):
        self.time_slice = 0
        self.QT_time = QTtime
    
        