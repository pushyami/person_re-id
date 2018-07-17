class Memory_Storage:

    def __init__(self):
        self.storage = {}
        self.counter = 0

    def insert(self, mem_object):
        self.storage["Frame " + str(self.counter)] = mem_object
        self.counter += 1

    def retrieve(self, frame_name):
        return self.storage[frame_name]


    def to_string(self):
        to_ret = ""
        for x in self.storage:
            to_ret += x + ": " + self.storage[x].to_string()

        return to_ret
