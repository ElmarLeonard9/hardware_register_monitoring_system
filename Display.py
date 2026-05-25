from rich.console import Console
from rich.table import Table

console = Console()

class Display:
    """Provides formatting and rich console rendering utilities for register telemetry logs."""

    @staticmethod
    def apply_status_color(field_name, status):
        """Format a field name and status pair with standard severity color codes.

        Args:
            field_name (str): The name identifier of the bitfield.
            status (str): The health state string (e.g., 'Healthy', 'Warning', 'Critical').

        Returns:
            str: A Rich markup-formatted string containing the colored status.
        """
        if status == "Healthy":
            return f"{field_name}: [bold green]{status}[/]"
        elif status == "Warning":
            return f"{field_name}: [bold yellow]{status}[/]"
        elif status == "Critical":
            return f"{field_name}: [bold red]{status}[/]"

    @staticmethod
    def apply_meaning_color(field_name, meaning):
        """Format a field name and semantic meaning pair with a unified accent color.

        Args:
            field_name (str): The name identifier of the bitfield.
            meaning (str): The literal interpretation or description of the bit value.

        Returns:
            str: A Rich markup-formatted string containing the colored meaning.
        """
        return f"{field_name}: [bold cyan]{meaning}[/]"

    @staticmethod
    def build_log_table(title: str):
        """Initialize a pre-configured Rich Table instance with standardized schema headers.

        Args:
            title (str): The text header caption to display above the grid.

        Returns:
            Table: An empty Rich Table UI component configured with telemetry columns.
        """
        table = Table(title=title, title_style="bold cyan", show_lines=True)
        for col in ["No", "Register", "Inputted Hex", "Name", "Access Type", "Timestamp", "Information", "State"]:
            table.add_column(col)
        return table

    @classmethod
    def format_log_row(cls, index: str, log: dict):
        """Process and serialize a raw log dictionary record into printable text cells.

        Args:
            index (str): The log sequence or lookup key identifier.
            log (dict): The target dictionary log containing metadata, states, and meanings.

        Returns:
            tuple: A sequence of structured string parameters matching table columns:
                (index, register, inputted_hex, name, access_type, timestamp, info, state)
        """
        log_info = ", ".join(cls.apply_meaning_color(info["field_name"], info["meaning"]) for info in log["information"])
        log_stat = ", ".join(cls.apply_status_color(stat["field_name"], stat["status"]) for stat in log["status"])
        return (index, log["register"], log["inputted_hex"], log["name"], log["access_type"], log["timestamp"], log_info, log_stat)

    @classmethod
    def log(cls, data: dict):
        """Render all historical telemetry log records within a structured UI terminal table.

        Args:
            data (dict): The log database dictionary object storing sequential entries.
        """
        table = cls.build_log_table("Telemetry Logs")
        for i in data.keys():
            log = data[i]
            index, reg, i_hex, name, acc_type, time, info, state = cls.format_log_row(i, log)
            table.add_row(index, reg, i_hex, name, acc_type, time, info, state)
    
        console.print(table)

    @classmethod
    def log_index(cls, index, data: dict):
        """Isolate and print a single specific log entry to the console terminal.

        Args:
            index (str): The unique target dictionary key representing the log sequence.
            data (dict): The log database dictionary object holding target records.
        """
        index_table = cls.build_log_table("Called Logs")

        log = data[index]
        i, reg, i_hex, name, acc_type, time, info, state = cls.format_log_row(index, log)
        index_table.add_row(i, reg, i_hex, name, acc_type, time, info, state)
        console.print(index_table)

    @classmethod
    def search_log(cls, search, search_by, data: dict):
        """Filter log rows based on a substring match rule and output matching results.

        Args:
            search (str): The substring text query sequence to match against.
            search_by (str): The log dict key category targeting the search boundary 
                (e.g., 'register', 'name', 'access_type', 'information', 'state').
            data (dict): The log database dictionary object containing valid logs.
        """
        search = search.lower()
        search_table = cls.build_log_table("Searched Logs")

        for i in data.keys():
            log = data[i]

            index, reg, i_hex, name, acc_type, time, info, state = cls.format_log_row(i, log)

            if search_by == "register":
                check = reg
            elif search_by == "name":
                check = name
            elif search_by == "access_type":
                check = acc_type
            elif search_by == "information":
                check = info
            elif search_by == "state":
                check = state

            if search in check.lower():
                search_table.add_row(index, reg, i_hex, name, acc_type, time, info, state)
    
        console.print(search_table)  