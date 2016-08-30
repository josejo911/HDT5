import simpy
import random

#UNIVERSIDAD DEL VALLE DE GUATEMALA
#ALGORITMOS Y ESTRUCTURA DE DATOS
#HOJA DE TRABAJO NO.5
#JENNIFER MARISOL BARILLAS,15307
#JOSE JAVIER JO, 14343
#ALGORITMO DE SIMULACION DE TIEMPO PARA CPU Y RAM ( SE TOMO DE BASE EJEMPLO2B )
#
# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador

# name: identificacion del proceso
# bcs:  cargador de procesos
# running time: tiempo que proceso antes de cargarse
# running duration: tiempo que toma para procesarse

def proceso(env, name, bcs, running_time,running_duration):
    global totalProce
    # Simulate los procesos que llegan
    yield env.timeout(running_time)

    # Pregunta si se puede procesar
    print('%s llega en el tiempo  %d' % (name, env.now))
    llegada = env.now #llega al procesador
    with bcs.request() as req:  #pedimos poder procesar
        yield req

        #
        print('%s comienza a procesarse a las  %s' % (name, env.now))
        yield env.timeout(running_duration)
        print('%s leaving the bcs at %s' % (name, env.now))
        # se hizo release automatico del proceso
    tiempoTotal = env.now - llegada
    totalProce = totalProce + tiempoTotal
    print('%s terminado a las  %s' % (name, tiempoTotal))
    
#crear ambiente de simulacion
env = simpy.Environment()
#El CPU atiene 1 proceso a la vez
bcs = simpy.Resource(env, capacity=1)

totalProce = 0.0

NProcesos = 25

RANDOM_SEED = 42  #para generar la misma serie de random
random.seed(RANDOM_SEED)
interval = 10 # la creacion de los procesos se distribuye exponencialmente en un intervalor de 10

# crear los carros
for i in range(NProcesos):
    t = random.expovariate(1.0 / interval)
    env.process(proceso(env, 'Proceso No. %d   ' % i, bcs, t, 5))

# correr la simulacion
env.run()

promProcesos = totalProce / NProcesos
print "el promedio fue: ", promProcesos
    
