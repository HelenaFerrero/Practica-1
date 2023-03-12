from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import random, randint

N = 20
NPROD = 3
NST = 4
       

def delay(factor = 3):
    sleep(random()/factor)

def producer(p, storage, empty, non_empty):
    current = 0
    ind_p = 0
    for v in range(N):
        print (f"producer {current_process().name} produciendo")
        current += randint(0, 5)
        delay(6)
        empty.acquire()
        storage[p][ind_p] = current
        ind_p = (ind_p + 1) % NST
        non_empty.release()
        print (f"producer {current_process().name} almacenado {v}")
    empty.acquire()
    storage[p][ind_p % NST] = -1
    non_empty.release()    

def consumer(storage, empty, non_empty):
    result = []
    prod = 0
    ind_c = [0 for _ in range(NPROD)]
    lista = []
    for i in range(NPROD):
        non_empty[i].acquire()
        lista.append(storage[i][ind_c[i]])
    while max(lista) > -1:
        menor = max(lista)
        for i in range(NPROD):
            if lista[i] <= menor and lista[i]>=0:
                menor = lista[i]
                prod = i        
        result.append(menor)
        ind_c[prod] = (ind_c[prod] + 1) % NST
        lista[prod] = storage[prod][ind_c[prod]]
        print (f"consumer {current_process().name} consumiendo {menor}")
        empty[prod].release()
        non_empty[prod].acquire()
    print(result)
    delay()   
    

def main():
    st = Array('i', NST)
    for i in range(NST):
        st[i] = -2
    storage = [st for _ in range(NPROD)]
    non_empty = [Semaphore(0) for _ in range(NPROD)]
    empty = [BoundedSemaphore(NST) for _ in range(NPROD)]

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
