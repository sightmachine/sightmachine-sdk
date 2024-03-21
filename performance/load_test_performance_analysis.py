import os
import sys
import json
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
def read_config(config_file: t_.Optional[str]) -> t_.Dict[str, t_.Any]:
    config = {}

    if config_file is None:
        raise ValueError("No config file specified.")

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file '{config_file}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON in config file '{config_file}'.")

    # Check for mandatory key-value pairs
    mandatory_keys = {
        "num_peak_users",
        "ramp_up_rate",
        "total_run_time",
        "min_wait_time",
        "max_wait_time",
        "get_cycles_query_config",
        "get_line_data_query_config",
        "get_kpi_data_viz_query_config",
    }
    missing_keys = mandatory_keys - set(config.keys())
    if missing_keys:
        raise ValueError(f"Missing mandatory keys in config file: {missing_keys}")

    return config


def dump_to_xunit_xml(
    metrics_dict: t_.Dict[str, t_.Dict[str, t_.Any]], xml_file: str
) -> None:
    total_time = 0
    errors = 0

    for api_name, api_metrics in metrics_dict.items():
        # Error count update
        errors += api_metrics.get("error_rate", 0) > 0
        # Total run time update
        total_time += api_metrics.get("run_time", 0)

    # Round total_time to nearest integer
    total_time = int(round(total_time))

    root = ET.Element(
        "testsuites",
        name="Performance Metrics",
        tests=str(len(metrics_dict)),
        failures="0",
        errors=str(errors),
        time=str(total_time),
    )

    for api_name, api_metrics in metrics_dict.items():
        testcase = ET.SubElement(root, "testcase", name=api_name)
        for metric_name, metric_value in api_metrics.items():
            ET.SubElement(testcase, metric_name).text = str(metric_value)

    # Convert the ElementTree to a string
    xml_content = ET.tostring(root, encoding="unicode", method="xml")

    # Prettify the XML content
    prettified_xml = xml.dom.minidom.parseString(xml_content).toprettyxml(indent="\t")

    # Write the prettified XML content to the file
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
    total_responses = len(response_times)
    avg_response_time = (
        sum(response_times) / total_responses if total_responses > 0 else 0
    )
    min_response_time = min(response_times) if total_responses > 0 else 0
    max_response_time = max(response_times) if total_responses > 0 else 0
    throughput = total_responses / elapsed_time if elapsed_time > 0 else 0
    error_rate = (len(errors) / (len(response_times) + len(errors))) * 100

    logger.info("Performance Metrics:")
    logger.info(f"Run Time: {elapsed_time}")
    logger.info(f"Number of Response: {total_responses}")
    logger.info(f"Average Response Time: {avg_response_time} seconds")
    logger.info(f"Minimum Response Time: {min_response_time} seconds")
    logger.info(f"Maximum Response Time: {max_response_time} seconds")
    logger.info(f"Throughput: {throughput} requests per second")
    logger.info(f"Error Rate: {error_rate}%")

    # Store performance metrics in XML file
    return {
        "run_time": elapsed_time,
        "num_response": total_responses,
        "avg_response_time": avg_response_time,
        "min_response_time": min_response_time,
        "max_response_time": max_response_time,
        "throughput": throughput,
        "error_rate": error_rate,
    }


def get_time_selection(config: t_.Dict[str, t_.Any]) -> t_.Dict[str, t_.Any]:
    time_selection = {}
    time_selection["time_type"] = config.get("TIME_TYPE", "relative")

    if time_selection["time_type"] == "absolute":
        time_selection["start_time"] = config.get("START_DATETIME", "")
        time_selection["end_time"] = config.get("END_DATETIME", "")
        time_selection["time_zone"] = config.get("TIME_ZONE", "")
    else:
        time_selection["time_type"] = "relative"
        time_selection["relative_start"] = config.get("RELATIVE_START", "7")
        time_selection["relative_unit"] = config.get("RELATIVE_UNIT", "day")
        time_selection["ctime_tz"] = config.get("TIME_ZONE", "America/Los_Angeles")

    return time_selection


