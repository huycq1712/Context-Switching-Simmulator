class Node:
    def __init__(self, task_struct=None, prevNode=None, nextNode=None) -> None:
        self.task_struct = task_struct
        self.prev = prevNode
        self.next = nextNode


class Queue:
    def __init__(self) -> None:
        self.num = 0
        self.header = Node()
        self.tailer = Node()
        self.header.next = self.tailer
        self.tailer.prev = self.header
        
    
    def enQueue(self, Node):
        last_node = self.tailer.prev
        last_node.next = Node
        Node.prev = last_node
        Node.next = self.tailer
        self.tailer.prev = Node
        self.num = self.num + 1
        return Node
        
    def deQueue(self):
        if self.num == 0:
            raise ValueError("Queue is empty")
        else:
            first_node = self.header.next
            self.header.next = first_node.next
            first_node.next.prev = self.header
            self.num = self.num - 1
        
        return first_node
    
    def get_id_process(self):
        res = []
        if self.num != 0:
            ptr = self.header.next
            while(ptr != self.tailer):
                res.append("process " + str(ptr.task_struct.pid))
                ptr = ptr.next
        return res


