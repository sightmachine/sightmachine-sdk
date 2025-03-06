ALERT_PAYLOAD = {
    "capturetime": "2025-03-03 08:10:42.863000",
    "capturetime_epoch": 1740989442863,
    "updatetime": "2025-03-03 08:10:42.863000",
    "localtz": "UTC",
    "updatelocation": "",
    "version": 0,
    "tombstone": False,
    "tombstone_epoch": 0,
    "audit_keys": [
        "id"
    ],
    "system_fixture": False,
    "created_by": {
        "_id": "8b8f8cdfab8df8c254d6b942",
        "metadata": None,
        "email": None,
        "username": None,
        "roles": None,
        "is_active": False
    },
    "enabled": True,
    "display_name": "Data latency updated FROM SMSDK",
    "sidebar_params": {
        "asset": {

        },
        "chartType": {

        },
        "specLimits": {

        },
        "yAxis": {

        },
        "dateRange": {

        }
    },
    "trigger": {
        "trigger_type": "periodic",
        "schedule": {
            "interval": {
                "every": 10,
                "period": "days"
            }
        }
    },
    "analytic": {
        "plugin_id": "DataLatencyAlertingETL3",
        "plugin_version": 1,
        "plugin_type": "analytic",
        "plugin_parameters": {
            "output_type": "alert",
            "time_selection": {
                "time_type": "relative",
                "relative_unit": "minute",
                "relative_start": 14400
            },
            "asset_selection": {

            },
            "spec_limits": {

            },
            "analytics": {

            },
            "alert_config": {
                "max_latency": {
                    "every": 1,
                    "period": "days"
                },
                "black_list": [],
                "white_list": [
                    "genmills-ms-rbg.v1.MS_RBG_ALL_LINE.PRODUCT_MATRIX_1st_Oct_v1"
                ]
            }
        }
    },
    "notification": {
        "backend": {
            "email": {
                "silence_window": {
                    "every": 1,
                    "period": "days"
                },
                "email_list": [
                    {
                        "to_email": "cjadhav@sightmachine.com",
                        "name": "chaitanya jadhav"
                    }
                ],
                "subject": "Data Latency Alert"
            }
        }
    },
    "id": "67c5640266af93c9e3095134",
    "incident_total": 0
}
ALERT_UPDATES = {"display_name": "Updated Name Data latency updated FROM SMSDK 2"}
UPDATED_ALERT = {'analytic': {'plugin_id': 'DataLatencyAlertingETL3',
                              'plugin_parameters': {'alert_config': {'black_list': [],
                                                                     'max_latency': {'every': 1,
                                                                                     'period': 'days'},
                                                                     'white_list': [
                                                                         'genmills-ms-rbg.v1.MS_RBG_ALL_LINE.PRODUCT_MATRIX_1st_Oct_v1']},
                                                    'analytics': {},
                                                    'asset_selection': {},
                                                    'output_type': 'alert',
                                                    'spec_limits': {},
                                                    'time_selection': {'relative_start': 14400,
                                                                       'relative_unit': 'minute',
                                                                       'time_type': 'relative'}},
                              'plugin_type': 'analytic',
                              'plugin_version': 1},
                 'display_name': 'Updated Name Data latency updated FROM SMSDK 2',
                 'enabled': True,
                 'notification': {'backend': {'email': {'email_list': [{'name': 'chaitanya '
                                                                                'jadhav',
                                                                        'to_email': 'cjadhav@sightmachine.com'}],
                                                        'silence_window': {'every': 1,
                                                                           'period': 'days'},
                                                        'subject': 'Data Latency Alert'}}},
                 'sidebar_params': {'asset': {},
                                    'chartType': {},
                                    'dateRange': {},
                                    'specLimits': {},
                                    'yAxis': {}},
                 'trigger': {'schedule': {'interval': {'every': 10, 'period': 'days'}},
                             'trigger_type': 'periodic'}}
