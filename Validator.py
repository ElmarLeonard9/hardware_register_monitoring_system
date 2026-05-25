from rich.console import Console
import string

console = Console()

class Validator:
    """Provides validation utility operations for user console inputs, databases, and register configurations."""

    @staticmethod
    def input(entry):
        """Validate and force a console input string to be a positive integer.

        Args:
            entry (str): The initial user input string to evaluate.

        Returns:
            int: The safely converted integer value.
        """
        while not entry.isdigit():
            console.print("[bold red]YOU INPUTTED WITH THE WRONG FORMAT!![/]")
            entry = input("please insert with the right format: ")
        entry = int(entry)
        return entry

    @staticmethod
    def data(register, database: dict):
        """Validate whether a register name exists within a target database configuration mapping.

        Args:
            register (str): The name identifier of the register to verify.
            database (dict): The target dictionary structure containing register schema definitions.

        Returns:
            str: A validated register key that is guaranteed to exist in the database keys.
        """
        while register not in database.keys():
            console.print("[bold red]THE INFORMATION YOU INPUTTED IS NOT IN THE DATABASE[/]")
            register = input("Insert the correct information: ")    
        return register

    @staticmethod
    def confirmation(confirm):
        """Validate and enforce a binary choice confirmation response from the user.

        Args:
            confirm (str): Initial raw prompt response string from the console.

        Returns:
            str: A validated lower-case response character ('y' or 'n').
        """
        while confirm != "y" and confirm != "n":
            confirm = console.input("please submit with the correct format([bold green]y[/]/[bold red]n[/]): ").lower()
        return confirm

    @staticmethod
    def hex32(value):
        """Validate and sanitize a string entry to guarantee a compliant 32-bit hexadecimal format.

        Args:
            value (str): The text-based string containing a potential hexadecimal identifier.

        Returns:
            str: A valid 8-character long hexadecimal identifier string minus any standard '0x' prefixes.
        """
        while True:
            inputted = value.removeprefix("0x").removeprefix("0X")
            if not inputted:
                value = console.input("[bold red]Hex information cannot be empty[/], insert hex value: ")
                continue
            if not all(c in string.hexdigits for c in inputted):
                value = console.input("[bold red]Invalid hex value[/], insert hex value: ")
                continue
            if len(inputted) != 8:
                value = console.input(f"[bold red]Value is not 32-bit[/] (8 hex chars max): ")
                continue
            return value
    
    @classmethod
    def bit(cls, register, data: dict, bit):
        """Validate whether a given hex string breaks down into recognizable schema definitions without faults.

        Args:
            register (str): Identity name of the register mapping definition.
            data (dict): Reference dataset dictionary holding system schemas.
            bit (str): Hexadecimal string candidate to slice up and check.

        Returns:
            str: A completely verified hexadecimal string that fits the layout limits.
        """
        while True:
            reg_value = int(bit, 16)
            database = data[register]
            base = database["bit_fields"]
            valid = True

            for i in range(len(base)):
                baseline = base[i]
                mask = (1 << baseline["bit_length"]) - 1
                extracted_bit = str(reg_value >> baseline["start_bit"] & mask)

                if extracted_bit not in baseline["value_meaning"]:
                    console.print(f"[bold red]Error: Bitfield '{baseline['field_name']}' results in value '{extracted_bit}', which is undefined![/]")
                    valid = False
                    break
        
            if valid:
                return bit
        
            bit = cls.hex32(input("Please input the correct hex value: "))