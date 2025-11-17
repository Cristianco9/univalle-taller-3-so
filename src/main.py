#!/usr/bin/env python3
import time
import os
import sys
import threading

# Color to the CLI
class Color:
    """ANSI codes used to colorized the CLI output"""
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"

# Bakery algorithm
"""
Implementation Bakery algorithm for mutual exclusion.

Allow:

    - Strict mutual exclusion
    - Process between threads
    - limited timing

Global structures:

    choosing[] : flag that indicate if a threading is choosing a number
    number[] : assigned thread turn

"""

bakery_mutex = threading.Lock()
choosing = []
number = []

def ensure_bakery_size(idx : int):
    """
    Guarantees these arrays choosing[] and number[] have space to the index

    Args:
        idx (int): index required for the thread
    """

    with bakery_mutex:
        while idx >= len(choosing):
            choosing.append(False)
            number.append(0)


def bakery_lock(i : int):
    """
    Require access to the Critical Section using the Bakery algorithm

    Args:
        i (int): Identifier the thread in the bakery
    """
    ensure_bakery_size(i)
    choosing[i] = True

    max_num : int = max(number) if number else 0
    number[i] = max_num + 1
    choosing[i] = False

    for j in range(len(number)):
        # Wait to the another thread finish to choose a number
        while choosing[j]:
            time.sleep(0.001)

            # Rules to the another turn
            while number[j] != 0 and (number[j] < number[i] or (number[j] == number[i] and j < i)):
                time.sleep(0.001)


def bakery_unlock(i : int):
    """
    Set free the Critical Section for the 'i' thread

    Args:
        i (int): Thread identifier in the Bakery algorithm
    """
    number[i] = 0


# PCB: Process
class Process:
    """
    Represente a process inside the Simulator

    Attributes:

        pid (int): Unique process identifier
        burst_time (int): Total execution time required
        remaining (int):  Remaining execution time
        state (str): Process state: NEW, READY, RUNNING, TERMINATED.
        priority (int): Process priority
        thread (Thread): Thread associated to this process
        bakery_id (int): Algorithm ID to guarantees mutual exclusion

    """

    def __init__(self, pid : int, burst_time : int, priority = 1, bakery_id = None):
        self.pid : int = pid
        self.burst_time : int = burst_time
        self.remaining  : int = burst_time
        self.state : str = "NEW"
        self.priority : int = priority
        self.thread = None
        self.bakery_id : int = bakery_id

    def set_state(self, new_state : str):
        """
        Update the process state with the Bakery algorithm output

        Args:

            new_state (str) : New process state
        """

        if self.bakery_id is not None:
            bakery_lock(self.bakery_id)

            try:
                print(f"{Color.CYAN}[PCB] {self.pid}: {self.state} -> {new_state}{Color.RESET}")
            finally:
                bakery_unlock(self.bakery_id)

        self.state = new_state
        time.sleep(3)


# Global system state
class System:
    """
    Manage the general system state simulated: Stack, Threads, and assignation

    Attributes:

        ready_queue (list[Process]): Process stack in state 'READY'
        terminated (list[Process]):  Array with process finished
        running_threads (list[Thread]): Threads executing
        last_pid (int): Last PID assigned
        bakery_id_counter (int): IDs counter in the Bakery algorithm
        assign_lock (Lock): Block for secure ID assignation in the Bakery
    """

    def __init__(self):
        self.ready_queue = []
        self.terminated = []
        self.running_threads = []
        self.last_pid = 0
        self.bakery_id_counter = 0
        self.assign_lock = threading.Lock()

    def reset(self):
        """
        Reset completed the system
        """

        self.ready_queue = []
        self.terminated = []
        self.running_threads = []
        self.last_pid = 0
        self.bakery_id_counter = 0

        global choosing, number
        with bakery_mutex:
            choosing = []
            number = []

    def allocate_bakery_id(self):
        """
        Get new ID to the process inside the Bakery algorithm

        Returns:
            int : ID assigned
        """
        with self.assign_lock:
            idx = self.bakery_id_counter
            self.bakery_id_counter +=1
            ensure_bakery_size(idx)
            return idx
        

SYSTEM = System()

