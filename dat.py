class Queue:
    def __init__(self):
        self.q = []

    def push(self, node):
        self.q.append(node)

    def pop(self):
        if (len(self.q) > 0):
            out = self.q[0]
            del self.q[0]
            return out
        else:
            return None
    def peep(self):
        # this shouldnt be allowed but yeah ;)
        return self.q[0]