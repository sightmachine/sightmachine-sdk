# Internal User Document: Load Test Performance Analysis Script

## Introduction
The `load_test_performance_analysis.py` script is designed to conduct load testing on SM-SDK APIs. Currently, it tests three APIs: `get_cycles`, `get_line_data`, and `get_kpi_data_viz` to analyze their performance metrics. This document provides a quick guide on how to use the script.

## Prerequisites
Before using the script, ensure the following prerequisites are met:

- Python 3.8.18 and above installed on your system.
- Necessary Python packages installed. You can install the required packages using pip:
  ```
  pip install pandas smsdk
  ```

## Usage

### 1. Configuration
Ensure that the `config.json` file is present in the same directory as the script. This file should contain the following configuration parameters:
- `num_peak_users`: Number of peak users to simulate load.
- `ramp_up_rate`: Rate at which users are ramped up.
- `total_run_time`: Total duration for which the load test should run.
- `min_wait_time`: Minimum wait time between API requests.
- `max_wait_time`: Maximum wait time between API requests.

### 2. Command Line Arguments
The script accepts one optional command-line argument:
- `--perfxml`: Path to the XML file where performance metrics will be dumped. If not provided, metrics will not be saved to any file.

### 3. Environment Variables
Ensure the following environment variables are set:
- `ENV_VAR_TENANT`: Your SMSDK tenant ID.
- `ENV_VAR_API_KEY`: Your API key.
- `ENV_VAR_API_SECRET`: Your API secret.

### 4. Running the Script
To run the script, execute the following command in your terminal:
```
python load_test_performance_analysis.py --perfxml <path_to_xml_file>
```
Replace `<path_to_xml_file>` with the desired path where you want to save the performance metrics XML file. If you don't want to save the metrics, you can omit the `--perfxml` argument.

### 5. Output
Once the script execution completes, it will display the performance metrics on the console. If the `--perfxml` argument is provided, the metrics will also be saved to the specified XML file.

## Conclusion
This document provides a quick guide on how to use the `load_test_performance_analysis.py` script for conducting load testing and analyzing performance metrics of SMSDK APIs. It is easy to extend to support other APIs in the future based on the requirement.