# Scheduler
class Scheduler:
    """
    Scheduler who init and manage the threads process

    Args:
        debug (bool): Active or Deactivate the message
    """

    def __init__(self, debug = True):
        self.debug = debug

    def debug_log(self, msg : str):
        """
        Print the debug message with Bakery protection
        """
        if self.debug:
            with bakery_mutex:
                print(f"{Color.MAGENTA}[DEBUG] {msg}{Color.RESET}")
            time.sleep(1)

    def run_process(self, process: Process):
        """
        Main loop to process execution

        Args:
            process (Process): Process to execute
        """
        process.set_state("RUNNING")
        self.debug_log(f"PID {process.pid} executing in Thread {threading.current_thread().name}")

        while process.remaining > 0:
            time.sleep(1)
            process.remaining -= 1

        process.set_state("TERMINATED")

        bakery_lock(process.bakery_id)

        try:
            SYSTEM.terminated.append(process)
        finally:
            bakery_unlock(process.bakery_id)

        self.debug_log(f"PID {process.pid} finish execution.")

    def start_thread(self, process: Process):
        """
        Initialize a Thread associate to a process

        Args:
            process (Process): Process to run
        """

        t = threading.Thread(target=self.run_process, args=(process,), daemon=True)
        process.thread = t

        bakery_lock(process.bakery_id)

        try:
            SYSTEM.running_threads.append(t)
        finally:
            bakery_unlock(process.bakery_id)

        t.start()


# Option 1: Multi thread simulation
def option_1_simulate_process():
    """
    Create multi process and execute it in independent threads using
    bakery algorithm
    """

    os.system("clear")
    print(f"{Color.BOLD}MULTI THREAD SIMULATION - BAKERY ALGORITHM {Color.RESET}\n")

    scheduler = Scheduler()
    bursts = (5, 3, 4)

    for burst in bursts:
        SYSTEM.last_pid += 1
        b_id = SYSTEM.allocate_bakery_id()
        proc = Process(SYSTEM.last_pid, burst, bakery_id=b_id)

        bakery_lock(proc.bakery_id)

        try:
            proc.set_state("READY")
            SYSTEM.ready_queue.append(proc)
        finally:
            bakery_unlock(proc.bakery_id)

        scheduler.start_thread(proc)

    print(f"{Color.GREEN}Process executing in independent threads.{Color.RESET}")
    print(f"{Color.YELLOW}Waiting for them to finish...{Color.RESET}")

    with bakery_mutex:
        threads_snapshot = SYSTEM.running_threads[:]

    for t in threads_snapshot:
        t.join()

    with bakery_mutex:
        SYSTEM.running_threads = []

    print(f"{Color.GREEN}All process have been finished.{Color.RESET}")
    input("Press ENTER to return...")


# Option 2: System state in independent thread
def thread_state():
    """
    Thread responsible to showing the system state without block main thread
    """

    os.system("clear")
    print(f"{Color.BOLD}=== SYSTEM STATE (THREAD ===){Color.RESET}\n")

    with bakery_mutex:
        ready_snapshot = list(SYSTEM.ready_queue)
        term_snapshot = list(SYSTEM.terminated)

    print("Process READY:")

    if ready_snapshot:
        for p in ready_snapshot:
            print(f"   P{p.pid}: {p.state} ({p.remaining}s remaining)")
    else:
        print("  None")

    print("\nProcess FINISHED:")

    if term_snapshot:
        for p in term_snapshot:
            print(f"   P{p.pid}: TERMINATED (burst={p.burst_time})")
    else:
        print("  None")

    print()
    input("Press ENTER to return...")

def option_2_show_state():
    """
    Throw a Thread to display the system state
    """

    thread = threading.Thread(target=thread_state)
    thread.start()
    thread.join()

# Option 3: clear the independent threads in the system
def thread_cleaner():
    """
    Thread responsible to restart the system global state
    """
    os.system("clear")
    SYSTEM.reset()
    print(f"{Color.GREEN}System restarted successfully.{Color.RESET}")
    time.sleep(1)
    input("Press ENTER to return...")

def option_3_clear_system():
    """
    Start an independent thread to clear the system
    """
    thread = threading.Thread(target=thread_cleaner)
    thread.start()
    thread.join()

# Main menu
def menu():
    """
    Interactive menu. Allow:

        1. Create process in thread
        2. Display the system state in independent thread
        3. Restart the system in independent thread
        4. Exit the program
    """
    while True:
        os.system("clear")
        print(f"{Color.BOLD}=== MULTI THREAD SIMULATOR ==={Color.RESET}")
        print("1. Create process in independent threads")
        print("2. Display the system state")
        print("3. Restart the system")
        print("4. Exit\n")

        op : int = int(input("Choose an option: "))

        if op == 1:
            option_1_simulate_process()
        elif op == 2:
            option_2_show_state()
        elif op == 3:
            option_3_clear_system()
        elif op == 4:
            print("Exit......")
            sys.exit(0)
        else:
            print("Wrong option.")
            time.sleep(1)
            


if __name__ == "__main__":
    menu()