import os
import sys
import json
import pandas as pd
from datetime import datetime
from smsdk import client
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor
import xml.dom.minidom
import xml.etree.ElementTree as ET
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to retrieve environment variables
def get_env_variable(name, default=""):
    val = os.environ.get(name, default)
    return val


# Function to read configuration from config.json
def read_config():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error("config.json file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error("config.json file is not a valid JSON.")
        sys.exit(1)

    required_keys = [
        "num_peak_users",
        "ramp_up_rate",
        "total_run_time",
        "min_wait_time",
        "max_wait_time",
    ]
    missing_keys = [key for key in required_keys if key not in config]

    if missing_keys:
        logger.error(f"Missing keys in config.json: {', '.join(missing_keys)}")
        sys.exit(1)

    return config


# Function to perform load testing
def simulate_load(cli, query, response_times, errors, min_wait_time, max_wait_time):
    start_time = time.time()
    try:
        df = cli.get_cycles(**query)
        response_times.append(time.time() - start_time)
        logger.info(f"Size of returned data: {df.shape}")
    except Exception as e:
        errors.append(e)
        logger.error(f"Error: {e}")

    # Introduce a random wait time
    wait_time = random.uniform(min_wait_time, max_wait_time)
    time.sleep(wait_time)


def dump_to_xml(metrics, xml_file):
    root = ET.Element("performance_metrics")
    for key, value in metrics.items():
        ET.SubElement(root, key).text = str(value)

    # Create ElementTree object with root element
    tree = ET.ElementTree(root)

    # Write ElementTree to XML file
    with open(xml_file, "wb") as f:
        tree.write(
            f, encoding="utf-8", xml_declaration=True, short_empty_elements=False
        )

    # Read the XML file to prettify
    with open(xml_file, "r", encoding="utf-8") as f:
        xml_content = f.read()

    # Prettify XML content
    dom = xml.dom.minidom.parseString(xml_content)
    prettified_xml = dom.toprettyxml(indent="\t")

    # Write prettified XML content back to the file
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(prettified_xml)


# Main function
def main(xml_file):
    # Get environment variables
    tenant = get_env_variable("ENV_VAR_TENANT")
    api_key = get_env_variable("ENV_VAR_API_KEY")
    api_secret = get_env_variable("ENV_VAR_API_SECRET")

    # Read configuration from config.json
    config = read_config()

    # Initialize SDK client
    cli = client.Client(tenant)
    cli.login("apikey", key_id=api_key, secret_id=api_secret)

    # Fetch machine information
    machine_type = cli.get_machine_type_names()[0]
    machines = cli.get_machine_names(source_type=machine_type)
    columns = cli.get_machine_schema(machines[0])["display"][:].to_list()

    # Define query parameters
    query = {
        "Machine": machines[0],
        "End Time__gte": datetime(2023, 4, 1),
        "End Time__lte": datetime(2023, 4, 2),
        "_order_by": "-End Time",
        "_limit": 100,
        "_only": columns,
    }

    # Number of concurrent requests to simulate
    response_times = []
    errors = []

    start_time = time.time()
    elapsed_time = 0

    # User ramp-up
    num_users = 0
    while elapsed_time < config["total_run_time"]:
        num_users += config["ramp_up_rate"]
        num_users = min(num_users, config["num_peak_users"])

        with ThreadPoolExecutor(max_workers=num_users) as executor:
            # Submit tasks to the executor
            futures = [
                executor.submit(
                    simulate_load,
                    cli,
                    query,
                    response_times,
                    errors,
                    config["min_wait_time"],
                    config["max_wait_time"],
                )
                for _ in range(num_users)
            ]

            # Wait for all tasks to complete
            for future in futures:
                future.result()

        elapsed_time = time.time() - start_time

    # Calculate performance metrics
    total_response = len(response_times)
    avg_response_time = (
        sum(response_times) / total_response if total_response > 0 else 1
    )
    min_response_time = min(response_times) if total_response > 0 else 0
    max_response_time = max(response_times) if total_response > 0 else 0
    throughput = total_response / elapsed_time if elapsed_time > 0 else 1
    error_rate = (len(errors) / (len(response_times) + len(errors))) * 100

    logger.info("Performance Metrics:")
    logger.info(f"Total Response: {total_response}")
    logger.info(f"Average Response Time: {avg_response_time} seconds")
    logger.info(f"Minimum Response Time: {min_response_time} seconds")
    logger.info(f"Maximum Response Time: {max_response_time} seconds")
    logger.info(f"Throughput: {throughput} requests per second")
    logger.info(f"Error Rate: {error_rate}%")

    # Store performance metrics in XML file
    metrics = {
        "total_response": total_response,
        "avg_response_time": avg_response_time,
        "min_response_time": min_response_time,
        "max_response_time": max_response_time,
        "throughput": throughput,
        "error_rate": error_rate,
    }

    if xml_file:
        dump_to_xml(metrics, xml_file)
        logger.info(f"Performance metrics dumped to {xml_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load testing script with optional performance metrics dump to XML"
    )
    parser.add_argument(
        "--perfxml",
        help="Path to the XML file to dump performance metrics",
        default=None,
    )
    args = parser.parse_args()
    main(args.perfxml)
