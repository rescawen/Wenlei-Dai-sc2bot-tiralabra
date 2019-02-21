class PriorityQueue():
    def __init__(self):
        self.queue = []

    def __str__(self):
        return self.queue.__str__()
    
    def isEmpty(self):
        return len(self.queue) == []

    def enqueue(self, unit_id, priority):
        if self.isEmpty:
            self.queue.insert(0, (unit_id, priority))
    

q = PriorityQueue()

unit1 = 'unit1'

q.enqueue(unit1, 1)

print(q)

    
    
