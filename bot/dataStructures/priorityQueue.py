class PriorityQueue():
    def __init__(self):
        self.queue = []

    def __str__(self):
        return self.queue.__str__()

    # def __iter__(self):
    #     for priority in self.queue:
    #         yield priority[0]
    
    def isEmpty(self):
        return len(self.queue) == []

    def enqueue(self, unit_id):
        self.queue.insert(len(self.queue), unit_id)
        
    def dequeue(self):
        return self.queue.pop(0)

    def delete(self, unit_id):
        for idx, unit in enumerate(self.queue):
            if unit == unit_id:
                del self.queue[idx]
    
    def reprioritize(self, unit_id, newPriority):
        self.delete(unit_id)
        # if newpriority is smaller than current queue then put
        # it in the middle, if not put it in the end
    

q = PriorityQueue()

unit1 = 'unit1'
unit2 = 'unit2'
unit3 = 'unit3'
unit4 = 'unit4'
unit5 = 'unit5'

q.enqueue(unit1)
q.enqueue(unit2)
q.enqueue(unit3)

for idx, val in enumerate(q.queue):
    print(idx, val)

q.dequeue()

for idx, val in enumerate(q.queue):
    print(idx, val)

q.delete(unit2)

for idx, val in enumerate(q.queue):
    print(idx, val)

    
    
