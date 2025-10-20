from collections import deque

queue = deque([1,2,3])
queue.append(4)

print(queue)

# Implementing queue from scratch

class Node:
    def __init__(self, data, next=None):
        self.data = data 
        self.next = next

class Queue:
    def __init__(self, head:Node, tail:Node=None):
        self.head = head 
        self.tail = tail
    
    def enqueue(self,node):
        if self.head is None:
           self.head = node
        else:
            self.tail.next = node
        self.tail = node
    
    def dequeue(self):
        if self.head:
            current_node = self.head
            self.head = self.head.next 
            current_node.next = None 
            return current_node
        if self.head is None:
            return None
    
    
    
    