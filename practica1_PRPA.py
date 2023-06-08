from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import random, randint

N = 10         #Número de elementos que produce cada productor
NPROD = 3      #Número de productores
C = 4          #Capacidad del almacén para cada productor

def delay(factor = 3):
    sleep(random()/factor)

def producer(p, storage, empty, non_empty, mutex):
    current = 0 
    ind_p = 0   #indica donde colocar el nuevo producto
    for v in range(N):
        
        empty.acquire()
        print (f"producer {current_process().name} produciendo")
        current += randint(0, 5) #se genera el nuevo producto
        mutex.acquire()
        storage[p][ind_p] = current #se almacena el nuevo producto
        print (f"producer {current_process().name} almacenado {v}")
        ind_p = (ind_p + 1) % C #pasamos a la siguiente posición
        mutex.release()
        non_empty.release()
        
    #Se añade un -1 en la posición correspondiente del almacén si no se van a 
    #producir más elementos 
    empty.acquire()
    storage[p][ind_p] = -1
    non_empty.release()

def consumer(storage, empty, non_empty, mutex):

    result = []
    ind_c = [0 for _ in range(NPROD)] #indica qué elemento mirar del almacén
    #de cada productor
    
    #Esperamos a que todos los nuevos productos están en el almacén: 
    #bloquear todos los semaforos del consumidor
    for i in range(NPROD):
        non_empty[i].acquire()
        
    lista = [storage[i][ind_c[i]] for i in range(NPROD)] #Se toman del almacén  
    #general (storage) las posiciones ind_c del almacén de cada productor
    
    while max(lista) > -1:
        m = max(lista)
        prod = 0   
        
        #Hallamos el elemento más pequeño
        for i in range(NPROD):
            mutex[i].acquire()
            
            if lista[i] <= m and lista[i]>=0:
                m = lista[i]
                prod = i
            mutex[i].release()
        
        ind_c[prod] = (ind_c[prod] + 1) % C #Pasamos a la siguiente 
        #posición del almacén del productor de donde hemos cogido el menor
        #elemento
        
        print (f"consumer {current_process().name} consumiendo {m}") 
        
        #Bloquear el semáforo del productor del elemento mínimo
        non_empty[prod].acquire()
        
        #Liberar semáforo del productor del elemento mínimo
        empty[prod].release()
        lista[prod] = storage[prod][ind_c[prod]] #Cambiamos el elemento 
        #correspondiente al productor del que hemos cogido el menor elemento
        
        result.append(m) #Guardamos el menor elemento
    print(result)

def main():
    #Se genera el almacén general (storage)
    storage = []
    for i in range(NPROD):
        st = Array('i', C)
        for i in range(C):
            st[i] = -2
        storage.append(st)
        
    #Se generan los semáforos de los productores y del consumidor
    non_empty = [Semaphore(0) for _ in range(NPROD)]
    empty = [BoundedSemaphore(C) for _ in range(NPROD)]
    mutex = [Lock() for _ in range(NPROD)]

    prodlst = [ Process(target=producer,
                        name=f'prod_{i}',
                        args=(i,storage, empty[i], non_empty[i], mutex[i]))
                for i in range(NPROD) ]

    conslst = [ Process(target=consumer,
                      args=(storage, empty, non_empty, mutex)) ]

    for p in prodlst + conslst:
        p.start()

    for p in prodlst + conslst:
        p.join()

if __name__ == '__main__':
    main()


