
import multiprocessing  # Para procesos y semáforos
import random           # Para generar números aleatorios
import time             # Para pausas entre operaciones
import os               # Para operaciones con archivos


# ------------------------
# Archivos compartidos
# ------------------------
ARCHIVO_PENDIENTES = "pendientes.txt"      # Donde el productor escribe los números
ARCHIVO_RESULTADOS = "resultados.txt"      # Donde el consumidor escribe los resultados


# ------------------------
# Función para calcular el factorial
# ------------------------
def factorial(n):
    resultado = 1
    for i in range(1, n + 1):
        resultado *= i
    return resultado


# ------------------------
# Proceso PRODUCTOR
# ------------------------
# Genera números aleatorios y los escribe en ARCHIVO_PENDIENTES.
# Usa 'mutex' para exclusión mutua y 'datos' para avisar al consumidor.
def productor(mutex, datos, cantidad=5):
    for _ in range(cantidad):
        num = random.randint(1, 6)
        mutex.acquire()  # Entra a sección crítica (acceso exclusivo al archivo)
        with open(ARCHIVO_PENDIENTES, "a") as f:
            f.write(f"{num}\n")
        print(f"[Productor] Generado: {num}")
        mutex.release()  # Sale de sección crítica
        datos.release()  # Señala que hay un nuevo dato disponible
        time.sleep(1)


# ------------------------
# Proceso CONSUMIDOR
# ------------------------
# Lee números de ARCHIVO_PENDIENTES, calcula el factorial y escribe el resultado en ARCHIVO_RESULTADOS.
# Usa 'mutex' para exclusión mutua y 'datos' para esperar hasta que haya datos disponibles.
def consumidor(mutex, datos, cantidad=5):
    procesados = 0
    while procesados < cantidad:
        datos.acquire()      # Espera a que haya datos disponibles
        mutex.acquire()      # Entra a sección crítica (acceso exclusivo a los archivos)
        with open(ARCHIVO_PENDIENTES, "r") as f:
            lineas = f.readlines()
        if lineas:
            num = int(lineas[0].strip())
            fact = factorial(num)
            resultado = f"El factorial de: {num} es {fact}\n"
            with open(ARCHIVO_RESULTADOS, "a") as f:
                f.write(resultado)
            print(f"[Consumidor] {resultado.strip()}")
            # Eliminar la línea procesada del archivo de pendientes
            with open(ARCHIVO_PENDIENTES, "w") as f:
                f.writelines(lineas[1:])
            procesados += 1
        mutex.release()      # Sale de sección crítica
        time.sleep(0.5)


# ------------------------
# MAIN: Configuración y lanzamiento de procesos
# ------------------------
if __name__ == "__main__":
    # Limpiar archivos al inicio
    open(ARCHIVO_PENDIENTES, "w").close()
    open(ARCHIVO_RESULTADOS, "w").close()

    # Semáforos:
    # mutex: Exclusión mutua para acceso a archivos compartidos
    # datos: Cuenta cuántos datos pendientes hay para procesar
    mutex = multiprocessing.Semaphore(1)
    datos = multiprocessing.Semaphore(0)

    # Crear procesos
    p1 = multiprocessing.Process(target=productor, args=(mutex, datos))
    p2 = multiprocessing.Process(target=consumidor, args=(mutex, datos))

    # Iniciar procesos
    p1.start()
    p2.start()

    # Esperar a que terminen
    p1.join()
    p2.join()

    # Mostrar resultados finales
    with open(ARCHIVO_RESULTADOS) as f:
        print("\nContenido de resultados.txt:")
        print(f.read())