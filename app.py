import time
import os

# Colores ANSI
RED = '\033[1;31m'
YELLOW = '\033[1;33m'
GREEN = '\033[1;32m'
CYAN = '\033[1;36m'
RESET = '\033[0m'

def get_cpu_usage():
    #lee los valores de la carpeta proc/stat
    def read_cpu_line():
        with open('/proc/stat', 'r') as f:
            for line in f:
                if line.startswith('cpu '):
                    parts = line.split()
                    values = [int(x) for x in parts[1:]]
                    return values
    v1 = read_cpu_line()
    time.sleep(0.5)
    v2 = read_cpu_line()
    idle1, total1 = v1[3], sum(v1)
    idle2, total2 = v2[3], sum(v2)
    idle_delta = idle2 - idle1
    total_delta = total2 - total1
    cpu_percent = 100 * (1 - idle_delta / total_delta) if total_delta else 0
    return round(cpu_percent, 1)

#misma carpeta, otros datos
def get_mem_usage():
    meminfo = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('MemTotal:') or line.startswith('MemAvailable:'):
                key, value, _ = line.split()
                meminfo[key] = int(value)
    mem_total = meminfo['MemTotal:']
    mem_available = meminfo['MemAvailable:']
    mem_used = mem_total - mem_available
    mem_percent = 100 * mem_used / mem_total
    return round(mem_percent, 1), mem_used // 1024, mem_total // 1024

def get_swap_usage():
    swap_total = swap_free = 0
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if line.startswith('SwapTotal:'):
                swap_total = int(line.split()[1])
            elif line.startswith('SwapFree:'):
                swap_free = int(line.split()[1])
    swap_used = swap_total - swap_free
    swap_percent = 100 * swap_used / swap_total if swap_total else 0
    return round(swap_percent, 1), swap_used // 1024, swap_total // 1024

def get_process_count():
    return len([d for d in os.listdir('/proc') if d.isdigit()])

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        seconds = float(f.readline().split()[0])
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}h {minutes}m"

def colorize(value, warn=80, crit=90):
    if value >= crit:
        return f"{RED}{value}{RESET}"
    elif value >= warn:
        return f"{YELLOW}{value}{RESET}"
    else:
        return f"{GREEN}{value}{RESET}"

def main():
    try:
        while True:
            cpu = get_cpu_usage()
            mem_percent, mem_used, mem_total = get_mem_usage()
            swap_percent, swap_used, swap_total = get_swap_usage()
            proc_count = get_process_count()
            uptime = get_uptime()

            print('\033c', end='')#borrador
            print("=" * 42)
            print(f"      {CYAN}Mini-top {RESET}")
            print("=" * 42)
            print(f"CPU:   {colorize(cpu):>8}%")
            print(f"RAM:   {colorize(mem_percent):>8}%  ({mem_used:>5} MB / {mem_total:>5} MB)")
            print(f"Swap:  {colorize(swap_percent):>8}%  ({swap_used:>5} MB / {swap_total:>5} MB)")
            print(f"Proc:  {proc_count:>8}")
            print(f"Uptime:{uptime:>8}")
            print("=" * 42)
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{GREEN}adios!{RESET}")

if __name__ == "__main__":
    main()