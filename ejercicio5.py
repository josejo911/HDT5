# Universidad del Valle de Guatemala
# Algoritmos y Estructura de datos
#Jennifer Barillas 15307
#Javier Jo 14343


import simpy
import random

#cant_inst: cantidad de instrucciones
#time_process: tiempo de proceso

def proceso(env, time_process, nombre, ram, memory, cant_inst, velocidad):
    global tiempoTotal
   #New
    yield env.timeout(time_process)
    print('tiempo: %f : %s NEW cantidad %d de memoria ram' % (env.now, nombre, memory))
    time_now = env.now 
    
    #memoria
    yield ram.get(memory)
    print('tiempo: %f : %s acepta la solicitud por %d de memoria ram' % (env.now, nombre, memory))

    #Revisar si las intrucciones estan completas
    check = 0
    
    while check < cant_inst:
        #pasa a ready
        with cpu.request() as req:
            yield req
            #instruccionss a realizar
            if (cant_inst-check)>=velocidad:
                realizar=velocidad
            else:
                realizar=(cant_inst-check)
            #tiempo de instrucciones a ejecutar
            print('tiempo: %f : %s READY el cpu ejecutara %d instrucciones' % (env.now, nombre, realizar))
            yield env.timeout(realizar/velocidad)

            #instrucciones completas
            check += realizar
            print('tiempo: %f : %s RUNNING (%d/%d) listo!' % (env.now, nombre, check, cant_inst))

        #CONDICION: Decide si espera o pasa a ready
        verificar = random.randint(1,2)
        if verificar == 1 and check<cant_inst:
         
            with waiting.request() as req2:
                yield req2
                #tiempo de operaciones
                yield env.timeout(1)                
                print('tiempo: %f : %s WAITING operaciones (in/out)' % (env.now, nombre))
    
    yield ram.put(memory)
    print('tiempo: %f : %s TERMINATED, %d de memoria ram' % (env.now, nombre, memory))
    #tiempo de todos los procesos
    tiempoTotal += (env.now -time_now) 
    tiempos.append(env.now - time_now)

    
#instrucciones por tiempo
velocidad = 3.0
memoriaRam= 100
#programas totales
cantProgra= 25
#tiempos de cada uno
tiempos= []
tiempoTotal= 0.0    

env = simpy.Environment()
cpu = simpy.Resource (env, capacity=2)
ram = simpy.Container(env, init=memoriaRam, capacity=memoriaRam)
waiting = simpy.Resource (env, capacity=2)

#random (semilla)
random.seed(1904)
#intervalo
rank = 1 

# PROCESO
for inicial in range(cantProgra):
    time_process = random.expovariate(1.0 / rank)
    #cantidad de instrucciones
    cant_inst = random.randint(1,10)
    #memoria a usar
    memory = random.randint(1,10) 
    env.process(proceso(env, time_process, 'No. Programa %d' % inicial, ram, memory, cant_inst, velocidad))

env.run()

#promedio
promedio=(tiempoTotal/cantProgra)
print('Tiempo promedio: %f' % (promedio))


#Desviacion estandar
suma=0
for xinicial in tiempos:
    suma+=(xinicial-promedio)**2
desv=(suma/(cantProgra-1))**0.5
print('Desviacion estandar: %f' %(desv))
