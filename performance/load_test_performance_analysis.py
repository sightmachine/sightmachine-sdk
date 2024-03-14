import os
import sys
import json
import pandas as pd
from datetime import datetime
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor
import xml.dom.minidom
import xml.etree.ElementTree as ET
import argparse
import typing as t_

from smsdk.client import Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to read configuration from config.json
def read_config() -> t_.Dict[str, t_.Any]:
    config = {}
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


def dump_to_xml(
    metrics_dict: t_.Dict[str, t_.Dict[str, t_.Any]], xml_file: str
) -> None:
    root = ET.Element("performance_metrics")
    for api_name, api_metrics in metrics_dict.items():
        api_element = ET.SubElement(root, api_name)
        for key, value in api_metrics.items():
            sub_element = ET.SubElement(api_element, key)
            sub_element.text = str(value)

    # Generate prettified XML content
    xml_content = ET.tostring(root, encoding="unicode", method="xml")
    prettified_xml = xml.dom.minidom.parseString(xml_content).toprettyxml(indent="\t")

    # Write prettified XML content to the file
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(prettified_xml)


def load_testing_decorator(func: t_.Callable[..., t_.Any]) -> t_.Callable[..., t_.Any]:
    def wrapper(
        cli: t_.Any,
        response_times: t_.List[float],
        errors: t_.List[Exception],
        min_wait_time: float,
        max_wait_time: float,
        **query: t_.Any,
    ) -> None:
        start_time = time.time()
        try:
            df = func(cli, **query)
            response_times.append(time.time() - start_time)
        except Exception as e:
            errors.append(e)
            logger.error(f"Error: {e}")

        # Introduce a random wait time
        wait_time = random.uniform(min_wait_time, max_wait_time)
        time.sleep(wait_time)
        print(".", end="", flush=True)

    return wrapper


# Function to perform load testing on 'get_cycles'
@load_testing_decorator
def get_cycles(cli: t_.Any, **query: t_.Any) -> t_.Any:
    return cli.get_cycles(**query)


# Function to perform load testing on 'get_line_data'
@load_testing_decorator
def get_line_data(cli: t_.Any, **query: t_.Any) -> t_.Any:
    return cli.get_line_data(**query)


# Function to perform load testing on 'get_kpi_data_viz'
@load_testing_decorator
def get_kpi_data_viz(cli: t_.Any, **query: t_.Any) -> t_.Any:
    return cli.get_kpi_data_viz(**query)


def perform_test(
    func: t_.Callable[..., t_.Any],
    config: t_.Dict[str, t_.Any],
    cli: Client,
    **payload: t_.Any,
) -> t_.Dict[str, t_.Union[int, float]]:
    # Number of concurrent requests to simulate load
    response_times: t_.List[float] = []
    errors: t_.List[Exception] = []

    start_time = time.time()
    elapsed_time = 0.0

    # User ramp-up
    num_users = 0
    while elapsed_time < config["total_run_time"]:
        num_users += config["ramp_up_rate"]
        num_users = min(num_users, config["num_peak_users"])

        with ThreadPoolExecutor(max_workers=num_users) as executor:
            # Submit tasks to the executor
            futures = [
                executor.submit(
                    func,
                    cli,
                    response_times,
                    errors,
                    config["min_wait_time"],
                    config["max_wait_time"],
                    **payload,
                )
                for _ in range(num_users)
            ]

            # Wait for all tasks to complete
            for future in futures:
                future.result()

        elapsed_time = time.time() - start_time

    print()
    # Calculate performance metrics
    total_response = len(response_times)
    avg_response_time = (
        sum(response_times) / total_response if total_response > 0 else 0
    )
    min_response_time = min(response_times) if total_response > 0 else 0
    max_response_time = max(response_times) if total_response > 0 else 0
    throughput = total_response / elapsed_time if elapsed_time > 0 else 0
    error_rate = (len(errors) / (len(response_times) + len(errors))) * 100

    logger.info("Performance Metrics:")
    logger.info(f"Number of Response: {total_response}")
    logger.info(f"Average Response Time: {avg_response_time} seconds")
    logger.info(f"Minimum Response Time: {min_response_time} seconds")
    logger.info(f"Maximum Response Time: {max_response_time} seconds")
    logger.info(f"Throughput: {throughput} requests per second")
    logger.info(f"Error Rate: {error_rate}%")

    # Store performance metrics in XML file
    return {
        "num_response": total_response,
        "avg_response_time": avg_response_time,
        "min_response_time": min_response_time,
        "max_response_time": max_response_time,
        "throughput": throughput,
        "error_rate": error_rate,
    }


