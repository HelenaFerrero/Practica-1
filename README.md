# Practica-1
En el fichero practica1_PRPA.py se da una solución en python al problema productor-onsumidor mediante el uso de semáforos. Las funciones que aparecen en dicho fichero son:

- main(): donde se generan los productores (cada uno produce N elementos), el almacén (storage) para poder guardar los elementos que van produciendo los productores, y los semáforos prara los productores y para el consumidor. Cada productor tiene un almacén propio de capacidad C dentro del almacén general (storage).

- producer(): medinate un bucle, permite que cada productor vaya produciendo sus N elementos y los guarde en el almacén. Cuando haya acabado de producir, se añade un -1 en la posición correspondiente del almacén para saber que ese productor ya no va a producir nada más.

-consumer(): cada vez que todos los productores hayan producido un nuevo elemento, se busca el producto más pequeño entre ellos, se consume y se guarda en la lista final.
