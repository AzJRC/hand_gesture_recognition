

class Timer():
    def __init__(self):
        self.timer = -1


    def startTimer(self, c_time: bool, s: int = 3, return_elapsed_time: bool = False):
        """
            Use the s parameter to define the wait time in seconds. Default = 3
            Timer will return True as soon as 0 is reached.
        """
        if self.timer == -1:
            self.timer = c_time + s
        elapsed_time = round(self.timer - c_time, 2)
        if elapsed_time <= 0:
            elapsed_time = 0
            return True
        if return_elapsed_time:
            return elapsed_time
        return False
    
    
    def resetTimer(self):
        """
            Set timer value to -1 which means timer is inactive
        """
        self.timer = -1