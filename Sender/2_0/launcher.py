import os
import time
import threading
import time

#####################METHODS#######################
def run_wheel():
    os.system("python sender_wheel2_0.py")
    
def run_level():
    os.system("python palanca2_0.py")

def start_program():
    wheel=threading.Thread(target=run_wheel)
    wheel.start()

    level=threading.Thread(target=run_level)
    level.start()

    wheel.join()
    level.join()



#####################MAIN#######################
if __name__ == "__main__":
    start_program()