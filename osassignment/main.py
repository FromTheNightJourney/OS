import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []
lock = threading.Lock()  # lock to sync acc to shared bufferlock
producer_done = False  # flag so we know when producer done generating nums
consumers_done = 0

# func for rand num gen and buffer population
def producer():
    global producer_done
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)  # RNG
        with lock:
            buffer.append(num)  
            with open("all.txt", "a") as f:
                f.write(str(num) + "\n") # write to all file
    producer_done = True 

# func for odd number buffer consumption
def consumer_odd():
    global consumers_done
    while not producer_done or buffer:  # keep going until buffer empty /producer no done
        with lock:
            if buffer and buffer[-1] % 2 == 1:  # check buffer not empty and if number is odd
                num = buffer.pop()  # pop odd number
                with open("odd.txt", "a") as f:
                    f.write(str(num) + "\n")  # add odd num to text file
        if producer_done and not buffer:  # exit condition
            break
    consumers_done += 1 

# func for even number buffer consumption
def consumer_even():
    global consumers_done
    while not producer_done or buffer: 
        with lock:
            if buffer and buffer[-1] % 2 == 0:  # check empty buffer and number even
                num = buffer.pop()  # pop even number
                with open("even.txt", "a") as f:
                    f.write(str(num) + "\n")  # add even num to text file
        if producer_done and not buffer:
            break
    consumers_done += 1 

if __name__ == "__main__":
    # thread creation
    producer_thread = threading.Thread(target=producer)
    consumer_odd_thread = threading.Thread(target=consumer_odd)
    consumer_even_thread = threading.Thread(target=consumer_even)

    producer_thread.start()
    consumer_odd_thread.start()
    consumer_even_thread.start()

    # waiting for all to finish
    producer_thread.join()
    consumer_odd_thread.join()
    consumer_even_thread.join()

    # wait for both consumer thread to finish
    while consumers_done < 2:
        pass  

    print("Program execution complete.")
