from timeit import default_timer as timer
import asyncio

async def run(task, seconds):
    print(f"{task} started at: {timer()}")
    await asyncio.sleep(seconds)
    print(f"{task} completed at: {timer()}")

async def main():
    start = timer()
    await asyncio.gather(
        run("Task1",2),
        run("Task2",1),
        run("Task3",3)
    )
    print(f"Total time taken: {timer() - start:.2f} s")

asyncio.run(main())