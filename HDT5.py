import simpy
import random

#
# el carro se conduce un tiempo y tiene que llegar a cargarse de energia
# luego puede continuar conduciendo
# Debe hacer cola (FIFO) en el cargador

# name: identificacion del carro
# bcs:  cargador de bateria
# driving_time: tiempo que conduce antes de necesitar carga
# charge_duration: tiempo que toma cargar la bateria

def proceso(env, name, bcs, running_time,running_duration):
    global totalProce
    # Simulate driving to the BCS
    yield env.timeout(running_time)

    # Request one of its charging spots
    print('%s llega en el tiempo  %d' % (name, env.now))
    llegada = env.now #llega a la estacion de servicio
    with bcs.request() as req:  #pedimos conectarnos al cargador de bateria
        yield req

        # Charge the battery
        print('%s comienza a procesarse a las  %s' % (name, env.now))
        yield env.timeout(running_duration)
        print('%s leaving the bcs at %s' % (name, env.now))
        # se hizo release automatico del cargador bcs
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
interval = 10

# crear los carros
for i in range(NProcesos):
    t = random.expovariate(1.0 / interval)
    env.process(proceso(env, 'Proceso No.  %d' % i, bcs, t, 5))

# correr la simulacion
env.run()

promProcesos = totalProce / NProcesos
print "el promedio fue: ", promProcesos
    
