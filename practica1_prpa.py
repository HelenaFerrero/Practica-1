from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import random, randint

N = 20
NPROD = 3

def delay(factor = 3):
    sleep(random()/factor)

def producer(p, storage, empty, non_empty):
    current = 0
    for v in range(N):
        print (f"producer {current_process().name} produciendo")
        current += randint(0, 5)
        delay(6)
        empty.acquire()
        storage[p] = current
        non_empty.release()
        print (f"producer {current_process().name} almacenado {v}")
    empty.acquire()
    storage[p] = -1
    non_empty.release()    

def consumer(storage, empty, non_empty):
    result = []
    prod = 0
    for i in range(NPROD):
        non_empty[i].acquire()
    print (f"consumer {current_process().name} desalmacenando")
    while max(storage) > -1:
        menor = max(storage)
        for i in range(NPROD):
            if storage[i] <= menor and storage[i]>=0:
                menor = storage[i]
                prod = i        
        result.append(menor)
        print (f"consumer {current_process().name} consumiendo {menor}")
        empty[prod].release()
        non_empty[prod].acquire()
    print(result)
    delay()

def main():
    storage = Array('i', NPROD)
    for i in range(NPROD):
        storage[i] = -2
    print ("almacen inicial", storage[:])
    non_empty = [Semaphore(0) for _ in range(NPROD)]
    empty = [BoundedSemaphore(1) for _ in range(NPROD)]

    prodlst = [ Process(target=producer,
                        name=f'prod_{i}',
                        args=(i,storage, empty[i], non_empty[i]))
                for i in range(NPROD) ]

    conslst = [ Process(target=consumer,
                        args=(storage, empty, non_empty)) ]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()

if __name__ == '__main__':
    main()
