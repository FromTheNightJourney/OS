import sys
# sys library used to take in the arguments from the command line

def FCFS(requests, initial_position):
    head_move = 0
    pos_now = initial_position
    
    for request in requests:
        head_move += abs(request - pos_now)
        pos_now = request
    
    return head_move

def SCAN(requests, init_pos):
    head_move = 0
    pos_now = init_pos
    index = 0
    
    # traverse list
    while index < len(requests) and requests[index] < init_pos:
        index += 1

    # split requests
    right = sorted(requests[index:])
    left = sorted(requests[:index], reverse=True)

    # for the requests in the left side, add head movement
    for request in left:
        head_move += abs(pos_now - request)
        pos_now = request
        
    pos_now = init_pos
    
    # for requests in right, add head movement
    for request in right:
        head_move += abs(pos_now - request)
        pos_now = request
        
    return head_move

def C_SCAN(requests, init_pos):
    head_move = 0  
    pos_now = init_pos 
    sorted_requests = sorted(requests)
    index = 0  
    disk_size = 4999
    
    # traverse reqs until end or find req greater than current position (pos_now)
    while index < len(requests) and requests[index] < init_pos:
        index += 1
        
        # split req into left and right of current position
    right = sorted(requests[index:])
    left = sorted(requests[:index])
        
    for request in right:
        head_move += abs(pos_now - request)  # add head movement for accessing the request
        pos_now = request

        # if req to the right exist, move to head until end of disk
    if right:
        head_move += abs(disk_size - pos_now)  # add head movement 
        pos_now = 0  # move the head to the beginning of disk
        head_move += disk_size  # add head movement for returning
            
        # process left requests
    for request in left:
        head_move += abs(pos_now - request)  
        pos_now = request
    return head_move



def main():
    if len(sys.argv) != 3:
        print("Usage: python disk_scheduler.py <initial_position> <input_file>")
        return

    initial_position = int(sys.argv[1])
    input_file = sys.argv[2]

    with open(input_file, 'r') as file:
        requests = [int(line.strip()) for line in file if line.strip().isdigit()]

    max_cylinder = 4999

    # Task 1
    print("Task 1 - FCFS:", FCFS(requests, initial_position))
    print("Task 1 - SCAN:", SCAN(requests, initial_position))
    print("Task 1 - C-SCAN:", C_SCAN(requests, initial_position))

    # Task 2
    print("Task 2 - FCFS:", FCFS(sorted(requests), initial_position))
    print("Task 2 - SCAN:", SCAN(sorted(requests), initial_position))
    print("Task 2 - C-SCAN:", C_SCAN(sorted(requests), initial_position))

if __name__ == "__main__":
    main()
