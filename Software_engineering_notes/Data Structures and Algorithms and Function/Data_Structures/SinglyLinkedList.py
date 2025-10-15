class Node:
    def __init__(self,data,next=None):
        self.data = data
        self.next = next
        
    def __str__(self):
        return str(self.data)

class LinkedList:
    def __init__(self,node:Node):
        self.head = node
        self.next = None
    def add(self, data):
        new_node=Node(data)
        if self.head: 
            new_node.next=self.head 
            self.head=new_node 
        else: 
            self.head=new_node
            self.tail=new_node
    def search(self,data):
        current_node=self.head
        while current_node: 
            if current_node.data==data: 
                return True
            else: 
                current_node=current_node.next
        return False
    
    def __str__(self):
        print_list = []
        while self.head:
            print_list.append(self.head.data)
            self.head = self.next
        return print_list

    
Head = Node(1)
A = Node(3)
B = Node(4)