ALERTS_LIST = [{
    "capturetime": "2025-03-03 08:10:42.863000",
    "capturetime_epoch": 1740989442863,
    "updatetime": "2025-03-03 08:10:42.863000",
    "localtz": "UTC",
    "updatelocation": "",
    "version": 0,
    "tombstone": False,
    "tombstone_epoch": 0,
    "audit_keys": [
        "id"
    ],
    "system_fixture": False,
    "created_by": {
        "_id": "8b8f8cdfab8df8c254d6b942",
        "metadata": None,
        "email": None,
        "username": None,
        "roles": None,
        "is_active": False
    },
    "enabled": True,
    "display_name": "Data latency updated FROM SMSDK",
    "sidebar_params": {
        "asset": {

        },
        "chartType": {

        },
        "specLimits": {

        },
        "yAxis": {

        },
        "dateRange": {

        }
    },
    "trigger": {
        "trigger_type": "periodic",
        "schedule": {
            "interval": {
                "every": 10,
                "period": "days"
            }
        }
    },
    "analytic": {
        "plugin_id": "DataLatencyAlertingETL3",
        "plugin_version": 1,
        "plugin_type": "analytic",
        "plugin_parameters": {
            "output_type": "alert",
            "time_selection": {
                "time_type": "relative",
                "relative_unit": "minute",
                "relative_start": 14400
            },
            "asset_selection": {

            },
            "spec_limits": {

            },
            "analytics": {

            },
            "alert_config": {
                "max_latency": {
                    "every": 1,
                    "period": "days"
                },
                "black_list": [],
                "white_list": [
                    "genmills-ms-rbg.v1.MS_RBG_ALL_LINE.PRODUCT_MATRIX_1st_Oct_v1"
                ]
            }
        }
    },
    "notification": {
        "backend": {
            "email": {
                "silence_window": {
                    "every": 1,
                    "period": "days"
                },
                "email_list": [
                    {
                        "to_email": "cjadhav@sightmachine.com",
                        "name": "chaitanya jadhav"
                    }
                ],
                "subject": "Data Latency Alert"
            }
        }
    },
    "id": "67c5640266af93c9e3095134",
    "incident_total": 0
},{
    "capturetime": "2025-03-03 08:10:42.863000",
    "capturetime_epoch": 1740989442863,
    "updatetime": "2025-03-03 08:10:42.863000",
    "localtz": "UTC",
    "updatelocation": "",
    "version": 0,
    "tombstone": False,
    "tombstone_epoch": 0,
    "audit_keys": [
        "id"
    ],
    "system_fixture": False,
    "created_by": {
        "_id": "8b8f8cdfab8df8c254d6b942",
        "metadata": None,
        "email": None,
        "username": None,
        "roles": None,
        "is_active": False
    },
    "enabled": True,
    "display_name": "Data latency updated FROM SMSDK",
    "sidebar_params": {
        "asset": {

        },
        "chartType": {

        },
        "specLimits": {

        },
        "yAxis": {

        },
        "dateRange": {

        }
    },
    "trigger": {
        "trigger_type": "periodic",
        "schedule": {
            "interval": {
                "every": 10,
                "period": "days"
            }
        }
    },
    "analytic": {
        "plugin_id": "DataLatencyAlertingETL3",
        "plugin_version": 1,
        "plugin_type": "analytic",
        "plugin_parameters": {
            "output_type": "alert",
            "time_selection": {
                "time_type": "relative",
                "relative_unit": "minute",
                "relative_start": 14400
            },
            "asset_selection": {

            },
            "spec_limits": {

            },
            "analytics": {

            },
            "alert_config": {
                "max_latency": {
                    "every": 1,
                    "period": "days"
                },
                "black_list": [],
                "white_list": [
                    "genmills-ms-rbg.v1.MS_RBG_ALL_LINE.PRODUCT_MATRIX_1st_Oct_v1"
                ]
            }
        }
    },
    "notification": {
        "backend": {
            "email": {
                "silence_window": {
                    "every": 1,
                    "period": "days"
                },
                "email_list": [
                    {
                        "to_email": "cjadhav@sightmachine.com",
                        "name": "chaitanya jadhav"
                    }
                ],
                "subject": "Data Latency Alert"
            }
        }
    },
    "id": "67c5640266af93c9e3095134",
    "incident_total": 0
},{
    "capturetime": "2025-03-03 08:10:42.863000",
    "capturetime_epoch": 1740989442863,
    "updatetime": "2025-03-03 08:10:42.863000",
    "localtz": "UTC",
    "updatelocation": "",
    "version": 0,
    "tombstone": False,
    "tombstone_epoch": 0,
    "audit_keys": [
        "id"
    ],
    "system_fixture": False,
    "created_by": {
        "_id": "8b8f8cdfab8df8c254d6b942",
        "metadata": None,
        "email": None,
        "username": None,
        "roles": None,
        "is_active": False
    },
    "enabled": True,
    "display_name": "Data latency updated FROM SMSDK",
    "sidebar_params": {
        "asset": {

        },
        "chartType": {

        },
        "specLimits": {

        },
        "yAxis": {

        },
        "dateRange": {

        }
    },
    "trigger": {
        "trigger_type": "periodic",
        "schedule": {
            "interval": {
                "every": 10,
                "period": "days"
            }
        }
    },
    "analytic": {
        "plugin_id": "SPC",
        "plugin_version": 1,
        "plugin_type": "analytic",
        "plugin_parameters": {
            "output_type": "alert",
            "time_selection": {
                "time_type": "relative",
                "relative_unit": "minute",
                "relative_start": 14400
            },
            "asset_selection": {

            },
            "spec_limits": {

            },
            "analytics": {

            },
            "alert_config": {
                "max_latency": {
                    "every": 1,
                    "period": "days"
                },
                "black_list": [],
                "white_list": [
                    "genmills-ms-rbg.v1.MS_RBG_ALL_LINE.PRODUCT_MATRIX_1st_Oct_v1"
                ]
            }
        }
    },
    "notification": {
        "backend": {
            "email": {
                "silence_window": {
                    "every": 1,
                    "period": "days"
                },
                "email_list": [
                    {
                        "to_email": "cjadhav@sightmachine.com",
                        "name": "chaitanya jadhav"
                    }
                ],
                "subject": "Data Latency Alert"
            }
        }
    },
    "id": "67c5640266af93c9e3095134",
    "incident_total": 0
}]
FILTERED_ALERTS = [{
    "capturetime": "2025-03-03 08:10:42.863000",
    "capturetime_epoch": 1740989442863,
    "updatetime": "2025-03-03 08:10:42.863000",
    "localtz": "UTC",
    "updatelocation": "",
    "version": 0,
    "tombstone": False,
    "tombstone_epoch": 0,
    "audit_keys": [
        "id"
    ],
    "system_fixture": False,
    "created_by": {
        "_id": "8b8f8cdfab8df8c254d6b942",
        "metadata": None,
        "email": None,
        "username": None,
        "roles": None,
        "is_active": False
    },
    "enabled": True,
    "display_name": "Data latency updated FROM SMSDK",
    "sidebar_params": {
        "asset": {

        },
        "chartType": {

        },
        "specLimits": {

        },
        "yAxis": {

        },
        "dateRange": {

        }
    },
    "trigger": {
        "trigger_type": "periodic",
        "schedule": {
            "interval": {
                "every": 10,
                "period": "days"
            }
        }
    },
    "analytic": {
        "plugin_id": "DataLatencyAlertingETL3",
        "plugin_version": 1,
        "plugin_type": "analytic",
        "plugin_parameters": {
            "output_type": "alert",
            "time_selection": {
                "time_type": "relative",
                "relative_unit": "minute",
                "relative_start": 14400
            },
            "asset_selection": {

            },
            "spec_limits": {

            },
            "analytics": {

            },
            "alert_config": {
                "max_latency": {
                    "every": 1,
                    "period": "days"
                },
                "black_list": [],
                "white_list": [
                    "genmills-ms-rbg.v1.MS_RBG_ALL_LINE.PRODUCT_MATRIX_1st_Oct_v1"
                ]
            }
        }
    },
    "notification": {
        "backend": {
            "email": {
                "silence_window": {
                    "every": 1,
                    "period": "days"
                },
                "email_list": [
                    {
                        "to_email": "cjadhav@sightmachine.com",
                        "name": "chaitanya jadhav"
                    }
                ],
                "subject": "Data Latency Alert"
            }
        }
    },
    "id": "67c5640266af93c9e3095134",
    "incident_total": 0
},{
    "capturetime": "2025-03-03 08:10:42.863000",
    "capturetime_epoch": 1740989442863,
    "updatetime": "2025-03-03 08:10:42.863000",
    "localtz": "UTC",
    "updatelocation": "",
    "version": 0,
    "tombstone": False,
    "tombstone_epoch": 0,
    "audit_keys": [
        "id"
    ],
    "system_fixture": False,
    "created_by": {
        "_id": "8b8f8cdfab8df8c254d6b942",
        "metadata": None,
        "email": None,
        "username": None,
        "roles": None,
        "is_active": False
    },
    "enabled": True,
    "display_name": "Data latency updated FROM SMSDK",
    "sidebar_params": {
        "asset": {

        },
        "chartType": {

        },
        "specLimits": {

        },
        "yAxis": {

        },
        "dateRange": {

        }
    },
    "trigger": {
        "trigger_type": "periodic",
        "schedule": {
            "interval": {
                "every": 10,
                "period": "days"
            }
        }
    },
    "analytic": {
        "plugin_id": "DataLatencyAlertingETL3",
        "plugin_version": 1,
        "plugin_type": "analytic",
        "plugin_parameters": {
            "output_type": "alert",
            "time_selection": {
                "time_type": "relative",
                "relative_unit": "minute",
                "relative_start": 14400
            },
            "asset_selection": {

            },
            "spec_limits": {

            },
            "analytics": {

            },
            "alert_config": {
                "max_latency": {
                    "every": 1,
                    "period": "days"
                },
                "black_list": [],
                "white_list": [
                    "genmills-ms-rbg.v1.MS_RBG_ALL_LINE.PRODUCT_MATRIX_1st_Oct_v1"
                ]
            }
        }
    },
    "notification": {
        "backend": {
            "email": {
                "silence_window": {
                    "every": 1,
                    "period": "days"
                },
                "email_list": [
                    {
                        "to_email": "cjadhav@sightmachine.com",
                        "name": "chaitanya jadhav"
                    }
                ],
                "subject": "Data Latency Alert"
            }
        }
    },
    "id": "67c5640266af93c9e3095134",
    "incident_total": 0
}]