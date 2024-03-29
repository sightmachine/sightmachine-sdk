AVALIBLE_KPI_JSON = [
    {
        "name": "Scrap_Rate",
        "display_name": "Scrap Rate",
        "unit": "",
        "type": "continuous",
        "data_type": "float",
        "stream_types": [],
        "raw_data_field": "",
    },
    {
        "name": "oee",
        "display_name": "OEE",
        "unit": "",
        "type": "continuous",
        "data_type": "float",
        "stream_types": [],
        "raw_data_field": "",
    },
    {
        "name": "quality",
        "display_name": "Quality",
        "unit": "",
        "type": "continuous",
        "data_type": "float",
        "stream_types": [],
        "raw_data_field": "",
    },
    {
        "name": "performance",
        "display_name": "Performance",
        "unit": "",
        "type": "continuous",
        "data_type": "float",
        "stream_types": [],
        "raw_data_field": "",
    },
    {
        "name": "availability",
        "display_name": "Availability",
        "unit": "",
        "type": "continuous",
        "data_type": "float",
        "stream_types": [],
        "raw_data_field": "",
    },
]

KPI_DATA_VIZ_JSON = [
    {
        "i_vals": {
            "endtime": {
                "i_pos": 0,
                "bin_no": 0,
                "bin_min": "2022-10-20T00:00:00-07:00",
                "bin_max": "2022-10-20T00:00:00-07:00",
                "bin_avg": "2022-10-20T00:00:00-07:00",
            }
        },
        "d_vals": {"quality": {"avg": 95.18072289156626}},
        "_count": 418,
        "kpi_dependencies": {"quality": {"Output": 395.0, "ScrapQuantity": 20.0}},
    },
    {
        "i_vals": {
            "endtime": {
                "i_pos": 0,
                "bin_no": 1,
                "bin_min": "2022-10-21T00:00:00-07:00",
                "bin_max": "2022-10-21T00:00:00-07:00",
                "bin_avg": "2022-10-21T00:00:00-07:00",
            }
        },
        "d_vals": {"quality": {"avg": 93.29123914759275}},
        "_count": 1282,
        "kpi_dependencies": {"quality": {"Output": 1182.0, "ScrapQuantity": 85.0}},
    },
    {
        "i_vals": {
            "endtime": {
                "i_pos": 0,
                "bin_no": 2,
                "bin_min": "2022-10-22T00:00:00-07:00",
                "bin_max": "2022-10-22T00:00:00-07:00",
                "bin_avg": "2022-10-22T00:00:00-07:00",
            }
        },
        "d_vals": {"quality": {"avg": 92.7477840451249}},
        "_count": 1260,
        "kpi_dependencies": {"quality": {"Output": 1151.0, "ScrapQuantity": 90.0}},
    },
]
