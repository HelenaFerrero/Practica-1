from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import random, randint

N = 10
NPROD = 3
NST = 4

def delay(factor = 3):
    sleep(random()/factor)

def producer(p, storage, empty, non_empty):
    current = 0
    ind_p = 0
    for v in range(N):
        empty.acquire()
        print (f"producer {current_process().name} produciendo")
        current += randint(0, 5)
        storage[p][ind_p] = current
        delay(6)
        print (f"producer {current_process().name} almacenado {v}")
        ind_p = (ind_p + 1) % NST
        non_empty.release()
    empty.acquire()
    storage[p][ind_p] = -1 
    non_empty.release()  

def consumer(storage, empty, non_empty):
    result = []
    prod = 0
    ind_c = [0 for _ in range(NPROD)]
    lista = [storage[i][ind_c[i]] for i in range(NPROD)]
    while max(lista) > -1:
        # Comprobar que todos han producido: bloquear todos los semaforos del consumidor
        for i in range(NPROD):
            non_empty[i].acquire()
        # Confeccionar la lista a partir del estado del storage, una vez que todos han producido
        lista = [storage[i][ind_c[i]] for i in range(NPROD)]
        # puede ocurrir que estando dentro del while, un productor ponga el último -1.
        if max(lista) > -1:
            menor = max(lista)
            for i in range(NPROD):
                if lista[i] <= menor and lista[i]>=0:
                    menor = lista[i]
                    prod = i
            ind_c[prod] = (ind_c[prod] + 1) % NST
            result.append(menor)
            print (f"consumer {current_process().name} consumiendo {menor}")            
        # Liberar semáforo del productor del número menor
        empty[prod].release()
        # Liberar todos los semaforos del consumidor
        for i in range(NPROD):
            non_empty[i].release()
        # Bloquear el semáforo del productor del número menor
        non_empty[prod].acquire()
    print(result)   
    
def main():
    storage = []
    for i in range(NPROD):
        st = Array('i', NST)
        for i in range(NST):
            st[i] = -2
        storage.append(st)
    non_empty = [Semaphore(0) for _ in range(NPROD)]
    empty = [Semaphore(1) for _ in range(NPROD)]
    
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
