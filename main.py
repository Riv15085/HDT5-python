import simpy
import random
import math
#se inicializan los debidos parametros que mas adelante se pueden cambiar
nrProcesos=10
semillaR= 12345
cantRamCPU= 100
cantCPU = 1
velocidad = 3
espera=1
wait=2
global tiempotot 
tiempotot = 0.0
vector = []
random.seed(semillaR) #se puede reproducir los mismos numeros al azar

def Procesando(env,self,cantRam, instrucciones, RAM, CPU, Waiting, espera,velocidad,t):
    #el proceso llega al sistema operativo
    global tiempotot
    yield env.timeout(t)
    tiempoStart=env.now
    print "%5.1f %s Empeiza (new)" %(tiempoStart,self)
    #hacemos un request de memoria ram, si no hay disponible debe esperar
    yield RAM.get(cantRam) 
    print "%5.1f %s Entra a memoria ram y esta listo para correr (ready)" % (env.now,self)
    Complet =0
    while Complet< instrucciones:

        with CPU.request() as req:
            yield req

            print "%5.1f %s Encuentra CPU" %(env.now,self)
            yield env.timeout(espera)
            #instruccion a realizarse
            if (instrucciones-Complet)>=velocidad:
                inst_exe=velocidad
            else:
                inst_exe=(instrucciones-Complet)

            print("%5.1f %s ejecutara %d instrucciones. (ready)" % (env.now,self, inst_exe))
            #tiempo de instrucciones a ejecutar
            yield env.timeout(inst_exe/velocidad)   

            #numero total de intrucciones terminadas
            Complet += inst_exe
            print("%5.1f %s (%d/%d) completado. (running)" % ( env.now,self, Complet, instrucciones))

            #CPU.release()
        num = random.randint(1,2)
        if Complet < instrucciones and num ==1:
            with Waiting.request() as req:
                    yield req
                    "%5.1f %s Operaciones de entrada y salida" %(env.now,self)
    yield RAM.put(cantRam)
    tiempofinish1 = env.now - tiempoStart
    vector.append(tiempofinish1)
    tiempotot = tiempotot + tiempofinish1

#se inicializa lo que sera la simulacion parametrizada
env = simpy.Environment()
Waiting = simpy.Resource(env,capacity=wait)
RAM= simpy.Container(env, init=cantRamCPU , capacity=cantRamCPU)
CPU = simpy.Resource(env, capacity=cantCPU)


for i in range (nrProcesos):
    instrucciones = random.randint(1,10)
    cantRam = random.randint(1,10)
    t = random.expovariate(1.0 / 10)
    Final = Procesando(env, "Proceso %d" % i, cantRam, instrucciones, RAM, CPU, Waiting, espera, velocidad,t)
    env.process(Final)
    
    #yield env.timeout(t)

env.run()

# Calcular promedio
total = tiempotot
print ("Tiempo total: %f" % total)
promedio = (tiempotot / nrProcesos)
print ("El promedio de tiempo de proceso es: %f " % promedio)

# Calcular desviacion estandar
tmp = 0

for i in vector:
        tmp += (i-promedio)**2

desv_Estandar = (tmp/(nrProcesos-1))**0.5

print "La desviacion estandar es: ", desv_Estandar

