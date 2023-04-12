from __future__ import unicode_literals

JSON_MACHINETYPE = [
    {
        "version": 0,
        "analytics": {
            "extra_indexes": [],
            "model": "machinetype",
            "table_name": "analytics_autonosew_robot2",
            "update_range_require_delete": True,
            "extra_columns": [],
        },
        "tag": "nike",
        "id": "57083f6786b984c6774a55ec",
        "updatelocation": "tenant_pc",
        "stats": [
            {
                "func": "strptime",
                "vars": ["Year", "Month", "Day", "Hour", "Minute", "Second"],
                "title": "PLC-StartTime",
                "parse": "%Y-%m-%d %H:%M:%S",
                "analytics": {"disabled": True},
                "splice": "{Year}-{Month}-{Day} {Hour}:{Minute}:{Second}",
                "timezone": "factory",
                "display": {"title_prefix": "PLC-StartTime"},
                "unit": "datetime",
                "row": "first",
            },
            {
                "func": "strptime",
                "vars": ["Year", "Month", "Day", "Hour", "Minute", "Second"],
                "title": "PLC-EndTime",
                "parse": "%Y-%m-%d %H:%M:%S",
                "analytics": {"disabled": True},
                "splice": "{Year}-{Month}-{Day} {Hour}:{Minute}:{Second}",
                "timezone": "factory",
                "display": {"title_prefix": "PLC-EndTime"},
                "unit": "datetime",
                "row": "last",
            },
            {
                "title": "AutoFuse_Vision_System",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__AutoFuse_Vision_System__val",
                        }
                    ]
                },
                "func": "set",
                "var": "AutoFuse_Vision_System",
                "display": {"title_prefix": "Auto Fuse Vision System"},
                "unit": "word",
            },
            {
                "title": "Gender",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__Gender__val",
                        }
                    ]
                },
                "func": "set",
                "var": "Gender",
                "display": {"title_prefix": "Gender"},
                "unit": "word",
            },
            {
                "title": "Grabit_DaughterBoard_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__Grabit_DaughterBoard_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "Grabit_DaughterBoard_Ver",
                "display": {
                    "title_prefix": "Grabit Daughter Board Version",
                    "version_field": True,
                },
                "unit": "word",
            },
            {
                "title": "Grabit_MotherBoard_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__Grabit_MotherBoard_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "Grabit_MotherBoard_Ver",
                "display": {
                    "title_prefix": "Grabit Mother Board Version",
                    "version_field": True,
                },
                "unit": "word",
            },
            {
                "title": "HMI_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__HMI_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "HMI_Ver",
                "display": {"title_prefix": "HMI Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "FP_HMI_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__FP_HMI_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "FP_HMI_Ver",
                "display": {"title_prefix": "FP HMI Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "Model_No",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__Model_No__val",
                        }
                    ]
                },
                "func": "set",
                "var": "Model_No",
                "display": {"title_prefix": "Model No"},
                "unit": "word",
            },
            {
                "title": "PLC_Program_93_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__PLC_Program_93_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "PLC_Program_93_Ver",
                "display": {
                    "title_prefix": "PLC Program 93 Version",
                    "version_field": True,
                },
                "unit": "word",
            },
            {
                "title": "FP_PLC_Program_93_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__FP_PLC_Program_93_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "FP_PLC_Program_93_Ver",
                "display": {
                    "title_prefix": "FP PLC Program 93 Version",
                    "version_field": True,
                },
                "unit": "word",
            },
            {
                "title": "PLC_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__PLC_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "PLC_Ver",
                "display": {"title_prefix": "PLC Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "FP_PLC_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__FP_PLC_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "FP_PLC_Ver",
                "display": {"title_prefix": "FP PLC Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "RB_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__RB_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "RB_Ver",
                "display": {"title_prefix": "RB Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "FP_RB_Ver",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__FP_RB_Ver__val",
                        }
                    ]
                },
                "func": "set",
                "var": "FP_RB_Ver",
                "display": {"title_prefix": "FP RB Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "Right_foot_or_Left_foot",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__Right_foot_or_Left_foot__val",
                        }
                    ]
                },
                "func": "set",
                "var": "Right_foot_or_Left_foot",
                "display": {"title_prefix": "Right Foot Or Left Foot"},
                "unit": "word",
            },
            {
                "title": "Size",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__Size__val",
                        }
                    ]
                },
                "func": "set",
                "var": "Size",
                "display": {"title_prefix": "Size"},
                "unit": "word",
            },
            {
                "title": "GB2_L_C_0ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_0ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_0ms",
                "variance": 53690.46975589595,
                "display": {"title_prefix": "GB2 Leakage Current 0ms"},
                "unit": "mA",
            },
            {
                "title": "GB2_L_C_100ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_100ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_100ms",
                "variance": 30139.85462829628,
                "display": {"title_prefix": "GB2 Leakage Current 100ms"},
                "unit": "mA",
            },
            {
                "title": "GB2_L_C_200ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_200ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_200ms",
                "variance": 2061.662424033839,
                "display": {"title_prefix": "GB2 Leakage Current 200ms"},
                "unit": "mA",
            },
            {
                "title": "GB2_L_C_3200ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_3200ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_3200ms",
                "variance": 1322.8958581261809,
                "display": {"title_prefix": "GB2 Leakage Current 3200ms"},
                "unit": "mA",
            },
            {
                "title": "GB2_L_C_3300ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_3300ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_3300ms",
                "variance": 1308.5974394959946,
                "display": {"title_prefix": "GB2 Leakage Current 3300ms"},
                "unit": "mA",
            },
            {
                "title": "GB2_L_C_3400ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_3400ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_3400ms",
                "variance": 1298.5714705211058,
                "display": {"title_prefix": "GB2 Leakage Current 3400ms"},
                "unit": "mA",
            },
            {
                "title": "GB2_L_C_6400ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_6400ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_6400ms",
                "variance": 2416.8823781513815,
                "display": {"title_prefix": "GB2 Leakage Current 6400ms"},
                "unit": "mA",
            },
            {
                "title": "GB2_L_C_6500ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_6500ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_6500ms",
                "variance": 10696.245591518315,
                "display": {"title_prefix": "GB2 Leakage Current 6500ms"},
                "unit": "mA",
            },
            {
                "title": "GB2_L_C_6600ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_6600ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_6600ms",
                "variance": 40197.257732135724,
                "display": {"title_prefix": "GB2 Leakage Current 6600ms"},
                "unit": "mA",
            },
            {
                "title": "GB2_L_C_9500ms",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__GB2_L_C_9500ms__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "GB2_L_C_9500ms",
                "display": {"title_prefix": "GB2 Leakage Current 9500ms"},
                "unit": "mA",
            },
            {
                "title": "Input_PLC_Grabit2_Bit_Data_1",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Bit_Data_1__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Bit_Data_1",
                "variance": 39.32529551685402,
                "display": {"title_prefix": "Input PLC Grabit2 Bit Data 1"},
                "unit": "",
            },
            {
                "title": "Input_PLC_Grabit2_Data_Register_3",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Data_Register_3__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Data_Register_3",
                "variance": 2302353.055203016,
                "display": {"title_prefix": "Input PLC Grabit2 Data Register 3"},
                "unit": "",
            },
            {
                "title": "Robot2_Picks_component_count",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Robot2_Picks_component_count__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Robot2_Picks_component_count",
                "variance": 5677.235758524685,
                "display": {"title_prefix": "Robot2 Picks Component Count"},
                "unit": "",
            },
            {
                "title": "ALARM",
                "in_timeline": True,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ALARM__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ALARM",
                "variance": 0.010712818228182281,
                "display": {
                    "title_prefix": "ALARM",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "AUTO_MODE",
                "in_timeline": True,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__AUTO_MODE__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "AUTO_MODE",
                "variance": 0.04087711877118771,
                "display": {
                    "title_prefix": "AUTO MODE",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "AUTO_RUN",
                "in_timeline": True,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__AUTO_RUN__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "AUTO_RUN",
                "variance": 0.10881302563025635,
                "display": {
                    "title_prefix": "AUTO RUN",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "BLOCKED",
                "in_timeline": True,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__BLOCKED__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "BLOCKED",
                "variance": 0.013415174151741517,
                "display": {
                    "title_prefix": "BLOCKED",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "DOWN",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__DOWN__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "DOWN",
                "variance": 0.010712818228182281,
                "display": {
                    "title_prefix": "DOWN",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "EMS",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__EMS__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "EMS",
                "variance": 0.0,
                "display": {
                    "title_prefix": "EMS",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "IDLE",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__IDLE__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "IDLE",
                "variance": 0.10156033720337204,
                "display": {
                    "title_prefix": "IDLE",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "LD_REMINDING",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__LD_REMINDING__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "LD_REMINDING",
                "variance": 0.2245141226412264,
                "display": {
                    "title_prefix": "LD REMINDING",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "LD_REQUEST",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__LD_REQUEST__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "LD_REQUEST",
                "variance": 0.12418205772057722,
                "display": {
                    "title_prefix": "LD REQUEST",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "MANUAL_MODE",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__MANUAL_MODE__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "MANUAL_MODE",
                "variance": 0.10789469804698047,
                "display": {
                    "title_prefix": "MANUAL MODE",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "RUN",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__RUN__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "RUN",
                "variance": 0.10978829538295387,
                "display": {
                    "title_prefix": "RUN",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST12_FD4_conveyor_Start_High_Speed",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST12_FD4_conveyor_Start_High_Speed__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST12_FD4_conveyor_Start_High_Speed",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST12 FD4 Conveyor Start High Speed",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST12_FD4_conveyor_Start_Low_Speed",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST12_FD4_conveyor_Start_Low_Speed__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST12_FD4_conveyor_Start_Low_Speed",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST12 FD4 Conveyor Start Low Speed",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST12_FD4_conveyor_Stop",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST12_FD4_conveyor_Stop__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST12_FD4_conveyor_Stop",
                "variance": 0.01931210312103121,
                "display": {
                    "title_prefix": "ST12 FD4 Conveyor Busy",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST12_FD5_conveyor_Start_High_Speed",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST12_FD5_conveyor_Start_High_Speed__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST12_FD5_conveyor_Start_High_Speed",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST12 FD5 Conveyor Start High Speed",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST12_FD5_conveyor_Start_Low_Speed",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST12_FD5_conveyor_Start_Low_Speed__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST12_FD5_conveyor_Start_Low_Speed",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST12 FD5 Conveyor Start Low Speed",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST12_FD5_conveyor_Stop",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST12_FD5_conveyor_Stop__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST12_FD5_conveyor_Stop",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST12 FD5 Conveyor Busy",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST12_FD6_conveyor_Start_High_Speed",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST12_FD6_conveyor_Start_High_Speed__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST12_FD6_conveyor_Start_High_Speed",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST12 FD6 Conveyor Start High Speed",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST12_FD6_conveyor_Start_Low_Speed",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST12_FD6_conveyor_Start_Low_Speed__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST12_FD6_conveyor_Start_Low_Speed",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST12 FD6 Conveyor Start Low Speed",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST12_FD6_conveyor_Stop",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST12_FD6_conveyor_Stop__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST12_FD6_conveyor_Stop",
                "variance": 0.015395544355443555,
                "display": {
                    "title_prefix": "ST12 FD6 Conveyor Busy",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Calculate_Piece_Coordinate_and_Grbit",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Calculate_Piece_Coordinate_and_Grbit__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Calculate_Piece_Coordinate_and_Grbit",
                "variance": 0.06494581705817058,
                "display": {
                    "title_prefix": "ST14 RB2 Calculate Place Coordinate And Grabit",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Calculate_Piece_Coordinate_and_Nozzle",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Calculate_Piece_Coordinate_and_Nozzle__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Calculate_Piece_Coordinate_and_Nozzle",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST14 RB2 Calculate Place Coordinate And Nozzle",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Call_Vision",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Call_Vision__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Call_Vision",
                "variance": 0.00992949839498395,
                "display": {
                    "title_prefix": "ST14 RB2 Call Vision",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Go_Home",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Go_Home__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Go_Home",
                "variance": 0.010575829658296584,
                "display": {
                    "title_prefix": "ST14 RB2 Go Home",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Grabit_Pack1",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Grabit_Pack1__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Grabit_Pack1",
                "variance": 0.0757779977799778,
                "display": {
                    "title_prefix": "ST14 RB2 Grabit Pick1",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Move_Busy",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Move_Busy__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Move_Busy",
                "variance": 0.13606135811358114,
                "display": {
                    "title_prefix": "ST14 RB2 Move Busy",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Nozzle_Tool_Pack2",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Nozzle_Tool_Pack2__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Nozzle_Tool_Pack2",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST14 RB2 Nozzle Tool Pick2",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Nozzle_Tool_Piace2",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Nozzle_Tool_Piace2__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Nozzle_Tool_Piace2",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST14 RB2 Nozzle Tool Place2",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Place_and_Base",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Place_and_Base__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Place_and_Base",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST14 RB2 Place The Base",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Robot_end",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Robot_end__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Robot_end",
                "variance": 0.0024340707407074073,
                "display": {
                    "title_prefix": "ST14 RB2 Robot End",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Vacuum_Tool_Pick3",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Vacuum_Tool_Pick3__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Vacuum_Tool_Pick3",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST14 RB2 Vacuum Tool Pick3",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Vacuum_Tool_Piece3",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Vacuum_Tool_Piece3__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Vacuum_Tool_Piece3",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST14 RB2 Vacuum Tool Place3",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Wait_time",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Wait_time__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Wait_time",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST14 RB2 Wait Time",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_Weld",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_Weld__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_Weld",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ST14 RB2 Weld",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ST14_RB2_robot_Start",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ST14_RB2_robot_Start__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ST14_RB2_robot_Start",
                "variance": 0.002244959949599496,
                "display": {
                    "title_prefix": "ST14 RB2 Robot Start",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "STARVED",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__STARVED__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "STARVED",
                "variance": 0.21492085920859208,
                "display": {
                    "title_prefix": "STARVED",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "STOP",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__STOP__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "STOP",
                "variance": 0.10881302563025631,
                "display": {
                    "title_prefix": "STOP",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ULD_REMINDING",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ULD_REMINDING__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ULD_REMINDING",
                "variance": 0.08714019780197801,
                "display": {
                    "title_prefix": "ULD REMINDING",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ULD_REQUEST",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ULD_REQUEST__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ULD_REQUEST",
                "variance": 0.20223354873548735,
                "display": {
                    "title_prefix": "ULD REQUEST",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "WARNING",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__WARNING__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "WARNING",
                "variance": 0.13789694656946577,
                "display": {
                    "title_prefix": "WARNING",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Curret_In_Eq_Count",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Curret_In_Eq_Count__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Curret_In_Eq_Count",
                "variance": 1.1008183512835128,
                "display": {"title_prefix": "Current In Eq Count"},
                "unit": "",
            },
            {
                "title": "FD4_conveyor_high_speed",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__FD4_conveyor_high_speed__val",
                        }
                    ]
                },
                "func": "avg",
                "var": "FD4_conveyor_high_speed",
                "variance": 0.0,
                "display": {"title_prefix": "FD4 Conveyor High Speed"},
                "unit": "mm/sec",
            },
            {
                "title": "FD4_conveyor_low_speed",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__FD4_conveyor_low_speed__val",
                        }
                    ]
                },
                "func": "avg",
                "var": "FD4_conveyor_low_speed",
                "variance": 0.0,
                "display": {"title_prefix": "FD4 Conveyor Low Speed"},
                "unit": "mm/sec",
            },
            {
                "title": "FD4_delay_Time_Scaled",
                "analytics": {"disabled": True},
                "func": "pre_scale",
                "multiplier": 0.1,
                "var": "FD4_delay_Time",
                "unit": "sec",
            },
            {
                "title": "FD4_delay_Time",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__FD4_delay_Time__val",
                        }
                    ]
                },
                "func": "avg",
                "var": "FD4_delay_Time_Scaled",
                "variance": 0.0,
                "display": {"title_prefix": "FD4 Delay Time"},
                "unit": "sec",
            },
            {
                "title": "FD5_conveyor_high_speed",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__FD5_conveyor_high_speed__val",
                        }
                    ]
                },
                "func": "avg",
                "var": "FD5_conveyor_high_speed",
                "variance": 0.0,
                "display": {"title_prefix": "FD5 Conveyor High Speed"},
                "unit": "mm/sec",
            },
            {
                "title": "FD5_conveyor_low_speed",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__FD5_conveyor_low_speed__val",
                        }
                    ]
                },
                "func": "avg",
                "var": "FD5_conveyor_low_speed",
                "variance": 0.0,
                "display": {"title_prefix": "FD5 Conveyor Low Speed"},
                "unit": "mm/sec",
            },
            {
                "title": "FD5_delay_Time_Scaled",
                "analytics": {"disabled": True},
                "func": "pre_scale",
                "multiplier": 0.1,
                "var": "FD5_delay_Time",
                "unit": "sec",
            },
            {
                "title": "FD5_delay_Time",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__FD5_delay_Time__val",
                        }
                    ]
                },
                "func": "avg",
                "var": "FD5_delay_Time_Scaled",
                "variance": 0.0,
                "display": {"title_prefix": "FD5 Delay Time"},
                "unit": "sec",
            },
            {
                "title": "FD6_conveyor_high_speed",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__FD6_conveyor_high_speed__val",
                        }
                    ]
                },
                "func": "avg",
                "var": "FD6_conveyor_high_speed",
                "variance": 0.0,
                "display": {"title_prefix": "FD6 Conveyor High Speed"},
                "unit": "mm/sec",
            },
            {
                "title": "FD6_conveyor_low_speed",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__FD6_conveyor_low_speed__val",
                        }
                    ]
                },
                "func": "avg",
                "var": "FD6_conveyor_low_speed",
                "variance": 0.0,
                "display": {"title_prefix": "FD6 Conveyor Low Speed"},
                "unit": "mm/sec",
            },
            {
                "title": "FD6_delay_Time_Scaled",
                "analytics": {"disabled": True},
                "func": "pre_scale",
                "multiplier": 0.1,
                "var": "FD6_delay_Time",
                "unit": "sec",
            },
            {
                "title": "FD6_delay_Time",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__FD6_delay_Time__val",
                        }
                    ]
                },
                "func": "avg",
                "var": "FD6_delay_Time_Scaled",
                "variance": 0.0,
                "display": {"title_prefix": "FD6 Delay Time"},
                "unit": "sec",
            },
            {
                "title": "Input_PLC_Grabit2_Bit_Data_2",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Bit_Data_2__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Bit_Data_2",
                "variance": 0.0,
                "display": {"title_prefix": "Input PLC Grabit2 Bit Data 2"},
                "unit": "",
            },
            {
                "title": "Input_PLC_Grabit2_Data_Register_1",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Data_Register_1__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Data_Register_1",
                "variance": 601880.1485429002,
                "display": {"title_prefix": "Input PLC Grabit2 Data Register 1"},
                "unit": "",
            },
            {
                "title": "Input_PLC_Grabit2_Data_Register_2",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Data_Register_2__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Data_Register_2",
                "variance": 0.0,
                "display": {"title_prefix": "Input PLC Grabit2 Data Register 2"},
                "unit": "",
            },
            {
                "title": "Input_PLC_Grabit2_Data_Register_4",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Data_Register_4__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Data_Register_4",
                "variance": 0.0,
                "display": {"title_prefix": "Input PLC Grabit2 Data Register 4"},
                "unit": "",
            },
            {
                "title": "Input_PLC_Grabit2_Data_Register_5",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Data_Register_5__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Data_Register_5",
                "variance": 0.0,
                "display": {"title_prefix": "Input PLC Grabit2 Data Register 5"},
                "unit": "",
            },
            {
                "title": "Input_PLC_Grabit2_Data_Register_6",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Data_Register_6__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Data_Register_6",
                "variance": 0.0,
                "display": {"title_prefix": "Input PLC Grabit2 Data Register 6"},
                "unit": "",
            },
            {
                "title": "Input_PLC_Grabit2_Data_Register_7",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Data_Register_7__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Data_Register_7",
                "variance": 0.0,
                "display": {"title_prefix": "Input PLC Grabit2 Data Register 7"},
                "unit": "",
            },
            {
                "title": "Input_PLC_Grabit2_Data_Register_8",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Input_PLC_Grabit2_Data_Register_8__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Input_PLC_Grabit2_Data_Register_8",
                "variance": 0.0,
                "display": {"title_prefix": "Input PLC Grabit2 Data Register 8"},
                "unit": "",
            },
            {
                "title": "Line_mode",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__Line_mode__val",
                        }
                    ]
                },
                "func": "lookup_table",
                "table": {"1": "EMPTY", "0": "AUTO", "2": "DRY RUN"},
                "var": "Line_mode",
                "variance": 0.02563332993329933,
                "display": {"title_prefix": "Line Mode"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Bit_Data_1",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Bit_Data_1__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Bit_Data_1",
                "variance": 1.8955560506607902,
                "display": {"title_prefix": "Output PLC Grabit2 Bit Data 1"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Bit_Data_2",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Bit_Data_2__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Bit_Data_2",
                "variance": 0.0,
                "display": {"title_prefix": "Output PLC Grabit2 Bit Data 2"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Data_Register_1",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Data_Register_1__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Data_Register_1",
                "variance": 563973.549944626,
                "display": {"title_prefix": "Output PLC Grabit2 Data Register 1"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Data_Register_2",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Data_Register_2__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Data_Register_2",
                "variance": 0.0,
                "display": {"title_prefix": "Output PLC Grabit2 Data Register 2"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Data_Register_3",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Data_Register_3__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Data_Register_3",
                "variance": 0.0,
                "display": {"title_prefix": "Output PLC Grabit2 Data Register 3"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Data_Register_4",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Data_Register_4__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Data_Register_4",
                "variance": 0.0,
                "display": {"title_prefix": "Output PLC Grabit2 Data Register 4"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Data_Register_5",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Data_Register_5__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Data_Register_5",
                "variance": 0.0,
                "display": {"title_prefix": "Output PLC Grabit2 Data Register 5"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Data_Register_6",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Data_Register_6__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Data_Register_6",
                "variance": 0.0,
                "display": {"title_prefix": "Output PLC Grabit2 Data Register 6"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Data_Register_7",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Data_Register_7__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Data_Register_7",
                "variance": 0.0,
                "display": {"title_prefix": "Output PLC Grabit2 Data Register 7"},
                "unit": "",
            },
            {
                "title": "Output_PLC_Grabit2_Data_Register_8",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Output_PLC_Grabit2_Data_Register_8__val",
                        }
                    ]
                },
                "func": "timeseries",
                "var": "Output_PLC_Grabit2_Data_Register_8",
                "variance": 0.0,
                "display": {"title_prefix": "Output PLC Grabit2 Data Register 8"},
                "unit": "",
            },
            {
                "title": "Pieces_per_Pair",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Pieces_per_Pair__val",
                        }
                    ]
                },
                "func": "max",
                "var": "Pieces_per_Pair",
                "variance": 0.0,
                "display": {"title_prefix": "Pieces Per Pair"},
                "unit": "pcs",
            },
            {
                "title": "Pieces_per_Pan",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Pieces_per_Pan__val",
                        }
                    ]
                },
                "func": "max",
                "var": "Pieces_per_Pan",
                "variance": 5.157519735197352,
                "display": {"title_prefix": "Pieces Per Pan"},
                "unit": "pcs",
            },
            {
                "title": "Production_Batch_Count_Setting_Value",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Production_Batch_Count_Setting_Value__val",
                        }
                    ]
                },
                "func": "max",
                "var": "Production_Batch_Count_Setting_Value",
                "variance": 0.0,
                "display": {"title_prefix": "Production Batch Count Setting Value"},
                "unit": "",
            },
            {
                "title": "Recipe_Number",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Recipe_Number__val",
                        }
                    ]
                },
                "func": "max",
                "var": "Recipe_Number",
                "variance": 1.206183831438322,
                "display": {"title_prefix": "Recipe Number"},
                "unit": "",
            },
            {
                "title": "Alarms",
                "analytics": {"disabled": True},
                "func": "collect_events",
                "var": "Alarms",
                "display": {"title_prefix": "Alarms"},
                "unit": "word",
            },
            {
                "title": "Total_NG_Count",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__Total_NG_Count__val",
                        }
                    ]
                },
                "func": "max",
                "var": "Total_NG_Count",
                "display": {"title_prefix": "Total NG Count"},
                "unit": "word",
            },
        ],
        "scaffold": None,
        "part_type": "",
        "metadata": {
            "local_to_utc_convert_flag": False,
            "output_type": "pairs",
            "calcplugin": {"calc_type": "OutputPerfStatCalculator"},
            "downtime_classifier": {
                "code_map": {
                    "F204": "UD_ANS_04_01",
                    "F205": "UD_ANS_04_01",
                    "F206": "UD_ANS_04_01",
                    "F207": "UD_ANS_04_01",
                    "F200": "UD_ANS_04_01",
                    "F201": "UD_ANS_04_01",
                    "F202": "UD_ANS_04_01",
                    "F203": "UD_ANS_04_01",
                    "F240": "UD_ANS_01_02",
                    "F241": "UD_ANS_01_02",
                    "F242": "UD_ANS_01_02",
                    "F243": "UD_ANS_01_02",
                    "F244": "UD_ANS_01_02",
                    "F209": "UD_ANS_01_03",
                    "F246": "UD_ANS_01_02",
                    "F247": "UD_ANS_01_02",
                    "F23": "UD_ANS_01_02",
                    "F22": "UD_ANS_01_02",
                    "F21": "UD_ANS_01_02",
                    "F20": "UD_ANS_01_02",
                    "F27": "UD_ANS_01_02",
                    "F26": "UD_ANS_01_02",
                    "F25": "UD_ANS_01_02",
                    "F24": "UD_ANS_01_02",
                    "F309": "UD_ANS_01_03",
                    "F29": "UD_ANS_01_02",
                    "F28": "UD_ANS_01_02",
                    "F308": "UD_ANS_01_03",
                    "F249": "UD_ANS_01_02",
                    "F314": "UD_ANS_01_03",
                    "F44": "UD_ANS_01_02",
                    "F320": "UD_ANS_01_03",
                    "F40": "UD_ANS_01_02",
                    "F305": "UD_ANS_01_03",
                    "F302": "UD_ANS_01_03",
                    "F304": "UD_ANS_01_03",
                    "F236": "UD_ANS_01_02",
                    "F306": "UD_ANS_01_03",
                    "F307": "UD_ANS_01_03",
                    "F312": "UD_ANS_01_03",
                    "F313": "UD_ANS_01_03",
                    "F310": "UD_ANS_01_03",
                    "F311": "UD_ANS_01_03",
                    "F239": "UD_ANS_01_02",
                    "F238": "UD_ANS_01_02",
                    "F211": "UD_ANS_01_02",
                    "F315": "UD_ANS_01_03",
                    "F235": "UD_ANS_01_02",
                    "F301": "UD_ANS_01_03",
                    "F234": "UD_ANS_01_02",
                    "F319": "UD_ANS_01_03",
                    "F231": "UD_ANS_01_02",
                    "F230": "UD_ANS_01_02",
                    "F43": "UD_ANS_01_02",
                    "F245": "UD_ANS_01_02",
                    "F30": "UD_ANS_01_02",
                    "F215": "UD_ANS_04_01",
                    "F303": "UD_ANS_01_03",
                    "F318": "UD_ANS_01_03",
                    "F316": "UD_ANS_01_03",
                    "F10": "UD_ANS_01_01",
                    "F11": "UD_ANS_01_07",
                    "F233": "UD_ANS_01_02",
                    "F1": "UD_ANS_01_03",
                    "F2": "UD_ANS_01_03",
                    "F3": "UD_ANS_01_03",
                    "F4": "UD_ANS_04_01",
                    "F5": "UD_ANS_04_01",
                    "F6": "UD_ANS_04_01",
                    "F41": "UD_ANS_01_02",
                    "F237": "UD_ANS_01_02",
                    "F9": "UD_ANS_01_03",
                    "F210": "UD_ANS_01_02",
                    "F7": "UD_ANS_01_03",
                    "F42": "UD_ANS_01_02",
                    "F248": "UD_ANS_01_02",
                    "F341": "UD_ANS_01_03",
                    "F340": "UD_ANS_01_03",
                    "F321": "UD_ANS_01_03",
                    "F317": "UD_ANS_01_03",
                    "F300": "UD_ANS_01_03",
                    "F8": "UD_ANS_01_01",
                    "F232": "UD_ANS_01_02",
                }
            },
            "timezone": "Asia/Taipei",
        },
        "localtz": "UTC",
        "cmdr_meta": None,
        "etlsettings": {
            "boundary_end_cycle_in_shift": True,
            "down_fields": ["DOWN"],
            "modules": {
                "get_group_record_by_index": "GetGroupRecordByIndexMultiRecords",
                "update_machinestate": "UpdateMachineStateSticky",
                "group": "GroupByCounterNonCycle",
                "get_record_groups": "GetRecordGroup",
                "process_record": "ProcessRecordExplicitDowntime",
            },
            "sticky_types": ["csv"],
        },
        "source_type": "AutoNoSew_Robot2",
        "capturetime": "2017-07-12T20:59:52.545000Z",
        "tombstone_epoch": 0,
        "updatetime": "2017-07-12 20:59:52.545000",
        "source_type_clean": "AutoNoSew_Robot2",
        "recipes": {
            "DEFAULT": {
                "cycle_finished_product_ratio": 0.5,
                "default_intended_pieces": 2,
                "cycle_threshold": 1600000,
                "cycle_ideal": 40000,
            }
        },
        "tombstone": False,
        "meta_assign": {
            "cycles_per_part": "Pieces_per_Pair",
            "intended_pieces": "Pieces_per_Pan",
        },
        "capturetime_epoch": 1499893192545,
        "etlpluginmap": {
            "xml": "AssociateFileByTimestampAnalyzer",
            "downtime_mod": "DowntimeAnalyzer",
            "multipart/form-data": "AssociateFileByTimestampAnalyzer",
            "csv": ["AssociateFileByTimestampAnalyzer", "EventAnalyzer"],
            "defect": "DefectAnalyzer",
            "cycle": "EventAnalyzer",
        },
    },
    {
        "version": 0,
        "analytics": {
            "extra_indexes": [],
            "model": "machinetype",
            "table_name": "analytics_autoassembly_bottomdryoven",
            "update_range_require_delete": True,
            "extra_columns": [],
        },
        "tag": "nike",
        "id": "5735315689fdcd2266ed362b",
        "updatelocation": "tenant_pc",
        "stats": [
            {
                "func": "strptime",
                "vars": ["Year", "Month", "Day", "Hour", "Minute", "Second"],
                "title": "PLC-StartTime",
                "parse": "%Y-%m-%d %H:%M:%S",
                "analytics": {"disabled": True},
                "splice": "{Year}-{Month}-{Day} {Hour}:{Minute}:{Second}",
                "timezone": "factory",
                "display": {"title_prefix": "PLC-StartTime"},
                "unit": "datetime",
                "row": "first",
            },
            {
                "func": "strptime",
                "vars": ["Year", "Month", "Day", "Hour", "Minute", "Second"],
                "title": "PLC-EndTime",
                "parse": "%Y-%m-%d %H:%M:%S",
                "analytics": {"disabled": True},
                "splice": "{Year}-{Month}-{Day} {Hour}:{Minute}:{Second}",
                "timezone": "factory",
                "display": {"title_prefix": "PLC-EndTime"},
                "unit": "datetime",
                "row": "last",
            },
            {
                "title": "HMI-Version",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__HMI-Version__val",
                        }
                    ]
                },
                "func": "set",
                "var": "HMI-Ver",
                "display": {"title_prefix": "HMI-Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBD_Parameter_PLC4_Barcode_Number_11_20_Output__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output"
                },
                "unit": "word",
            },
            {
                "map": {
                    "BB": "BB",
                    "CL": "Cleat",
                    "YA": "YA",
                    "TR": "Training",
                    "SW": "NSW",
                    "TN": "TN",
                    "GF": "GF",
                    "FB": "FB",
                    "JD": "JD",
                    "SB": "SB",
                    "RN": "RN",
                    "CP": "CP",
                },
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_category",
                "in_timeline": False,
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output Category"
                },
                "analytics": {"disabled": True},
                "range": "0-1",
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output",
                "invalid_value": "-1",
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_category",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBDParameterPLC4BarcodeNumber1120OutputCategory__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_category",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output Category"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_model_id",
                "in_timeline": False,
                "analytics": {"disabled": True},
                "range": "2-7",
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_model_id",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBDParameterPLC4BarcodeNumber1120OutputModelId__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output Model ID"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_material_way",
                "in_timeline": False,
                "analytics": {"disabled": True},
                "range": "8-10",
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_material_way",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBDParameterPLC4BarcodeNumber1120OutputMaterialWay__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_material_way",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output Material Way"
                },
                "unit": "word",
            },
            {
                "map": {
                    "G": "Grade school",
                    "I": "Infant",
                    "M": "Men",
                    "P": "pre school",
                    "T": "Toddler",
                    "W": "Women",
                },
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_gender",
                "in_timeline": False,
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output"
                },
                "analytics": {"disabled": True},
                "range": 11,
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output",
                "invalid_value": "-1",
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_gender",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBDParameterPLC4BarcodeNumber1120OutputGender__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_gender",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output Gender"
                },
                "unit": "word",
            },
            {
                "map": {"R": "Right", "B": "Both", "L": "Left"},
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_left_right",
                "in_timeline": False,
                "analytics": {"disabled": True},
                "range": 12,
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_left_right",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBDParameterPLC4BarcodeNumber1120OutputLeftRight__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_left_right",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output Left Right Shoe"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_size",
                "in_timeline": False,
                "analytics": {"disabled": True},
                "range": "13-15",
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output",
                "output_type": "float",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output"
                },
                "unit": "",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_size",
                "analytics": {"disabled": True},
                "func": "pre_scale",
                "multiplier": 0.1,
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_size",
                "unit": "",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_size",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Parameter_PLC4_Barcode_Number_11_20_Output_size__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_11_20_Output_size",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 11 20 Output Size"
                },
                "unit": "",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBD_Parameter_PLC4_Barcode_Number_1_10_Input__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input"
                },
                "unit": "",
            },
            {
                "map": {
                    "BB": "BB",
                    "CL": "Cleat",
                    "YA": "YA",
                    "TR": "Training",
                    "SW": "NSW",
                    "TN": "TN",
                    "GF": "GF",
                    "FB": "FB",
                    "JD": "JD",
                    "SB": "SB",
                    "RN": "RN",
                    "CP": "CP",
                },
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_category",
                "in_timeline": False,
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input Category"
                },
                "analytics": {"disabled": True},
                "range": "0-1",
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input",
                "invalid_value": "-1",
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_category",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBDParameterPLC4BarcodeNumber110InputCategory__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_category",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input Category"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_model_id",
                "in_timeline": False,
                "analytics": {"disabled": True},
                "range": "2-7",
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_model_id",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBDParameterPLC4BarcodeNumber110InputModelId__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input Model ID"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_material_way",
                "in_timeline": False,
                "analytics": {"disabled": True},
                "range": "8-10",
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_material_way",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBDParameterPLC4BarcodeNumber110InputMaterialWay__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_material_way",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input Material Way"
                },
                "unit": "word",
            },
            {
                "map": {
                    "G": "Grade school",
                    "I": "Infant",
                    "M": "Men",
                    "P": "pre school",
                    "T": "Toddler",
                    "W": "Women",
                },
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_gender",
                "in_timeline": False,
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input"
                },
                "analytics": {"disabled": True},
                "range": 11,
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input",
                "invalid_value": "-1",
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_gender",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBD_Parameter_PLC4_Barcode_Number_1_10_Input_gender__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_gender",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input Gender"
                },
                "unit": "word",
            },
            {
                "map": {"R": "Right", "B": "Both", "L": "Left"},
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_left_right",
                "in_timeline": False,
                "analytics": {"disabled": True},
                "range": 12,
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_left_right",
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__OBDParameterPLC4BarcodeNumber110InputLeftRight__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_left_right",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input Left Right Shoe"
                },
                "unit": "word",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_size",
                "in_timeline": False,
                "analytics": {"disabled": True},
                "range": "13-15",
                "func": "pre_substr",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input",
                "output_type": "float",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input"
                },
                "unit": "",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_size",
                "analytics": {"disabled": True},
                "func": "pre_scale",
                "multiplier": 0.1,
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_size",
                "unit": "",
            },
            {
                "title": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_size",
                "analytics": {
                    "columns": [
                        {
                            "type": "float",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Parameter_PLC4_Barcode_Number_1_10_Input_size__val",
                        }
                    ]
                },
                "func": "last",
                "var": "OBD_Parameter_PLC4_Barcode_Number_1_10_Input_size",
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Barcode Number 1 10 Input Size"
                },
                "unit": "",
            },
            {
                "title": "PLC-Program_93_Version",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__PLC-Program_93_Version__val",
                        }
                    ]
                },
                "func": "set",
                "var": "PLC-Program_93_Ver",
                "display": {
                    "title_prefix": "PLC-Program 93 Version",
                    "version_field": True,
                },
                "unit": "word",
            },
            {
                "title": "FP_Program_93_Version",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__FP_Program_93_Version__val",
                        }
                    ]
                },
                "func": "set",
                "var": "FP_Program_93_Ver",
                "display": {
                    "title_prefix": "FP PLC Program 93 Version",
                    "version_field": True,
                },
                "unit": "word",
            },
            {
                "title": "PLC-Version",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__PLC-Version__val",
                        }
                    ]
                },
                "func": "set",
                "var": "PLC-Ver",
                "display": {"title_prefix": "PLC-Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "FP_PLC_Version",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__FP_PLC_Version__val",
                        }
                    ]
                },
                "func": "set",
                "var": "FP_PLC_Ver",
                "display": {"title_prefix": "FP PLC Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "FP_HMI_Version",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__FP_HMI_Version__val",
                        }
                    ]
                },
                "func": "set",
                "var": "FP_HMI_Ver",
                "display": {"title_prefix": "FP HMI Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "FP_RB_Version",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__FP_RB_Version__val",
                        }
                    ]
                },
                "func": "set",
                "var": "FP_RB_Ver",
                "display": {"title_prefix": "FP RB Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "RB-Version",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "string",
                            "source_field": "val",
                            "stat_type": "Categorical",
                            "name": "stats__RB-Version__val",
                        }
                    ]
                },
                "func": "set",
                "var": "RB-Ver",
                "display": {"title_prefix": "RB-Version", "version_field": True},
                "unit": "word",
            },
            {
                "title": "ALARM",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ALARM__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ALARM",
                "variance": 0.033738135781357814,
                "display": {
                    "title_prefix": "ALARM",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "AUTO_MODE",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__AUTO_MODE__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "AUTO_MODE",
                "variance": 0.034453711637116406,
                "display": {
                    "title_prefix": "AUTO MODE",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "AUTO_RUN",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__AUTO_RUN__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "AUTO_RUN",
                "variance": 0.034565123151231565,
                "display": {
                    "title_prefix": "AUTO RUN",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "BLOCKED",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__BLOCKED__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "BLOCKED",
                "variance": 0.0,
                "display": {
                    "title_prefix": "BLOCKED",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "DOWN",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__DOWN__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "DOWN",
                "variance": 0.033738135781357814,
                "display": {
                    "title_prefix": "DOWN",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "EMS",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__EMS__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "EMS",
                "variance": 0.033738135781357814,
                "display": {
                    "title_prefix": "EMS",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "IDLE",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__IDLE__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "IDLE",
                "variance": 0.21751571755717558,
                "display": {
                    "title_prefix": "IDLE",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "LD_REMINDING",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__LD_REMINDING__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "LD_REMINDING",
                "variance": 0.0,
                "display": {
                    "title_prefix": "LD REMINDING",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "LD_REQUEST",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__LD_REQUEST__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "LD_REQUEST",
                "variance": 0.0,
                "display": {
                    "title_prefix": "LD REQUEST",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "MANUAL_MODE",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__MANUAL_MODE__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "MANUAL_MODE",
                "variance": 0.03445371163711637,
                "display": {
                    "title_prefix": "MANUAL MODE",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Run",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Run__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "Run",
                "variance": 0.034565123151231565,
                "display": {
                    "title_prefix": "Run",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "STARVED",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__STARVED__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "STARVED",
                "variance": 0.21751571755717558,
                "display": {
                    "title_prefix": "STARVED",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "STOP",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__STOP__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "STOP",
                "variance": 0.03456512315123151,
                "display": {
                    "title_prefix": "STOP",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ULD_REMINDING",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ULD_REMINDING__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ULD_REMINDING",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ULD REMINDING",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "ULD_REQUEST",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__ULD_REQUEST__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "ULD_REQUEST",
                "variance": 0.0,
                "display": {
                    "title_prefix": "ULD REQUEST",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "WARNING",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__WARNING__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "WARNING",
                "variance": 0.06487698116981169,
                "display": {
                    "title_prefix": "WARNING",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "OBD_Loading_Start",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Loading_Start__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "OBD_Loading_Start",
                "variance": 0.07221199961999619,
                "display": {
                    "title_prefix": "OBD Loading Start",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "OBD_Unloading_End",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Unloading_End__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "OBD_Unloading_End",
                "variance": 0.07282708187081871,
                "display": {
                    "title_prefix": "OBD Unloading End",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Online_signal_PLC1_To_PC_1",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Online_signal_PLC1_To_PC_1__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "Online_signal_PLC1_To_PC_1",
                "variance": 0.0,
                "display": {
                    "title_prefix": "Online signal PLC1 To PC",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Online_signal_PLC1_To_PC_2",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Online_signal_PLC1_To_PC_2__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "Online_signal_PLC1_To_PC_2",
                "variance": 0.0,
                "display": {
                    "title_prefix": "Online signal PC To PLC1",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Online_signal_PLC2_To_PC_1",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Online_signal_PLC2_To_PC_1__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "Online_signal_PLC2_To_PC_1",
                "variance": 0.0,
                "display": {
                    "title_prefix": "Online signal PLC2 To PC",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Online_signal_PLC2_To_PC_2",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Online_signal_PLC2_To_PC_2__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "Online_signal_PLC2_To_PC_2",
                "variance": 0.0,
                "display": {
                    "title_prefix": "Online signal PC To PLC2",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Online_signal_PLC3_To_PC_1",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Online_signal_PLC3_To_PC_1__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "Online_signal_PLC3_To_PC_1",
                "variance": 0.0,
                "display": {
                    "title_prefix": "Online signal PLC3 To PC PBT",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Online_signal_PLC3_To_PC_2",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Online_signal_PLC3_To_PC_2__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "Online_signal_PLC3_To_PC_2",
                "variance": 0.0,
                "display": {
                    "title_prefix": "Online signal PC To PBT",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Online_signal_PLC4_To_PC_1",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Online_signal_PLC4_To_PC_1__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "Online_signal_PLC4_To_PC_1",
                "variance": 0.0,
                "display": {
                    "title_prefix": "Online signal PLC4 To PC CBT",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "Online_signal_PLC4_To_PC_2",
                "in_timeline": False,
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Online_signal_PLC4_To_PC_2__val",
                        }
                    ]
                },
                "func": "hightimer",
                "var": "Online_signal_PLC4_To_PC_2",
                "variance": 0.0,
                "display": {
                    "title_prefix": "Online signal PC To CBT",
                    "custom": {
                        "val": {
                            "ui": {
                                "formatting": {
                                    "duration": True,
                                    "formatString": "seconds",
                                }
                            }
                        }
                    },
                },
                "unit": "",
            },
            {
                "title": "LBT_Input_Count",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__LBT_Input_Count__val",
                        }
                    ]
                },
                "func": "max",
                "var": "LBT_Input_Count",
                "variance": 194302.90866471163,
                "display": {"title_prefix": "LBT Input Count"},
                "unit": "pcs",
            },
            {
                "title": "LBT_Output_Count",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__LBT_Output_Count__val",
                        }
                    ]
                },
                "func": "max",
                "var": "LBT_Output_Count",
                "variance": 194302.90866471163,
                "display": {"title_prefix": "LBT Output Count"},
                "unit": "pcs",
            },
            {
                "title": "OBD_Parameter_PLC4_Bottom_Surface_Temperature",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Parameter_PLC4_Bottom_Surface_Temperature__val",
                        }
                    ]
                },
                "func": "max",
                "var": "OBD_Parameter_PLC4_Bottom_Surface_Temperature",
                "variance": 15.358038535485473,
                "display": {
                    "title_prefix": "OBD Parameter PLC4 Bottom Surface Temperature"
                },
                "unit": "\u00b0C",
            },
            {
                "title": "OBD_Parameter_PLC4_Conveyer_Speed_Scaled",
                "analytics": {"disabled": True},
                "func": "pre_scale",
                "multiplier": 0.01,
                "var": "OBD_Parameter_PLC4_Conveyer_Speed",
                "unit": "mm/sec",
            },
            {
                "title": "OBD_Parameter_PLC4_Conveyer_Speed",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Parameter_PLC4_Conveyer_Speed__val",
                        }
                    ]
                },
                "func": "max",
                "var": "OBD_Parameter_PLC4_Conveyer_Speed_Scaled",
                "variance": 0.0,
                "display": {"title_prefix": "OBD Parameter PLC4 Conveyer Speed"},
                "unit": "mm/sec",
            },
            {
                "title": "OBD_Parameter_PLC4_Input_Count",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Parameter_PLC4_Input_Count__val",
                        }
                    ]
                },
                "func": "max",
                "var": "OBD_Parameter_PLC4_Input_Count",
                "variance": 350295.4093487171,
                "display": {"title_prefix": "OBD Parameter PLC4 Input Count"},
                "unit": "pcs",
            },
            {
                "title": "OBD_Parameter_PLC4_MIR_S_V_1_Scaled",
                "analytics": {"disabled": True},
                "func": "pre_scale",
                "multiplier": 0.1,
                "var": "OBD_Parameter_PLC4_MIR_S_V_1",
                "unit": "%",
            },
            {
                "title": "OBD_Parameter_PLC4_MIR_S_V_1",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Parameter_PLC4_MIR_S_V_1__val",
                        }
                    ]
                },
                "func": "max",
                "var": "OBD_Parameter_PLC4_MIR_S_V_1_Scaled",
                "variance": 0.0,
                "display": {"title_prefix": "OBD Parameter PLC4 MIR S V"},
                "unit": "%",
            },
            {
                "title": "OBD_Parameter_PLC4_MIR_S_V_2",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Parameter_PLC4_MIR_S_V_2__val",
                        }
                    ]
                },
                "func": "max",
                "var": "OBD_Parameter_PLC4_MIR_S_V_2",
                "variance": 0.0,
                "display": {"title_prefix": "OBD Parameter PLC4 NIR S V"},
                "unit": "\u00b0C",
            },
            {
                "title": "OBD_Parameter_PLC4_MIR_S_V_3",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Parameter_PLC4_MIR_S_V_3__val",
                        }
                    ]
                },
                "func": "max",
                "var": "OBD_Parameter_PLC4_MIR_S_V_3",
                "variance": 0.1394422548227481,
                "display": {"title_prefix": "OBD Parameter PLC4 NIR P V"},
                "unit": "\u00b0C",
            },
            {
                "title": "OBD_Parameter_PLC4_Output_Count",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__OBD_Parameter_PLC4_Output_Count__val",
                        }
                    ]
                },
                "func": "max",
                "var": "OBD_Parameter_PLC4_Output_Count",
                "variance": 351439.9613755354,
                "display": {"title_prefix": "OBD Parameter PLC4 Output Count"},
                "unit": "pcs",
            },
            {
                "title": "Pieces_per_Pair",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Pieces_per_Pair__val",
                        }
                    ]
                },
                "func": "max",
                "var": "Pieces_per_Pair",
                "variance": 0.0,
                "display": {"title_prefix": "Pieces per Pair"},
                "unit": "pcs",
            },
            {
                "title": "Total_Line_Pieces_Count",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Total_Line_Pieces_Count__val",
                        }
                    ]
                },
                "func": "max",
                "var": "Total_Line_Pieces_Count",
                "variance": 0.0,
                "display": {"title_prefix": "Total Line Pieces Count"},
                "unit": "pcs",
            },
            {
                "title": "Total_NG_Pieces_Count",
                "analytics": {
                    "columns": [
                        {
                            "type": "int",
                            "source_field": "val",
                            "stat_type": "Continuous",
                            "name": "stats__Total_NG_Pieces_Count__val",
                        }
                    ]
                },
                "func": "max",
                "var": "Total_NG_Pieces_Count",
                "variance": 0.0,
                "display": {"title_prefix": "Total NG Pieces Count"},
                "unit": "pcs",
            },
            {
                "title": "Alarms",
                "analytics": {"disabled": True},
                "func": "collect_events",
                "var": "Alarms",
                "display": {"title_prefix": "Alarms"},
                "unit": "word",
            },
        ],
        "scaffold": None,
        "part_type": "",
        "metadata": {
            "output_type": "pairs",
            "calcplugin": {"calc_type": "OutputPerfStatCalculator"},
            "downtime_classifier": {
                "code_map": {
                    "F89": "UD_AA_02_01",
                    "F88": "UD_AA_02_01",
                    "F85": "UD_AA_02_01",
                    "F84": "UD_AA_02_01",
                    "F87": "UD_AA_02_01",
                    "F86": "UD_AA_02_01",
                    "F81": "UD_AA_02_01",
                    "F80": "UD_AA_02_01",
                    "F83": "UD_AA_02_01",
                    "F82": "UD_AA_02_01",
                    "F74": "UD_AA_02_01",
                    "F21": "UD_AA_02_01",
                    "F76": "UD_AA_02_01",
                    "F77": "UD_AA_02_01",
                    "F4": "UD_AA_02_01",
                    "F5": "UD_AA_02_01",
                    "F92": "UD_AA_02_01",
                    "F93": "UD_AA_02_01",
                    "F90": "UD_AA_02_01",
                    "F91": "UD_AA_02_01",
                    "F96": "UD_AA_02_01",
                    "F97": "UD_AA_02_01",
                    "F94": "UD_AA_02_01",
                    "F95": "UD_AA_02_01",
                    "F98": "UD_AA_02_01",
                    "F130": "UD_AA_02_01",
                    "F99": "UD_AA_02_01",
                    "F110": "UD_AA_02_01",
                    "F111": "UD_AA_02_01",
                    "F112": "UD_AA_02_01",
                    "F113": "UD_AA_02_01",
                    "F56": "UD_AA_02_01",
                    "F57": "UD_AA_02_01",
                    "F54": "UD_AA_02_01",
                    "F55": "UD_AA_02_01",
                    "F52": "UD_AA_02_01",
                    "F53": "UD_AA_02_01",
                    "F51": "UD_AA_02_01",
                    "F2": "UD_AA_02_01",
                    "F124": "UD_AA_02_01",
                    "F6": "UD_AA_02_01",
                    "F31": "UD_AA_02_01",
                    "F32": "UD_AA_02_01",
                    "F3": "UD_AA_02_01",
                    "F34": "UD_AA_02_01",
                    "F79": "UD_AA_02_01",
                    "F12": "UD_AA_02_01",
                    "F75": "UD_AA_02_01",
                    "F10": "UD_AA_02_01",
                    "F11": "UD_AA_02_01",
                    "F71": "UD_AA_02_01",
                    "F72": "UD_AA_02_01",
                    "F73": "UD_AA_02_01",
                    "F1": "UD_AA_02_01",
                    "F127": "UD_AA_02_01",
                    "F126": "UD_AA_02_01",
                    "F121": "UD_AA_02_01",
                    "F120": "UD_AA_02_01",
                    "F123": "UD_AA_02_01",
                    "F122": "UD_AA_02_01",
                    "F7": "UD_AA_02_01",
                    "F129": "UD_AA_02_01",
                    "F128": "UD_AA_02_01",
                    "F33": "UD_AA_02_01",
                    "F78": "UD_AA_02_01",
                    "F109": "UD_AA_02_01",
                    "F108": "UD_AA_02_01",
                    "F107": "UD_AA_02_01",
                    "F106": "UD_AA_02_01",
                    "F105": "UD_AA_02_01",
                    "F104": "UD_AA_02_01",
                    "F103": "UD_AA_02_01",
                    "F102": "UD_AA_02_01",
                    "F101": "UD_AA_02_01",
                    "F100": "UD_AA_02_01",
                }
            },
        },
        "localtz": "UTC",
        "cmdr_meta": None,
        "etlsettings": {
            "boundary_end_cycle_in_shift": True,
            "down_fields": ["DOWN"],
            "modules": {
                "get_group_record_by_index": "GetGroupRecordByIndexMultiRecords",
                "update_machinestate": "UpdateMachineStateSticky",
                "group": "GroupByCounterNonCycle",
                "get_record_groups": "GetRecordGroup",
                "process_record": "ProcessRecordExplicitDowntime",
            },
        },
        "source_type": "AutoAssembly_BottomDryOven",
        "capturetime": "2017-07-12T20:59:52.642000Z",
        "tombstone_epoch": 0,
        "updatetime": "2017-07-12 20:59:52.643000",
        "source_type_clean": "Auto Assembly: Oven for Bottom Dry",
        "recipes": {
            "DEFAULT": {
                "cycle_finished_product_ratio": 0.5,
                "cycle_threshold": 300000,
                "cycle_ideal": 25600,
            }
        },
        "tombstone": False,
        "meta_assign": None,
        "capturetime_epoch": 1499893192642,
        "etlpluginmap": {
            "downtime_mod": "DowntimeAnalyzer",
            "cycle": "EventAnalyzer",
            "defect": "DefectAnalyzer",
            "multipart/form-data": "AssociateFileByCounterAnalyzer",
        },
    },
]

MACHINE_TYPE_FIELDS = [
    {"type": "float", "name": "stat__test_float", "title_prefix": "test float"},
    {"type": "string", "name": "stat__test_string", "title_prefix": "test string"},
    {
        "type": "string",
        "name": "stat__test_hidden",
        "title_prefix": "test hidden",
        "ui_hidden": True,
    },
]
