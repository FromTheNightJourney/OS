import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []  # Shared buffer to hold generated numbers
lock = threading.Lock()  # Lock to synchronize access to the shared buffer
producer_done = False  # Flag to indicate when the producer is done generating numbers
consumers_done = 0  # Counter to keep track of how many consumer threads have finished

# Function to generate random numbers and populate the buffer
def producer():
    global producer_done
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)  # Generate a random number
        with lock:
            buffer.append(num)  # Add the generated number to the buffer
            with open("all.txt", "a") as f:
                f.write(str(num) + "\n")  # Write the number to the 'all.txt' file
    producer_done = True  # Set the producer_done flag to True when done

# Function for consumers to consume odd numbers from the buffer
def consumer_odd():
    global consumers_done
    while not producer_done or buffer:  # Continue consuming while producer is not done or buffer is not empty
        with lock:
            if buffer and buffer[-1] % 2 == 1:  # Check if buffer is not empty and the last number is odd
                num = buffer.pop()  # Remove the last odd number from the buffer
                with open("odd.txt", "a") as f:
                    f.write(str(num) + "\n")  # Write the odd number to the 'odd.txt' file
        if producer_done and not buffer:  # If producer is done and buffer is empty, exit the loop
            break
    consumers_done += 1  # Increment the consumers_done counter when done

# Function for consumers to consume even numbers from the buffer
def consumer_even():
    global consumers_done
    while not producer_done or buffer:  # Continue consuming while producer is not done or buffer is not empty
        with lock:
            if buffer and buffer[-1] % 2 == 0:  # Check if buffer is not empty and the last number is even
                num = buffer.pop()  # Remove the last even number from the buffer
                with open("even.txt", "a") as f:
                    f.write(str(num) + "\n")  # Write the even number to the 'even.txt' file
        if producer_done and not buffer:  # If producer is done and buffer is empty, exit the loop
            break
    consumers_done += 1  # Increment the consumers_done counter when done

if __name__ == "__main__":
    # Create threads for producer and consumers
    producer_thread = threading.Thread(target=producer)
    consumer_odd_thread = threading.Thread(target=consumer_odd)
    consumer_even_thread = threading.Thread(target=consumer_even)

    # Start threads
    producer_thread.start()
    consumer_odd_thread.start()
    consumer_even_thread.start()

    # Wait for all threads to finish
    producer_thread.join()
    consumer_odd_thread.join()
    consumer_even_thread.join()

    # Wait for both consumer threads to finish
    while consumers_done < 2:
        pass  # Waiting for consumers to finish

    print("Program execution complete.")  # Print a message when the program execution is complete
