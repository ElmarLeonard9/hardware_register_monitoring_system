## Hardware Register Monitoring System Application Based on Python

A comprehensive Python application for managing inventory data with Create, Read, Update, and Delete (CRUD) operations.

## Business Understanding

This application is designed for hardware validation engineers in the semiconductor industry who face critical risk of device failure due to manual errors when monitoring complex, raw hexadecimal hardware data. The Hardware Register Monitoring System addresses this by providing a Python-based CRUD interface that automatically validates telemetry against a pre-defined JSON reference map. This solution ensures real-time health alerts (Healthy/Critical) for efficient debugging. Limitations: the application operates strictly through a command-line terminal and data is stored within the program’s internal memory using nested dictionary.


**Benefits:**

* Automated Treshold Checker: Compares user input against reference automatically to lessen ineffieciency of searching of specific state in documentation that could have thousands of pages.
* Visual Status Indicators: Inform component status whether its healthy, warning or Critical.
* Human-Language Translator: Convert hex addresess into readable component names.


**Target Users:**

This application is designed for Hardware Validation Engineers, Embedded Firmware Developers and Quality Assurance Team.

## Features

* **Create:**
    * Add new log entries to the system, specifying details like product name, description, SKU (Stock Keeping Unit), quantity on hand, reorder point, and category.
    * Implement validation rules to ensure data accuracy.
* **Read:**
    * Search and retrieve specific product information by register, name, access type, information or state.
    * Display comprehensive log details in a user-friendly format.
* **Update:**
    * Modify existing log information to reflect changes in register or hex.
    * Provide clear confirmation or error messages for update success or failure.
* **Delete:**
    * Allow for the removal of unused log or mistake log.
* **Summarize:**
    * Generate summarize report on the condition of every register logged.
* **Export:**
    * Export reports in JSON formats for further analysis.

## Installation

1. **Prerequisites:**
    * Python version 3.7 or later
    * Additional dependencies:
        * `pip install rich`

2. **Installation:**
    ```bash
    git clone [https://github.com/](https://github.com/)ElmarLeonard9/hardware_register_monitoring_system
    cd python-inventory-crud
    pip install -r requirements.txt
    ```

3. **Database Setup:**
    * Create a JSON file with the information of the register

## Usage

1. **Run the application:**
    ```bash
    python monitor_system.py
    ```

2. **CRUD Operations:**
    * **Create:** Add a new log to the telemetry logs's table, providing necessary details like register and hex value (e.g register: "0x0004" or "0x0000, hex value: "0x00000001" or "0x00000010").
    * **Read:** Search for a specific log by register, name, access type, information or state.
    * **Update:** Modify the register or hex of a log.
    * **Delete:** Remove an unused log or a mistake log.
    * **Summarize:** Generate reports on condition of the .

## Data Model

This project utilizes a JSON to store register information. The following is an example of the data in the JSON:

```Python
{
    "0x0000": {
    "name": "GPU_STATUS",
    "description": "Top-level GPU execution and pipeline status register",
    "access_type": "RO",
    "current_value": "0x00000005",
    "bit_fields": [
      {
        "field_name": "PIPELINE_ACTIVE",
        "start_bit": 0,
        "bit_length": 1,
        "value_meaning": {
          "0": { "meaning": "Pipeline idle", "status": "Healthy" },
          "1": { "meaning": "Pipeline executing commands", "status": "Healthy" }
        }
      },
      {
        "field_name": "CONTEXT_SWITCH",
        "start_bit": 1,
        "bit_length": 1,
        "value_meaning": {
          "0": { "meaning": "No context switch in progress", "status": "Healthy" },
          "1": { "meaning": "Context switch in progress", "status": "Warning" }
        }
      },
      {
        "field_name": "SHADER_STALL",
        "start_bit": 2,
        "bit_length": 1,
        "value_meaning": {
          "0": { "meaning": "Shader units running normally", "status": "Healthy" },
          "1": { "meaning": "Shader stall detected (dependency or resource conflict)", "status": "Warning" }
        }
      },
      {
        "field_name": "MEMORY_BUSY",
        "start_bit": 3,
        "bit_length": 1,
        "value_meaning": {
          "0": { "meaning": "Memory subsystem idle", "status": "Healthy" },
          "1": { "meaning": "Memory subsystem busy", "status": "Healthy" }
        }
      },
      {
        "field_name": "DISPLAY_ACTIVE",
        "start_bit": 4,
        "bit_length": 1,
        "value_meaning": {
          "0": { "meaning": "Display output disabled", "status": "Healthy" },
          "1": { "meaning": "Display engine actively driving output", "status": "Healthy" }
        }
      },
      {
        "field_name": "RESERVED",
        "start_bit": 5,
        "bit_length": 27,
        "value_meaning": {
          "0": { "meaning": "Reserved, must be zero", "status": "Healthy" }
        }
      }
    ]
  }
}
```