def perform_get_cycles_load_test(
    config: t_.Dict[str, t_.Any], cli: Client
) -> t_.Dict[str, t_.Any]:
    # Extract the 'get_cycles' configuration
    get_cycles_config = config.get("get_cycles_query_config", {})

    # Convert datetime strings to datetime objects
    for key, value in get_cycles_config.items():
        if isinstance(value, str):
            try:
                get_cycles_config[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                pass  # Handle the case where the value is not a valid datetime string

    return perform_test(get_cycles, config, cli, **get_cycles_config)


def perform_get_line_data_load_test(
    config: t_.Dict[str, t_.Any], cli: Client
) -> t_.Dict[str, t_.Any]:
    # Extract the 'get_line_data' configuration
    line_data_config = config.get("get_line_data_query_config", {})

    time_selection = get_time_selection(line_data_config)

    assets = line_data_config.get("ASSETS", [])

    fields = []
    for asset in assets:
        for field in line_data_config.get("FIELDS", []):
            fields.append({"asset": asset, "name": field})

    filters = []
    for filter in line_data_config.get("FILTERS", []):
        filters.append(
            {
                "asset": filter.get("asset", ""),
                "name": filter.get("field", ""),
                "op": filter.get("op", ""),
                "value": filter.get("value", ""),
            }
        )

    query = {
        "time_selection": time_selection,
        "assets": assets,
        "fields": fields,
        "filters": filters,
        "limit": line_data_config.get("MAX_ROWS", 100),
    }

    print(f"DebugInf:: query - {query}")

    return perform_test(get_line_data, config, cli, **query)


def perform_get_kpi_data_viz_load_test(
    config: t_.Dict[str, t_.Any], cli: Client
) -> t_.Dict[str, t_.Any]:
    # Extract the 'get_kpi_data_viz' configuration
    kpi_data_viz_config = config.get("get_kpi_data_viz_query_config", {})

    time_selection = get_time_selection(kpi_data_viz_config)

    assets = kpi_data_viz_config.get("ASSETS", [])

    query = {
        "machine_sources": assets,
        "kpis": kpi_data_viz_config.get("KPIS", []),
        "i_vars": kpi_data_viz_config.get("I_VARS", []),
        "time_selection": time_selection,
        "where": kpi_data_viz_config.get("WHERE", []),
        "db_mode": kpi_data_viz_config.get("DB_MODE", "sql"),
    }

    return perform_test(get_kpi_data_viz, config, cli, **query)


# Main function
def main(config_file: t_.Optional[str], xml_file: t_.Optional[str]) -> None:
    # Read configurations
    config = read_config(config_file)

    # Get environment variables
    tenant = os.environ.get("ENV_SDK_VAR_TENANT", "")
    api_key = os.environ.get("ENV_SDK_VAR_API_KEY", "")
    api_secret = os.environ.get("ENV_SDK_VAR_API_SECRET", "")

    # Initialize SDK client
    cli: Client = Client(tenant)
    cli.login("apikey", key_id=api_key, secret_id=api_secret)

    metrics = {}

    # Perform load test on 'get_cycles' API and store the metrics
    metrics["get_cycles"] = perform_get_cycles_load_test(config, cli)
    # Perform load test on 'get_line_data' API and store the metrics
    metrics["get_line_data"] = perform_get_line_data_load_test(config, cli)
    # Perform load test on 'get_kpi_data_viz' API and store the metrics
    metrics["get_kpi_data_viz"] = perform_get_kpi_data_viz_load_test(config, cli)

    if xml_file:
        dump_to_xunit_xml(metrics, xml_file)
        logger.info(f"Performance metrics dumped to {xml_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load testing script with optional performance metrics dump to XML"
    )
    parser.add_argument(
        "--config-file",
        help="Path to the configuration file",
        required=True,
    )
    parser.add_argument(
        "--metrics-xml",
        help="Path to the XML file to dump performance metrics",
        default=None,
    )
    args = parser.parse_args()
    main(args.config_file, args.metrics_xml)
