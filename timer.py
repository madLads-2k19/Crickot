import time

class Timer:
    startTime = None

    @classmethod
    def setStartTime(cls):
        cls.startTime = time.time()
        print("\nSET START TIME: 0.00\n")
    
    @classmethod
    def checkpoint(cls, text):
        print(f"\n\nCHECKPOINT {text}: {time.time() - cls.startTime}\n\n")