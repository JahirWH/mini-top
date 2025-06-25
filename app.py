import time
import psutil
from rich.console import Console
from rich.table import Table

console = Console()

def get_stats():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    return cpu, mem.percent, mem.used // (1024 ** 2), mem.total // (1024 ** 2)


def main():
    try:
        while True:
            cpu, mem_percent, mem_used, mem_total = get_stats()
            #table = Table(title=" Monitor" ,[numero de sistema], show_header=True, header_style="bold magenta")

            table = Table(title=" Monitor" , show_header=True, header_style="bold magenta")
            table.add_column("CPU (%)", justify="right")
            table.add_column("RAM (%)", justify="right")
            table.add_column("RAM Used (MB)", justify="right")
            table.add_column("RAM Total (MB)", justify="right")
            table.add_row(f"{cpu}", f"{mem_percent}", f"{mem_used}", f"{mem_total}")

            console.clear()
            console.print(table)
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold green]Adios![/bold green]")

if __name__ == "__main__":
    main()


#Testeo con psutil