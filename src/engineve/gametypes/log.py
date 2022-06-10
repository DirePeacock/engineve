class Log:
    def __init__(self, *args, **kwargs):
        self.history = []
        self.stack = []
    
    def write(self, obj):
        self.history.append(obj)
        