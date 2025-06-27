#!/usr/bin/env python3

import time
import os


ROJO = '\033[1;31m'
AMARILLO = '\033[1;33m'
VERDE = '\033[1;32m'
AZUL = '\033[1;36m'
NORMAL = '\033[0m'

# Esta función mira cuánto trabaja la cpu lee el archivo desde el kernel
def uso_cerebro(intervalo=0.5):
    def leer_linea_cpu():
        with open('/proc/stat', 'r') as archivo:
            for linea in archivo:
                if linea.startswith('cpu '):
                    partes = linea.split()
                    numeros = [int(x) for x in partes[1:]]
                    return numeros
    primero = leer_linea_cpu()
    time.sleep(intervalo)
    segundo = leer_linea_cpu()
    quieto1, total1 = primero[3], sum(primero)
    quieto2, total2 = segundo[3], sum(segundo)
    diferencia_quieto = quieto2 - quieto1
    diferencia_total = total2 - total1
    if diferencia_total == 0:
        return 0
    porcentaje = 100 * (1 - diferencia_quieto / diferencia_total)
    return round(porcentaje, 1)

# funcion memoria
def uso_memoria():
    datos = {}
    with open('/proc/meminfo', 'r') as archivo:
        for linea in archivo:
            if linea.startswith('MemTotal:') or linea.startswith('MemAvailable:'):
                nombre, valor, _ = linea.split()
                datos[nombre] = int(valor)
    total = datos['MemTotal:']
    libre = datos['MemAvailable:']
    usada = total - libre
    porcentaje = 100 * usada / total
    return round(porcentaje, 1), usada // 1024, total // 1024

#  swap
def uso_swap():
    total = libre = 0
    with open('/proc/meminfo', 'r') as archivo:
        for linea in archivo:
            if linea.startswith('SwapTotal:'):
                total = int(linea.split()[1])
            elif linea.startswith('SwapFree:'):
                libre = int(linea.split()[1])
    usada = total - libre
    porcentaje = 100 * usada / total if total else 0
    return round(porcentaje, 1), usada // 1024, total // 1024

# Proramas corriendo
# def contar_programas():
#     return len([d for d in os.listdir('/proc') if d.isdigit()])

def barra(porcentaje, largo=25):
    full = int(porcentaje / 100 * largo)
    return '[' + "#" * full + ' ' * (largo - full ) + ']'

# Funcion del tiempo encendida
def tiempo_encendida():
    with open('/proc/uptime', 'r') as archivo:
        segundos = float(archivo.readline().split()[0])
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    return f"{horas} horas y {minutos} minutos"

# Esta función pone color 
def poner_color(valor, mucho=80, alto=90):
    if valor >= alto:
        return f"{ROJO}{valor}{NORMAL}"
    elif valor >= mucho:
        return f"{AMARILLO}{valor}{NORMAL}"
    else:
        return f"{VERDE}{valor}{NORMAL}"

# main
if __name__ == "__main__":
    try:
        while True:
            cpu = uso_cerebro()
            memoria, usada, total = uso_memoria()
            swap, swap_usada, swap_total = uso_swap()
            # programas = contar_programas()
            tiempo = tiempo_encendida()

            print('\033c', end='')  
            print("=" * 45)
            print(f"                  {AZUL}Mini-top {NORMAL}")
            print("=" * 45)
            print(f"(CPU):{barra(cpu)}  {poner_color(cpu):>8}%")
            print(f"(RAM):{barra(memoria)}  {poner_color(memoria):>8}%  ")
            print(f"(Swap):{poner_color(swap):>8}%  ")
            # print(f"Programas :  {programas:>8}")
            print(f"Tiempo encendida: {tiempo}")
            print("=" * 45)
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{VERDE}exit!{NORMAL}")