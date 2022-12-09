import multiprocessing as mp
import time


# funcion para hacer pruebas (suma 1 a los bits impares)
def f(im):
    for i in range(len(im)):
        blur_condition = i%2
        if blur_condition:
            im[i] += 1
    return im
#----------------------


# PRE: import multiprocessing as mp
# IN:  im_fragments = lista con fragmentos de una imagen / f = funcion para procesar cada fragmento
# OUT: im_fragments se ha actualizado 
def ejecutarEnParalelo(im_fragments, f):

    #optimizacion segun el pc
    np = mp.cpu_count()
    #print("Number of processors: ", np)
    pool = mp.Pool(np)

    #actualizacion de im_fragments tras ser procesado en paralelo con f
    im_fragments = pool.map(f, im_fragments)
    #print(print("paral im_fragments: ", im_fragments))
    
    pool.close() 


if __name__ == '__main__':

    # DATOS A PROCESAR
    # (simulo imagenes como listas de 0s, y blur es pasar del 0 al 1)
    imf1 = [0] * 32
    imf2 = [0] * 32
    imf3 = [0] * 32
    imf4 = [0] * 32
    imf5 = [0] * 32
    imf6 = [0] * 32
    imf7 = [0] * 32
    imf8 = [0] * 32
    im_fragments = [imf1,imf2,imf3,imf4,imf5,imf6,imf7,imf8]
    #print("im_fragments: ", im_fragments)
    #-----------


    #nota: con los datos de prueba tarda más la version pararlelizada porque tarda más pillar las librerias y tal
    #      pero con datos grandes imagino que mejorara
    """
    # Pruebas sin paralelizar
    t1 = time.time()
    for j in range(len(im_fragments)):
        im_fragments[j] = f(im_fragments[j])
    t2 = time.time()
    t = t2-t1
    print("TIEMPO: ", t, " s")
    print("im_fragments: ", im_fragments)
    #-------------------------


    
    # Pruebas paralelizado
    t1 = time.time()
    ejecutarEnParalelo(im_fragments,f)
    t2 = time.time()
    t = t2-t1
    print("TIEMPO: ", t, " s")
    #-------------------------
    """

    print("paralelizar.py ejecutado\n")
