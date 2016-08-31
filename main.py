import simpy
import random

def proceso(env,nrProcesos,RAM, CPU, Waiting, espera, tiempotot):
    for i in range (nrProcesos):
        instrucciones = random.randint(1,10)
        cantRam = random.randint(1,10)
        Final = Procesando(env, "Proceso%d" % i, cantRam, instrucciones, RAM, CPU, Waiting, espera, tiempotot)
        env.process(Final)
        t = random.expovariate(1.0 / 1)
        yield env.timeout(t)

def Procesando(env,self,cantRam, instrucciones, RAM, CPU, Waiting, espera, tiempotot):
    #el proceso llega al sistema operativo
    tiempoStart=env.now
    print "%5.1f %s Empeiza (new)" %(tiempoStart,self)
    #hacemos un request de memoria ram, si no hay disponible debe esperar
    with RAM.get(cantRam) as req:
        yield req
        print "%5.1f %s Entra a memoria ram y esta listo para correr (ready)" % (env.now,self)
        while instrucciones> 0:
            yield CPU.request()
            print "%5.1f %s Encuentra CPU" %(env.now,self)
            yield env.timeout(espera)
            cont = velocidad
            while (cont >0):
                if (instrucciones != 0):
                    instrucciones = instrucciones -1
                    cont = cont -1
                else:
                    cont = 0
            CPU.release()
            if (instrucciones <= 0):
                "%5.1f %s Se ha terminado el proceso (terminated)" %(env.now,self)
                tiempofinish1 = env.now- tiempoStart
                vector.append(tiempofinish1)
                tiempotot = tiempotot + tiempofinish1
            else:
                num = random.randint(1,2)
                if num == 1:
                    with Waiting.request() as req:
                        yield req

#se inicializan los debidos parametros que mas adelante se pueden cambiar
nrProcesos=25
semillaR= 12345
cantRamCPU= 100
cantCPU = 1
velocidad = 3
espera=1
wait=2
tiempotot = 0.0
vector = []
random.seed(semillaR) #se puede reproducir los mismos numeros al azar

#se inicializa lo que sera la simulacion parametrizada
env = simpy.Environment()
Waiting = simpy.Resource(env,capacity=wait)
RAM= simpy.Container(env, init=cantRamCPU , capacity=cantRamCPU)
CPU = simpy.Resource(env, capacity=cantCPU)
env.process(proceso(env,nrProcesos,RAM, CPU, Waiting, espera, tiempotot))
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

