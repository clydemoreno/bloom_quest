
import multiprocessing

def worker(i, a,b,c, result_queue):
    print(i)
    result_queue.put((a+1, b+1, c+1))



def simulate():

    processes = []
    cores = multiprocessing.cpu_count()
    result_queue = multiprocessing.Queue()

    for i in range(cores):

        p = multiprocessing.Process(target=worker, args=(i,1,2,3, result_queue))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()



    total = 0
    for _ in range(cores):
        a,b,c  = result_queue.get()
        total += a + b + c

    print("Total:",total)

if __name__ == "__main__":
    simulate()

