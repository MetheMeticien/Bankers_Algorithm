import numpy as np

def print_state(step, processes, allocation, need, finish, work):
    print(f"Step {step}:")
    print("-" * 80)
    header = f"{'Process':>8} | {'Allocation':>20} | {'Need':>20} | {'Finish':>8}"
    print(header)
    print("-" * len(header))
    for i in range(len(processes)):
        alloc_str = str(list(allocation[i].data))
        need_str = str(list(need[i].data))
        finish_str = str(finish[i])
        print(
            f"{processes[i]:>8} | {alloc_str:>20} | {need_str:>20} | {finish_str:>8}")
    print("-" * len(header))
    print(f"Available (Work): {list(work.data)}")
    print("-" * 80)
    print()


def is_safe_state(processes, available, max_demand, allocation):
    num_processes = len(processes)

    # Calculate the need matrix and initialize work and finish arrays
    need = max_demand - allocation
    work = available.copy()
    finish = np.zeros(num_processes, dtype=bool)
    safe_sequence = []

    step = 0
    print_state(step, processes, allocation, need, finish, work)

    while len(safe_sequence) < num_processes:
        allocated = False
        for i in range(num_processes):
            # Check if process i can be allocated
            if not finish[i] and np.all(need[i] <= work):
                print(
                    f"Process {processes[i]} can be allocated: Need {list(need[i])} <= Available {list(work)}")
                # Release resources when process i finishes
                work += allocation[i]
                finish[i] = True       # Mark process i as finished
                safe_sequence.append(processes[i])
                step += 1
                print_state(step, processes, allocation, need, finish, work)
                allocated = True
                break

        # If no process could be allocated in this iteration, the system is unsafe.
        if not allocated:
            print("No further allocation possible. System is in an unsafe state!")
            return False, []

    return True, safe_sequence

def find_safe_sequences(processes, available, max_demand, allocation, need, work, finish, sequence, safe_sequences):
    allocated = False
    for i in range(len(processes)):
        if not finish[i] and all(need[i] <= work):
            finish[i] = True
            new_work = work + allocation[i]
            find_safe_sequences(processes, available, max_demand, allocation, need, new_work, finish.copy(), sequence + [processes[i]], safe_sequences)
            finish[i] = False
            allocated = True
    
    if not allocated:
        if all(finish):
            safe_sequences.append(sequence)

def get_all_safe_sequences(processes, available, max_demand, allocation):
    need = max_demand - allocation
    work = available.copy()
    finish = np.zeros(len(processes), dtype=bool)
    safe_sequences = []
    find_safe_sequences(processes, available, max_demand, allocation, need, work, finish, [], safe_sequences)
    return safe_sequences

# Example usage

def invalid_file(x=""):
    print("Invalid File Format")

def main():

    FILE_NAME = input("Enter file name: ")
    file_is_valid = True
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        file_is_valid = False
    
    if not file_is_valid: 
        invalid_file()
        return

    def checkInput(lines):
        global file_is_valid
        lengths = set([])
        for line in lines:
            lengths.add(len(line.split("	")))
        if len(lengths) != 1:
            file_is_valid = False


    checkInput(lines)

    if not file_is_valid: 
        invalid_file()
        return

    max_demand = []
    allocation = []
    processes = []
    available = []

    headings = lines[0].split("	")

    try:
        for row in range(1, len(lines)):
            line = lines[row].split("	")
            row_allocation = []
            row_max_demand = []
            for col in range(0, len(line)):
                value = line[col]
                heading = headings[col].lower()
                # print(heading, end=" ")
                if "allocation" in heading:
                    row_allocation.append(int(value))
                elif "max" in heading:
                    row_max_demand.append(int(value))
                elif "available" in heading and row == 1:
                    available.append(int(value))
                elif "pid" in heading:
                    processes.append(value)
            allocation.append(row_allocation)
            max_demand.append(row_max_demand)
    except:
        file_is_valid = False

    if not file_is_valid: 
        invalid_file()
        return

    available = np.array(available)  # Available resources
    max_demand = np.array(max_demand)
    allocation = np.array(allocation)

    if not (len(processes) == max_demand.shape[0] == allocation.shape[0]):
        file_is_valid = False
    if not (available.shape[0] == max_demand.shape[1] == allocation.shape[1]):
        file_is_valid = False

    if not file_is_valid: 
        invalid_file()
        return

    print("Valid File Format")

    safe, sequence = is_safe_state(
        processes, available, max_demand, allocation)
    if safe:
        print("System is in a safe state.")
        print("Safe sequence:", sequence)
        safe_sequences = get_all_safe_sequences(processes, available, max_demand, allocation)
        print("Similarly, all possible safe sequences are: ")
        for i, seq in enumerate(safe_sequences):
            print(i+1, "-->", seq)
    else:
        print("System is in an unsafe state!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("There was an error", e)
