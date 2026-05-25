from rich.console import Console
from LogManager import LogManager
from Validator import Validator
from Display import Display
import json

with open("registers.json", "r") as file:
    register_db = json.load(file)
    
console = Console()
log_manager = LogManager()
search_map = {
    2: "register",
    3: "name",
    4: "access_type",
    5: "information",
    6: "state"
}

def show_main_menu():
    """Display the primary application menu and return a validated navigation choice.

    Returns:
        int: A validated menu selection option between 1 and 6.
    """
    console.print("[bold cyan]===== Hardware Register Monitoring System =====[/]")
    print("1. Create logs")
    print("2. Read Logs")
    print("3. Update Logs")
    print("4. Delete Logs")
    print("5. Summarize Logs")
    print("6. Exit")
    option = Validator.input(input("Insert the menu number you want to choose: "))
    while option not in [1, 2, 3, 4, 5, 6]:
        option = Validator.input(input("Insert the correct menu number: ")) 
    return option

def show_sub_menu_update():
    """Display the log modification options menu and return a validated selection.

    Returns:
        int: A validated modification path selection (1: Register, 2: Bit mask, 3: Exit).
    """
    console.print("\n[bold cyan]===== Update Log =====[/]")
    print("1. Update register")
    print("2. Update bit mask")
    print("3. Exit")
    option = Validator.input(input("Insert the menu number you want to choose: "))
    while option not in [1, 2, 3]:
        option = Validator.input(input("Insert the correct menu number: ")) 
    return option

def show_sub_menu_read():
    """Display log viewing filter options and return a validated filter configuration choice.

    Returns:
        int: A validated lookup strategy selection between 1 and 7.
    """
    console.print("\n[bold cyan]===== Read Log =====[/]")
    print("1. Read all Log")
    print("2. Search Specific Register")
    print("3. Search Specific Register Name")
    print("4. Search Specific Access Type")
    print("5. Search Specific Information")
    print("6. Search Specific state")
    print("7. Exit")
    option = Validator.input(input("Insert the menu number you want to choose: "))
    while option not in [1, 2, 3, 4, 5, 6, 7]:
        option = Validator.input(input("Insert the correct menu number: ")) 
    return option
            
def create_log_menu():
    """Handle interactive user workflow for defining, validating, and submitting a new register log."""

    console.print("\n[bold cyan]===== Creating Logs =====[/]")
    register = Validator.data(input("Insert the register: "), register_db)
    bit = Validator.hex32(input("Insert the hex value of the register: "))
    bit = Validator.bit(register, register_db, bit)
    choose = Validator.confirmation(console.input("do you want to submit the log([bold green]y[/]/[bold red]n[/]): ").lower())
    if choose == "y":
        log_manager.create(register, register_db, bit)
        console.print("[bold green]log successfully submitted[/]\n")
    else:
        console.print("[bold red]log is not submitted[/]\n")

def read_menu_log():
    """Execute the log retrieval pipeline based on chosen sub-menu filter criteria."""

    if log_manager.is_empty():
        console.print("[bold red]There is no data inside the log yet[/]\n")
    else:
        read = show_sub_menu_read()
        if read == 1:
            Display.log(log_manager.logs)
        elif read in search_map:
            search = input("insert the words you want to search: ")
            choose = Validator.confirmation(console.input("do you want to submit the log([bold green]y[/]/[bold red]n[/]): ").lower())
            if choose == "y":
                Display.search_log(search, search_map[read], log_manager.logs)
            else:
                console.print("[bold red]Search is canceled[/]\n")
        elif read == 7:
            console.print("[bold red]Reading log is canceled[/]\n") 

def update_menu_log():
    """Orchestrate interactive log value overrides for existing records inside the system repository."""

    if log_manager.is_empty():
        console.print("[bold red]There is no data inside the log yet[/]\n")
    else:
        update = show_sub_menu_update()
        if update == 1:
            Display.log(log_manager.logs)
            index = Validator.data(input("Insert the index you want to update: "), log_manager.logs)
            Display.log_index(index, log_manager.logs)
            choose = Validator.confirmation(console.input("do you want to edit this log([bold green]y[/]/[bold red]n[/]): ").lower())
            if choose == "y":
                register = Validator.data(input("Insert the updated register: "), register_db)
                log_manager.update(index=index, register=register, data=register_db)
                console.print("[bold green]Log successfully updated[/]\n")
            else:
                console.print("[bold red]Log is not updated[/]\n")
        elif update == 2:
            Display.log(log_manager.logs)
            index = Validator.data(input("Insert the index you want to update: "), log_manager.logs)
            Display.log_index(index, log_manager.logs)
            choose = Validator.confirmation(console.input("do you want to edit this log([bold green]y[/]/[bold red]n[/]): ").lower())
            if choose == "y":
                register = Validator.data(input("Insert the updated register: "), register_db)
                bit = Validator.hex32(input("Insert the hex value of the updated register: "))
                bit = Validator.bit(register, register_db, bit)
                log_manager.update(index=index, register=register, data=register_db, bit=bit)
                console.print("[bold green]Log successfully updated[/]\n")
            else:
                console.print("[bold red]Log is not updated[/]\n")

def delete_menu():
    """Present historical records to the user and manage target entry extraction processes safely."""

    if log_manager.is_empty():
        console.print("[bold red]There is no data inside the log yet[/]\n")
    else:
        console.print("\n[bold cyan]===== Delete Log =====[/]")
        Display.log(log_manager.logs)
        delete = Validator.data(input("Insert the index you want to delete: "), log_manager.logs)
        Display.log_index(delete, log_manager.logs)
        pick = Validator.confirmation(console.input("do you want to delete this log([bold green]y[/]/[bold red]n[/]): "))
        if pick == "y":
            log_manager.delete(delete)
            console.print("[bold green]Log has been deleted[/]\n")
        else:
            console.print("[bold red]the deletion process has been cancelled[/]\n")

def summarize_log():
    """Compile metrics from memory and render a clear telemetry safety report across active registers."""

    if log_manager.is_empty():
        console.print("[bold red]There is no data inside the log yet[/]\n")
    else:
        console.print("\n[bold cyan]===== Health Summary =====[/]")
        print(f"Total Logs : {len(log_manager.logs)}")
        crit_count, crit_register, warn_count, warn_register, heal_count = log_manager.calculate_health()
        console.print(f"\n[bold red]Critical[/]: {crit_count} ({", ".join(crit_register)})")
        console.print(f"[bold yellow]Warning[/]: {warn_count} ({", ".join(warn_register)})")
        console.print(f"[bold green]Healthy[/]: {heal_count}\n")

        if crit_count:
            console.print("Registers with [bold red]Critical[/] status should be investigated immediately.\n")
        if warn_count:
            console.print("Registers with [bold yellow]Warning[/] status should be investigated.\n")
        if not crit_count and not warn_count:
            console.print("All registers logged are working as intended.\n")

if __name__ == "__main__":
    while True:
        option = show_main_menu()
        if option == 1:
            create_log_menu()
        elif option == 2:
            read_menu_log()
        elif option == 3:
            update_menu_log()
        elif option == 4:
            delete_menu()
        elif option == 5:
            summarize_log()
        elif option == 6:
            if log_manager.is_empty():
                break
            else:
                choose = Validator.confirmation(console.input("do you want to save the logs made([bold green]y[/]/[bold red]n[/]): ").lower())
                if choose == "y":
                    log_manager.save("output.json")
                    break
                else:
                    break