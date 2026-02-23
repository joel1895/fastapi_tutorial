import time
from timeit import default_timer as timer

def run_tasks(name,seconds):
    print(f"{name} started at: {timer()}")
    time.sleep(seconds)
    print(f"{name} completed at: {timer()}")


start = timer()
run_tasks("Task 1",2)
run_tasks("Task 2",1)
run_tasks("Tasks 3",3)
print(f"Total time taken: {timer() - start:.2f} s")
