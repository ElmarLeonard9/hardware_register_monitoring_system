from datetime import datetime
from Validator import Validator
import json


class LogManager:
    """Manages system register logs, including creation, decoding, updates, and health analysis."""

    def __init__(self):
        self.logs = {}
        self.counter = 1

    @staticmethod
    def decode_bit(bit, data):
        """Decode a hex register value into bits and compare with schema definitions.

        Args:
            bit (str): Hexadecimal string value of the register.
            data (dict): Dictionary containing register field definitions 
                and bit mappings.

        Returns:
            tuple: A tuple containing two lists:
                - state (list[dict]): Extracted statuses for each field.
                - meaning (list[dict]): Semantic meanings for each field.
        """
        state = []
        meaning = []
        reg_value = int(bit, 16)
        base = data["bit_fields"]

        for i in range(len(base)):
            baseline = base[i]
            mask = (1 << baseline["bit_length"]) - 1
            extracted_bit = str(reg_value >> baseline["start_bit"] & mask)

            temp_state =  f"{baseline["value_meaning"][extracted_bit]["status"]}"
            temp_meaning = f"{baseline["value_meaning"][extracted_bit]["meaning"]}"

            state.append({"field_name": baseline["field_name"], "status": temp_state})
            meaning.append({"field_name": baseline["field_name"], "meaning": temp_meaning})
        return state, meaning

    def create(self, register, data: dict, bit):
        """Create a new log entry and insert it into the logs repository.

        Args:
            register (str): The machine name of the register.
            data (dict): Master dataset containing details of the register.
            bit (str): Hexadecimal string value of the register.
        """
        database = data[register]
        state, meaning = self.decode_bit(bit=bit, data=database)

        self.logs[str(self.counter)] = {"register": register, "inputted_hex": bit, "name": database["name"], "access_type": 
                               database["access_type"], "timestamp": str(datetime.now()),"information": meaning, "status": state }

        self.counter += 1
    
    def update(self, index: str , data: dict, register: str, bit: str = None):
        """Update an existing log entry inside the repository.

        Args:
            index (str): Unique log index key to be updated.
            data (dict): Master dataset containing details of the register.
            register (str): The machine name of the register.
            bit (str, optional): New hexadecimal string value. Revalidates existing 
                value if omitted. Defaults to None.
        """
        if bit is None:
            bit = Validator.bit(register, data, self.logs[index]["inputted_hex"])    
        database = data[register]
        state, meaning = self.decode_bit(bit=bit, data=database)

        self.logs[index] = {"register": register, "inputted_hex": bit, "name": database["name"], "access_type": 
                            database["access_type"], "timestamp": str(datetime.now()),"information": meaning, "status": state }
    
    def delete(self, index):
        """Remove a specific log entry using its index.

        Args:
            index (str): Unique log index key to be deleted.
        """
        self.logs.pop(index)
    
    def is_empty(self):
        """Check whether the logs repository contains any entries.

        Returns:
            bool: True if logs are empty, False otherwise.
        """
        return len(self.logs) == 0
    
    def calculate_health(self):
        """Analyze log records to calculate system health metrics and alerts.

        Returns:
            tuple: A tuple containing structural health summaries:
                - crit_count (int): Total number of critical status flags found.
                - crit_register (list[str]): Identity labels of critical registers.
                - warn_count (int): Total number of warning status flags found.
                - warn_register (list[str]): Identity labels of warned registers.
                - heal_count (int): Total number of healthy status flags found.
        """
        crit_count = 0
        crit_register = []
        warn_count = 0
        warn_register = []
        heal_count = 0

        for i in self.logs.keys():
            for j in range(len(self.logs[i]["status"])):
                checker = self.logs[i]["status"][j]["status"]
                reg_name = self.logs[i]["status"][j]["field_name"]
                if "Critical" in checker:
                    crit_count += 1
                    crit_register.append(f"{self.logs[i]["register"]}: {reg_name}")
                elif "Warning" in checker:
                    warn_count += 1
                    warn_register.append(f"{self.logs[i]["register"]}: {reg_name}")
                elif "Healthy" in checker:
                    heal_count += 1
        return crit_count, crit_register, warn_count, warn_register, heal_count
        
    def save(self, path):
        """Serialize and export all logs to a JSON file format.

        Args:
            path (str): System file destination target path.
        """
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.logs, file, indent=4, ensure_ascii=False)
    