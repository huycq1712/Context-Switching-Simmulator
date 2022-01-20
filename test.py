from multiprocessing import Process
import time

if __name__ == '__main__':
    while(1):
        file = open("io.txt", "r")
        lines = file.readlines()
        for line in lines:
            if line == "a":
                print("ok")
            else:
                print("no")
        time.sleep(1)
        