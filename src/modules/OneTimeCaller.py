class OneTimeCaller:
    def __init__(self):
        self.called = False

    def call(self, func):
        if not self.called:
            self.called = True
            func()

# # Usage
# reset_once = OneTimeCaller()

# reset_once.call(lambda: print("Resetting canvas..."))