def perform_get_cycles_load_test(
    config: t_.Dict[str, t_.Any], cli: Client
) -> t_.Dict[str, t_.Any]:
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

    return perform_test(get_cycles, config, cli, **query)


def perform_get_line_data_load_test(
    config: t_.Dict[str, t_.Any], cli: Client
) -> t_.Dict[str, t_.Any]:
    START_DATETIME = "2023-04-01T08:00:00.000Z"
    END_DATETIME = "2023-04-02T23:00:00.000Z"
    TIME_ZONE = "America/Los_Angeles"
    MACHINE4 = "JB_NG_PickAndPlace_1_Stage4"
    FIELD_NAME1 = "stats__BLOCKED__val"
    FIELD_NAME2 = "stats__PneumaticPressure__val"
    MIN_PRESSURE = 75.25
    MAX_ROWS = 50

    assets = [MACHINE4]
    fields = [
        {"asset": MACHINE4, "name": FIELD_NAME1},
        {"asset": MACHINE4, "name": FIELD_NAME2},
    ]

    time_selection = {
        "time_type": "absolute",
        "start_time": START_DATETIME,
        "end_time": END_DATETIME,
        "time_zone": TIME_ZONE,
    }

    filters = [
        {
            "asset": MACHINE4,
            "name": FIELD_NAME2,
            "op": "gte",
            "value": MIN_PRESSURE,
        }
    ]

    query = {
        "assets": assets,
        "fields": fields,
        "time_selection": time_selection,
        "filters": filters,
        "limit": MAX_ROWS,
    }

    return perform_test(get_line_data, config, cli, **query)


def perform_get_kpi_data_viz_load_test(
    config: t_.Dict[str, t_.Any], cli: Client
) -> t_.Dict[str, t_.Any]:
    machine_sources = ["Nagoya - Pick and Place 6"]
    kpis = ["quality"]
    i_vars = [
        {
            "name": "endtime",
            "time_resolution": "day",
            "query_tz": "America/Los_Angeles",
            "output_tz": "America/Los_Angeles",
            "bin_strategy": "user_defined2",
            "bin_count": 50,
        }
    ]
    time_selection = {
        "time_type": "relative",
        "relative_start": 7,
        "relative_unit": "year",
        "ctime_tz": "America/Los_Angeles",
    }

    data_viz_query = {
        "where": [],
        "db_mode": "sql",
    }

    query = {
        "machine_sources": machine_sources,
        "kpis": kpis,
        "i_vars": i_vars,
        "time_selection": time_selection,
        "where": [],
        "db_mode": "sql",
    }

    return perform_test(get_kpi_data_viz, config, cli, **query)


# Main function
def main(xml_file: str) -> None:
    # Read configuration from config.json
    config = read_config()

    # Get environment variables
    tenant = os.environ.get("ENV_VAR_TENANT", "")
    api_key = os.environ.get("ENV_VAR_API_KEY", "")
    api_secret = os.environ.get("ENV_VAR_API_SECRET", "")

    # Initialize SDK client
    cli: Client = Client(tenant)
    cli.login("apikey", key_id=api_key, secret_id=api_secret)

    metrics = {}

    metrics["get_cycles"] = perform_get_cycles_load_test(config, cli)
    metrics["get_line_data"] = perform_get_line_data_load_test(config, cli)
    metrics["get_kpi_data_viz"] = perform_get_kpi_data_viz_load_test(config, cli)

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
