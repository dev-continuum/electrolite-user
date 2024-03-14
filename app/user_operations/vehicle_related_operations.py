from data_store import data_schemas
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations
from fastapi import status
from fastapi.exceptions import HTTPException
from utility.custom_logger import logger

vehicle_data = {
    "4 wheeler": {
        "Tata Motors": {
            "TATA TIGOR EV - XE": {
                "range": "140",
                "max_speed": "80",
                "electric_energy_consumption": "13.3",
                "battery_technology": "Lithium ion",
                "battery_capacity": "16.2",
                "battery_density": "121",
                "battery_cycle": "2000"
            },
            "TATA TIGOR EV - XM": {
                "range": "140",
                "max_speed": "80",
                "electric_energy_consumption": "13.3",
                "battery_technology": "Lithium ion",
                "battery_capacity": "16.2",
                "battery_density": "131.6",
                "battery_cycle": "2000"
            },
            "TATA TIGOR EV - XT": {
                "range": "140",
                "max_speed": "80",
                "electric_energy_consumption": "13.3",
                "battery_technology": "Lithium ion",
                "battery_capacity": "16.2",
                "battery_density": "131.6",
                "battery_cycle": "2000"
            },
            "TATA TIGOR EV - XE+": {
                "range": "213",
                "max_speed": "80",
                "electric_energy_consumption": "11.8",
                "battery_technology": "Lithium ion",
                "battery_capacity": "21.5",
                "battery_density": "121",
                "battery_cycle": "2000"
            },
            "TATA TIGOR EV - XM+": {
                "range": "213",
                "max_speed": "80",
                "electric_energy_consumption": "11.8",
                "battery_technology": "Lithium ion",
                "battery_capacity": "21.5",
                "battery_density": "121",
                "battery_cycle": "2000"
            },
            "TATA TIGOR EV - XT+": {
                "range": "213",
                "max_speed": "80",
                "electric_energy_consumption": "11.8",
                "battery_technology": "Lithium ion",
                "battery_capacity": "21.5",
                "battery_density": "121",
                "battery_cycle": "2000"
            },
            "TATA NEXON EV XM": {
                "range": "312",
                "max_speed": "80",
                "electric_energy_consumption": "10.6",
                "battery_technology": "Lithium Iron Phosphate LiFePO4",
                "battery_capacity": "30.2",
                "battery_density": "179",
                "battery_cycle": "1200"
            },
            "TATA NEXON EV XZ+": {
                "range": "312",
                "max_speed": "80",
                "electric_energy_consumption": "10.6",
                "battery_technology": "Lithium Iron Phosphate LiFePO4",
                "battery_capacity": "30.2",
                "battery_density": "179",
                "battery_cycle": "1200"
            },
            "TATA XPRES-T EV XE+": {
                "range": "213",
                "max_speed": "80.7",
                "electric_energy_consumption": "11.8",
                "battery_technology": "Lithium Iron",
                "battery_capacity": "21.5",
                "battery_density": "121",
                "battery_cycle": "2000"
            },
            "TATA XPRES-T EV XM+": {
                "range": "213",
                "max_speed": "80.7",
                "electric_energy_consumption": "11.8",
                "battery_technology": "Lithium Iron",
                "battery_capacity": "21.5",
                "battery_density": "121",
                "battery_cycle": "2000"
            },
            "TATA XPRES-T EV XT+": {
                "range": "213",
                "max_speed": "80.7",
                "electric_energy_consumption": "11.8",
                "battery_technology": "Lithium Iron",
                "battery_capacity": "21.5",
                "battery_density": "121",
                "battery_cycle": "2000"
            },
            "TATA NEXON EV XZ+ DK": {
                "range": "310",
                "max_speed": "78.2",
                "electric_energy_consumption": "12",
                "battery_technology": "Lithium Ion Iron Phosphate",
                "battery_capacity": "30.2",
                "battery_density": "179",
                "battery_cycle": "1200"
            },
            "Tata Tigor EV XZ+": {
                "range": "314",
                "max_speed": "116.5",
                "electric_energy_consumption": "11",
                "battery_technology": "Lithium Ion Iron Phosphate",
                "battery_capacity": "26.0",
                "battery_density": "179",
                "battery_cycle": "1200"
            },
            "Tata Tigor EV XE (26 kWh)": {
                "range": "314",
                "max_speed": "116.5",
                "electric_energy_consumption": "11",
                "battery_technology": "Lithium Ion Iron Phosphate",
                "battery_capacity": "26.00",
                "battery_density": "179",
                "battery_cycle": "1200"
            },
            "Tata Tigor EV XM (26 kWh)": {
                "range": "314",
                "max_speed": "116.5",
                "electric_energy_consumption": "11",
                "battery_technology": "Lithium Ion Iron Phosphate",
                "battery_capacity": "26.00",
                "battery_density": "179",
                "battery_cycle": "1200"
            },
            "TATA TIGOR XPRES-T EV XM": {
                "range": "314",
                "max_speed": "116.5",
                "electric_energy_consumption": "11",
                "battery_technology": "",
                "battery_capacity": "26.00",
                "battery_density": "179",
                "battery_cycle": "1200"
            }
        },
        "Mahindra and Mahindra": {
            "e-Verito C2": {
                "range": "143",
                "max_speed": "80",
                "electric_energy_consumption": "14.9",
                "battery_technology": "Lithium ion",
                "battery_capacity": "15.9",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "e-Verito C4": {
                "range": "143",
                "max_speed": "80",
                "electric_energy_consumption": "14.9",
                "battery_technology": "Lithium ion",
                "battery_capacity": "15.9",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "e-Verito C6": {
                "range": "143",
                "max_speed": "80",
                "electric_energy_consumption": "14.9",
                "battery_technology": "Lithium ion",
                "battery_capacity": "15.9",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "e-Verito D2": {
                "range": "181",
                "max_speed": "80",
                "electric_energy_consumption": "14.6",
                "battery_technology": "Lithium ion",
                "battery_capacity": "21.2",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "e-Verito D4": {
                "range": "181",
                "max_speed": "80",
                "electric_energy_consumption": "14.6",
                "battery_technology": "Lithium ion",
                "battery_capacity": "21.2",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "e-Verito D6": {
                "range": "181",
                "max_speed": "80",
                "electric_energy_consumption": "14.6",
                "battery_technology": "Lithium ion",
                "battery_capacity": "21.2",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Mahindra e-Supro Cargo Van": {
                "range": "134",
                "max_speed": "60",
                "electric_energy_consumption": "14.2",
                "battery_technology": "Lithium ion",
                "battery_capacity": "16.1",
                "battery_density": "81.6",
                "battery_cycle": "5000"
            },
            "Mahindra e-Supro Cargo Van VX": {
                "range": "134",
                "max_speed": "60",
                "electric_energy_consumption": "14.2",
                "battery_technology": "Lithium ion",
                "battery_capacity": "16.1",
                "battery_density": "81.6",
                "battery_cycle": "5000"
            },
            "Zor Grand PU": {
                "range": "148",
                "max_speed": "51",
                "electric_energy_consumption": "7.4",
                "battery_technology": "",
                "battery_capacity": "10.24",
                "battery_density": "162.4",
                "battery_cycle": "3000"
            },
            "Zor Grand DAC 1": {
                "range": "146",
                "max_speed": "51",
                "electric_energy_consumption": "8.2",
                "battery_technology": "",
                "battery_capacity": "10.24",
                "battery_density": "162.4",
                "battery_cycle": "3000"
            },
            "Zor Grand DAC 2": {
                "range": "146",
                "max_speed": "51",
                "electric_energy_consumption": "8.2",
                "battery_technology": "",
                "battery_capacity": "10.24",
                "battery_density": "162.4",
                "battery_cycle": "3000"
            }
        }
    },
    "3 wheeler": {
        "Mahindra Electric": {
            "Treo Yaari HRT": {
                "range": "129",
                "max_speed": "00",
                "electric_energy_consumption": "3.41",
                "battery_technology": "Lithium ion",
                "battery_capacity": "3.7",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo HRT": {
                "range": "171",
                "max_speed": "40",
                "electric_energy_consumption": "5.8",
                "battery_technology": "Lithium ion",
                "battery_capacity": "7.4",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo SFT": {
                "range": "171",
                "max_speed": "40",
                "electric_energy_consumption": "5.8",
                "battery_technology": "Lithium ion",
                "battery_capacity": "7.4",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Yaari SFT": {
                "range": "129",
                "max_speed": "00",
                "electric_energy_consumption": "3.41",
                "battery_technology": "Lithium ion",
                "battery_capacity": "3.7",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Zor": {
                "range": "125",
                "max_speed": "50.2",
                "electric_energy_consumption": "6.44",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "7.4",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Zor FB": {
                "range": "125",
                "max_speed": "50.2",
                "electric_energy_consumption": "6.44",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "7.4",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Zor DV": {
                "range": "118",
                "max_speed": "50.2",
                "electric_energy_consumption": "6.75",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "7.4",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Yaari Cargo HRT DV": {
                "range": "113",
                "max_speed": "0",
                "electric_energy_consumption": "4.5",
                "battery_technology": "",
                "battery_capacity": "3.70",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Yaari Cargo HRT FB": {
                "range": "116",
                "max_speed": "0",
                "electric_energy_consumption": "4.3",
                "battery_technology": "",
                "battery_capacity": "3.70",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Yaari Cargo HRT PU": {
                "range": "116",
                "max_speed": "0",
                "electric_energy_consumption": "4.3",
                "battery_technology": "",
                "battery_capacity": "3.70",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Yaari Cargo SFT DV": {
                "range": "113",
                "max_speed": "0",
                "electric_energy_consumption": "4.5",
                "battery_technology": "",
                "battery_capacity": "3.70",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Yaari Cargo SFT FB": {
                "range": "116",
                "max_speed": "0",
                "electric_energy_consumption": "4.3",
                "battery_technology": "",
                "battery_capacity": "3.70",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            },
            "Treo Yaari Cargo SFT PU": {
                "range": "116",
                "max_speed": "0",
                "electric_energy_consumption": "4.3",
                "battery_technology": "",
                "battery_capacity": "3.70",
                "battery_density": "129.2",
                "battery_cycle": "2000"
            }
        },
        "Kinetic Green": {
            "Kinetic SAFAR SMART LFP": {
                "range": "112",
                "max_speed": "0",
                "electric_energy_consumption": "5.65",
                "battery_technology": "Lithium ion",
                "battery_capacity": "3.7",
                "battery_density": "145.96",
                "battery_cycle": "2000"
            },
            "SAFAR SHAKTI LFP": {
                "range": "100",
                "max_speed": "0",
                "electric_energy_consumption": "7.9",
                "battery_technology": "Lithium ion",
                "battery_capacity": "4.1",
                "battery_density": "146",
                "battery_cycle": "1500"
            },
            "KINETIC SAFAR SMART": {
                "range": "126",
                "max_speed": "0",
                "electric_energy_consumption": "7.7",
                "battery_technology": "Lithium Iron Phosphate LiFe PO4",
                "battery_capacity": "4.1",
                "battery_density": "146",
                "battery_cycle": "1500"
            },
            "KINETIC SAFAR STAR - 400": {
                "range": "83.5",
                "max_speed": "42.6",
                "electric_energy_consumption": "9.83",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt)",
                "battery_capacity": "4.2",
                "battery_density": "188",
                "battery_cycle": "2000"
            },
            "KINETIC SAFAR JUMBO - PICKUP": {
                "range": "142",
                "max_speed": "45.4",
                "electric_energy_consumption": "8.3",
                "battery_technology": "Li ion battery (Lithium Iron Phosphate)",
                "battery_capacity": "8.2",
                "battery_density": "160",
                "battery_cycle": "2000"
            },
            "KINETIC SAFAR SMART-NEXT": {
                "range": "161",
                "max_speed": "25",
                "electric_energy_consumption": "4.3",
                "battery_technology": "",
                "battery_capacity": "5.40",
                "battery_density": "196",
                "battery_cycle": "2000"
            },
            "Kinetic SAFAR SMART-NEO": {
                "range": "126",
                "max_speed": "24.5",
                "electric_energy_consumption": "4.6",
                "battery_technology": "",
                "battery_capacity": "4.10",
                "battery_density": "196",
                "battery_cycle": "2000"
            },
            "ZING HSS": {
                "range": "125",
                "max_speed": "45.8",
                "electric_energy_consumption": "3.3",
                "battery_technology": "",
                "battery_capacity": "3.40",
                "battery_density": "199.5",
                "battery_cycle": "1000"
            }
        },
        "champion polyplast": {
            "SAARTHI SHAVAK E AUTO": {
                "range": "94.18",
                "max_speed": "40",
                "electric_energy_consumption": "6.23",
                "battery_technology": "Lithium ion",
                "battery_capacity": "6.6",
                "battery_density": "110",
                "battery_cycle": "2000"
            },
            "SAARTHI SHAVAK DLX E - AUTO": {
                "range": "94.18",
                "max_speed": "40",
                "electric_energy_consumption": "6.23",
                "battery_technology": "Lithium ion",
                "battery_capacity": "6.6",
                "battery_density": "110",
                "battery_cycle": "2000"
            },
            "SAARTHI F2": {
                "range": "105.70",
                "max_speed": "00",
                "electric_energy_consumption": "7.12",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "4.4",
                "battery_density": "76.05",
                "battery_cycle": "2000"
            },
            "SAARTHI F2 ( 5.1 KW )": {
                "range": "123",
                "max_speed": "40",
                "electric_energy_consumption": "3.09",
                "battery_technology": "",
                "battery_capacity": "5.10",
                "battery_density": "162.22",
                "battery_cycle": "5000"
            }
        },
        "Victory Electric": {
            "VICTORY VIKRANT": {
                "range": "136.46",
                "max_speed": "0.00",
                "electric_energy_consumption": "4.55",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "5.2",
                "battery_density": "131",
                "battery_cycle": "2000"
            },
            "VICTORY +": {
                "range": "136.46",
                "max_speed": "0.00",
                "electric_energy_consumption": "4.55",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "5.2",
                "battery_density": "131",
                "battery_cycle": "2000"
            },
            "VICTORY BHIM +": {
                "range": "136.46",
                "max_speed": "0.00",
                "electric_energy_consumption": "4.55",
                "battery_technology": "Lithium ion",
                "battery_capacity": "5.2",
                "battery_density": "131",
                "battery_cycle": "2000"
            },
            "VICTORY BHIM CLEANER +": {
                "range": "136.46",
                "max_speed": "0.00",
                "electric_energy_consumption": "4.55",
                "battery_technology": "Lithium ion",
                "battery_capacity": "5.2",
                "battery_density": "131",
                "battery_cycle": "2000"
            }
        },
        "Y C": {
            "YATRI SUPER": {
                "range": "113.2",
                "max_speed": "00",
                "electric_energy_consumption": "4.62",
                "battery_technology": "Nickel-Manganese-Cobalt",
                "battery_capacity": "4.3",
                "battery_density": "99.5",
                "battery_cycle": "2000"
            },
            "YATRI CART": {
                "range": "110.78",
                "max_speed": "00",
                "electric_energy_consumption": "4.79",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "99.5",
                "battery_cycle": "2000"
            },
            "YATRI SUPER(5.1kWh)": {
                "range": "120",
                "max_speed": "0.00",
                "electric_energy_consumption": "5.70",
                "battery_technology": "",
                "battery_capacity": "5.10",
                "battery_density": "145",
                "battery_cycle": "4000"
            }
        },
        "Best Way": {
            "ele ex": {
                "range": "126.81",
                "max_speed": "00",
                "electric_energy_consumption": "4.44",
                "battery_technology": "Lithium-Iron-Phosphate",
                "battery_capacity": "4.4",
                "battery_density": "76.05",
                "battery_cycle": "2000"
            },
            "ele ex cargo": {
                "range": "126.81",
                "max_speed": "00",
                "electric_energy_consumption": "4.44",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "4.3",
                "battery_density": "76.05",
                "battery_cycle": "2000"
            }
        },
        "Avon Cycles": {
            "GREENWAY HP DX": {
                "range": "91.72",
                "max_speed": "00",
                "electric_energy_consumption": "5.38",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "103.62",
                "battery_cycle": "2000"
            },
            "E-RICK 306 LI": {
                "range": "91.72",
                "max_speed": "00",
                "electric_energy_consumption": "5.38",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "103.62",
                "battery_cycle": "2000"
            }
        },
        "Goenka Electric": {
            "Prince Pro": {
                "range": "83.7",
                "max_speed": "17.6",
                "electric_energy_consumption": "4.46",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "3.7",
                "battery_density": "140",
                "battery_cycle": "1500"
            },
            "Prince Pro X": {
                "range": "109",
                "max_speed": "17.6",
                "electric_energy_consumption": "4.31",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.3",
                "battery_density": "132.41",
                "battery_cycle": "2000"
            },
            "Samrat Pro X": {
                "range": "131.29",
                "max_speed": "20.12",
                "electric_energy_consumption": "4.22",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.3",
                "battery_density": "132.41",
                "battery_cycle": "2000"
            }
        },
        "Energy Electric": {
            "Premium Udaan": {
                "range": "108.37",
                "max_speed": "0",
                "electric_energy_consumption": "5.37",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "4.4",
                "battery_density": "76.05",
                "battery_cycle": "2000"
            }
        },
        "Thukral Electric": {
            "THUKRAL Erl Li": {
                "range": "99.57",
                "max_speed": "00",
                "electric_energy_consumption": "4.21",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "3.5",
                "battery_density": "102",
                "battery_cycle": "2000"
            },
            "THUKRAL TM DLX Li": {
                "range": "101.79",
                "max_speed": "0",
                "electric_energy_consumption": "6.74",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "3.5",
                "battery_density": "102",
                "battery_cycle": "2000"
            }
        },
        "Saera Electric": {
            "Mayuri Star": {
                "range": "92.96",
                "max_speed": "0.00",
                "electric_energy_consumption": "6.39",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.0",
                "battery_density": "105",
                "battery_cycle": "1000"
            },
            "MAYURI DV": {
                "range": "82.74",
                "max_speed": "0",
                "electric_energy_consumption": "6.38",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "4.0",
                "battery_density": "105",
                "battery_cycle": "1000"
            },
            "MAYURI SMART": {
                "range": "102",
                "max_speed": "0",
                "electric_energy_consumption": "5.83",
                "battery_technology": "",
                "battery_capacity": "4.00",
                "battery_density": "105",
                "battery_cycle": "1000"
            },
            "MAYURI AUTO": {
                "range": "102",
                "max_speed": "0",
                "electric_energy_consumption": "5.83",
                "battery_technology": "",
                "battery_capacity": "4.00",
                "battery_density": "105",
                "battery_cycle": "1000"
            }
        },
        "U P": {
            "power Li-ion": {
                "range": "99.68",
                "max_speed": "0",
                "electric_energy_consumption": "5.00",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "103.62",
                "battery_cycle": "2000"
            },
            "Power Li-Ion DV": {
                "range": "99.68",
                "max_speed": "0",
                "electric_energy_consumption": "5.00",
                "battery_technology": "Lithium-Ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "103.62",
                "battery_cycle": "2000"
            },
            "Power Li-Ion FB": {
                "range": "99.68",
                "max_speed": "0",
                "electric_energy_consumption": "5.00",
                "battery_technology": "Lithium Iron phosphate",
                "battery_capacity": "4.4",
                "battery_density": "103.62",
                "battery_cycle": "2000"
            },
            "Power Li-Ion CV": {
                "range": "99.68",
                "max_speed": "0",
                "electric_energy_consumption": "5.00",
                "battery_technology": "Lithium Iron phosphate",
                "battery_capacity": "4.4",
                "battery_density": "103.62",
                "battery_cycle": "2000"
            },
            "Power Li-Ion Primus": {
                "range": "85",
                "max_speed": "00",
                "electric_energy_consumption": "6.48",
                "battery_technology": "",
                "battery_capacity": "4.40",
                "battery_density": "201.48",
                "battery_cycle": "2000"
            }
        },
        "Khalsa Agencies": {
            "Khalsa Grand": {
                "range": "120.13",
                "max_speed": "0",
                "electric_energy_consumption": "4.72",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "76.05",
                "battery_cycle": "2000"
            }
        },
        "Atul Auto": {
            "Atul Elite+": {
                "range": "116",
                "max_speed": "00",
                "electric_energy_consumption": "4.9",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "3.7",
                "battery_density": "145.96",
                "battery_cycle": "2000"
            },
            "Atul Elite+ Cargo": {
                "range": "118",
                "max_speed": "00",
                "electric_energy_consumption": "4.6",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "3.7",
                "battery_density": "145.96",
                "battery_cycle": "2000"
            }
        },
        "Altigreen Propulsion": {
            "NEEV": {
                "range": "117",
                "max_speed": "53.4",
                "electric_energy_consumption": "8.1",
                "battery_technology": "Lithium ion LiFeP04 (Lithium Iron phosphate)",
                "battery_capacity": "7.7",
                "battery_density": "145.96",
                "battery_cycle": "2000"
            },
            "NEEV HD": {
                "range": "151",
                "max_speed": "53.7",
                "electric_energy_consumption": "8.7",
                "battery_technology": "Li ion battery based on LiFePO4 (Lithium Ion Phosphate)",
                "battery_capacity": "11.1",
                "battery_density": "129.4",
                "battery_cycle": "2000"
            },
            "NEEV LR": {
                "range": "151",
                "max_speed": "53.7",
                "electric_energy_consumption": "8.7",
                "battery_technology": "Li ion battery based on LiFePO4 (Lithium Ion Phosphate)",
                "battery_capacity": "11.1",
                "battery_density": "129.4",
                "battery_cycle": "2000"
            },
            "NEEV HDx": {
                "range": "160",
                "max_speed": "54",
                "electric_energy_consumption": "8",
                "battery_technology": "Li ion battery based on LiFePO4",
                "battery_capacity": "11.0",
                "battery_density": "129.4",
                "battery_cycle": "2000"
            }
        },
        "Dilli Electric": {
            "CITYLIFE LI-PRIMA": {
                "range": "96.5",
                "max_speed": "23",
                "electric_energy_consumption": "4.1",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "76.05",
                "battery_cycle": "2000"
            },
            "CITYLIFE LI MAX": {
                "range": "131.91",
                "max_speed": "0",
                "electric_energy_consumption": "4.74",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "76.05",
                "battery_cycle": "2000"
            }
        },
        "Piaggio Vehicles": {
            "Ape' E-City": {
                "range": "102",
                "max_speed": "43.6",
                "electric_energy_consumption": "8.2",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt)",
                "battery_capacity": "4.2",
                "battery_density": "188",
                "battery_cycle": "2000"
            },
            "Ape' E-City FX": {
                "range": "159",
                "max_speed": "43",
                "electric_energy_consumption": "5.8",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt oxide)",
                "battery_capacity": "7.5",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "Ape E- Xtra FX PU": {
                "range": "142",
                "max_speed": "44.2",
                "electric_energy_consumption": "6.7",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt oxide)",
                "battery_capacity": "8.5",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "Ape E-Xtra FX With Platform": {
                "range": "142",
                "max_speed": "44.2",
                "electric_energy_consumption": "6.7",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt oxide)",
                "battery_capacity": "8.5",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "Ape E-Xtra LX With Platform": {
                "range": "87",
                "max_speed": "43.7",
                "electric_energy_consumption": "6.78",
                "battery_technology": "Nickel Manganese Cobalt Chemistry",
                "battery_capacity": "4.65",
                "battery_density": "188",
                "battery_cycle": "2000"
            },
            "Ape E- Xtra LX PU": {
                "range": "87",
                "max_speed": "43.7",
                "electric_energy_consumption": "6.78",
                "battery_technology": "Nickel Manganese Cobalt Chemistry",
                "battery_capacity": "4.7",
                "battery_density": "188",
                "battery_cycle": "2000"
            },
            "Ape E-Xtra LX DAC": {
                "range": "85",
                "max_speed": "43",
                "electric_energy_consumption": "5.9",
                "battery_technology": "Nickel Manganese Cobalt Chemistry",
                "battery_capacity": "4.7",
                "battery_density": "188",
                "battery_cycle": "2000"
            },
            "Ape E-Xtra FX DAC": {
                "range": "148",
                "max_speed": "45",
                "electric_energy_consumption": "6.17",
                "battery_technology": "Nickel Manganese Cobalt Chemistry",
                "battery_capacity": "8.5",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "Ape' E-Xtra EX With Platform": {
                "range": "134",
                "max_speed": "43.5",
                "electric_energy_consumption": "9.89",
                "battery_technology": "Li ion battery (Nickel Cobalt Aluminum)",
                "battery_capacity": "7.6",
                "battery_density": "267",
                "battery_cycle": "1000"
            },
            "Ape E- Xtra FX PU(8 KwH)": {
                "range": "141",
                "max_speed": "44.6",
                "electric_energy_consumption": "6.5",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "Ape E-Xtra FX With Platform (8 KWh)": {
                "range": "141",
                "max_speed": "44.6",
                "electric_energy_consumption": "6.5",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "Ape' E-Xtra FX DAC (8KWh)": {
                "range": "161",
                "max_speed": "44.6",
                "electric_energy_consumption": "6.7",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "Ape E- City FX NE": {
                "range": "131",
                "max_speed": "43.8",
                "electric_energy_consumption": "7.74",
                "battery_technology": "",
                "battery_capacity": "7.50",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "Ape E- Xtra FX NE PU": {
                "range": "159",
                "max_speed": "44.5",
                "electric_energy_consumption": "6.54",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "APE E-Xtra FX NE with Platform": {
                "range": "148",
                "max_speed": "44.5",
                "electric_energy_consumption": "6.36",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "APE E-Xtra FX NE DAC": {
                "range": "148",
                "max_speed": "44.5",
                "electric_energy_consumption": "6.36",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "Ape E- City FX NE MAX": {
                "range": "181",
                "max_speed": "41.6",
                "electric_energy_consumption": "5.17",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "APE E- XTRA FX NE MAX PU": {
                "range": "126",
                "max_speed": "41.1",
                "electric_energy_consumption": "6.4",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "APE E- XTRA FX NE MAX Platform": {
                "range": "126",
                "max_speed": "41.1",
                "electric_energy_consumption": "6.4",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "APE E- XTRA FX NE MAX DAC": {
                "range": "136",
                "max_speed": "41.1",
                "electric_energy_consumption": "6.4",
                "battery_technology": "",
                "battery_capacity": "8.00",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            }
        },
        "Speego Vehicles": {
            "SPEEGO DLX Li": {
                "range": "112.5",
                "max_speed": "00",
                "electric_energy_consumption": "4.80",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "76.05",
                "battery_cycle": "2000"
            }
        },
        "Shigan Evoltz": {
            "Bull Cart Super": {
                "range": "144.21",
                "max_speed": "40",
                "electric_energy_consumption": "5.09",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "9.6",
                "battery_density": "135",
                "battery_cycle": "3500"
            },
            "Green Cart Super": {
                "range": "120.56",
                "max_speed": "0",
                "electric_energy_consumption": "6.05",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "5.1",
                "battery_density": "133.33",
                "battery_cycle": "2000"
            },
            "Green Rick Super": {
                "range": "115.6",
                "max_speed": "0",
                "electric_energy_consumption": "5.83",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "5.1",
                "battery_density": "133.33",
                "battery_cycle": "2000"
            }
        },
        "Lohia Auto": {
            "NARAIN i": {
                "range": "112.91",
                "max_speed": "0",
                "electric_energy_consumption": "4.51",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "3.8",
                "battery_density": "98",
                "battery_cycle": "1000"
            },
            "NARAIN iCE": {
                "range": "112.91",
                "max_speed": "0",
                "electric_energy_consumption": "4.51",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "3.8",
                "battery_density": "98",
                "battery_cycle": "1000"
            },
            "Humsafar iB": {
                "range": "111",
                "max_speed": "40",
                "electric_energy_consumption": "8.53",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "7.6",
                "battery_density": "98",
                "battery_cycle": "1000"
            },
            "Narain Xi": {
                "range": "137",
                "max_speed": "0",
                "electric_energy_consumption": "4.45",
                "battery_technology": "",
                "battery_capacity": "4.40",
                "battery_density": "127.1",
                "battery_cycle": "2500"
            },
            "Narain XIU": {
                "range": "137",
                "max_speed": "0",
                "electric_energy_consumption": "4.45",
                "battery_technology": "",
                "battery_capacity": "4.40",
                "battery_density": "127.1",
                "battery_cycle": "2500"
            }
        },
        "Omega Seiki": {
            "RAGE+": {
                "range": "89.32",
                "max_speed": "40",
                "electric_energy_consumption": "8.34",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "7.5",
                "battery_density": "98",
                "battery_cycle": "1000"
            },
            "RAGE+ 125": {
                "range": "151",
                "max_speed": "45",
                "electric_energy_consumption": "8.53",
                "battery_technology": "",
                "battery_capacity": "10.80",
                "battery_density": "169.69",
                "battery_cycle": "3500"
            },
            "RAGE+ SWAP": {
                "range": "89",
                "max_speed": "40",
                "electric_energy_consumption": "7.45",
                "battery_technology": "",
                "battery_capacity": "4.70",
                "battery_density": "188",
                "battery_cycle": "2000"
            },
            "RAGE+ A85": {
                "range": "115",
                "max_speed": "40",
                "electric_energy_consumption": "9.01",
                "battery_technology": "",
                "battery_capacity": "8.50",
                "battery_density": "168.75",
                "battery_cycle": "2000"
            },
            "RAGE+ RAPID": {
                "range": "88",
                "max_speed": "40",
                "electric_energy_consumption": "9.43",
                "battery_technology": "",
                "battery_capacity": "5.80",
                "battery_density": "74.79",
                "battery_cycle": "10000"
            }
        },
        "Keto Motors": {
            "BULKe plus 2.0": {
                "range": "187.69",
                "max_speed": "40",
                "electric_energy_consumption": "7.16",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "12.6",
                "battery_density": "134.73",
                "battery_cycle": "1500"
            },
            "BULKe": {
                "range": "187.69",
                "max_speed": "40",
                "electric_energy_consumption": "7.17",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "12.6",
                "battery_density": "134.73",
                "battery_cycle": "1500"
            },
            "BULKe Plus 2.1": {
                "range": "148.1",
                "max_speed": "40",
                "electric_energy_consumption": "8.66",
                "battery_technology": "Lithium Ion (Lithium Ferro Phosphate)",
                "battery_capacity": "9.8",
                "battery_density": "140",
                "battery_cycle": "1500"
            },
            "BULKe 1.0": {
                "range": "148.1",
                "max_speed": "40",
                "electric_energy_consumption": "8.66",
                "battery_technology": "Lithium Ferro Phosphate",
                "battery_capacity": "9.8",
                "battery_density": "140",
                "battery_cycle": "1500"
            },
            "TriLux": {
                "range": "148.1",
                "max_speed": "40",
                "electric_energy_consumption": "8.66",
                "battery_technology": "Lithium Ion (Lithium Ferro Phosphate)",
                "battery_capacity": "9.8",
                "battery_density": "140",
                "battery_cycle": "1500"
            },
            "TriLux 1.0": {
                "range": "88",
                "max_speed": "45",
                "electric_energy_consumption": "6.98",
                "battery_technology": "",
                "battery_capacity": "7.80",
                "battery_density": "194.42",
                "battery_cycle": "4000"
            },
            "BULKe Plus 2.2": {
                "range": "88",
                "max_speed": "45",
                "electric_energy_consumption": "6.98",
                "battery_technology": "",
                "battery_capacity": "7.80",
                "battery_density": "194.42",
                "battery_cycle": "4000"
            }
        },
        "Grd Motors": {
            "DAVRATH EXPRESS": {
                "range": "111.60",
                "max_speed": "0",
                "electric_energy_consumption": "6.99",
                "battery_technology": "Lithium-Ion (Lithium Iron phosphate)",
                "battery_capacity": "4.4",
                "battery_density": "76.05",
                "battery_cycle": "2000"
            }
        },
        "Etrio Automobiles": {
            "Touro Max Loader": {
                "range": "114.4",
                "max_speed": "40",
                "electric_energy_consumption": "9.54",
                "battery_technology": "Lithium Iron phosphate",
                "battery_capacity": "7.7",
                "battery_density": "123",
                "battery_cycle": "3000"
            },
            "Touro Mini loader": {
                "range": "105",
                "max_speed": "0",
                "electric_energy_consumption": "4.83",
                "battery_technology": "Lithium Ferro Phosphate",
                "battery_capacity": "3.83",
                "battery_density": "123",
                "battery_cycle": "3000"
            },
            "Touro Mini Passenger": {
                "range": "105",
                "max_speed": "0",
                "electric_energy_consumption": "4.83",
                "battery_technology": "Lithium Ferro Phosphate",
                "battery_capacity": "3.83",
                "battery_density": "123",
                "battery_cycle": "3000"
            },
            "Touro Max+ Flat": {
                "range": "127",
                "max_speed": "40",
                "electric_energy_consumption": "7.94",
                "battery_technology": "",
                "battery_capacity": "10.20",
                "battery_density": "142.22",
                "battery_cycle": "2500"
            },
            "Touro Max+ Loader": {
                "range": "127",
                "max_speed": "40",
                "electric_energy_consumption": "7.94",
                "battery_technology": "",
                "battery_capacity": "10.20",
                "battery_density": "142.22",
                "battery_cycle": "2500"
            },
            "Touro Max+ Delivery": {
                "range": "127",
                "max_speed": "40",
                "electric_energy_consumption": "7.94",
                "battery_technology": "",
                "battery_capacity": "10.20",
                "battery_density": "142.22",
                "battery_cycle": "2500"
            }
        },
        "Om Balajee": {
            "e VIKAS": {
                "range": "102.96",
                "max_speed": "40",
                "electric_energy_consumption": "9.87",
                "battery_technology": "Lithium-Ion (Lithium Ferro phosphate)",
                "battery_capacity": "9.6",
                "battery_density": "116",
                "battery_cycle": "1500"
            },
            "e VIKAS FERRI": {
                "range": "102.96",
                "max_speed": "40",
                "electric_energy_consumption": "9.87",
                "battery_technology": "Lithium Ferro Phosphate",
                "battery_capacity": "9.6",
                "battery_density": "116",
                "battery_cycle": "1500"
            }
        },
        "Scooters India": {
            "VIKRAM Vidyut Passenger Carrier(6P+1D)": {
                "range": "168.7",
                "max_speed": "40",
                "electric_energy_consumption": "6.29",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "16.2",
                "battery_density": "135",
                "battery_cycle": "2000"
            }
        },
        "Mlr Auto": {
            "TEJA HANDY CARGO NORMAL DECK EV": {
                "range": "133",
                "max_speed": "46.2",
                "electric_energy_consumption": "6.34",
                "battery_technology": "LIFe PO4(Lithium Iron phosphate)",
                "battery_capacity": "7.5",
                "battery_density": "146",
                "battery_cycle": "2000"
            },
            "ePRO CARGO": {
                "range": "119",
                "max_speed": "49.8",
                "electric_energy_consumption": "7.3",
                "battery_technology": "",
                "battery_capacity": "8.50",
                "battery_density": "168",
                "battery_cycle": "1000"
            },
            "ePRO CITY": {
                "range": "144",
                "max_speed": "49.8",
                "electric_energy_consumption": "9.8",
                "battery_technology": "",
                "battery_capacity": "8.50",
                "battery_density": "168",
                "battery_cycle": "1000"
            }
        },
        "Continental Engines": {
            "Baxy Cargo Super King-EV": {
                "range": "115",
                "max_speed": "51.3",
                "electric_energy_consumption": "7.0",
                "battery_technology": "Nickel Manganese Cobalt",
                "battery_capacity": "7.50",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            },
            "BAXY  PRO": {
                "range": "134",
                "max_speed": "51",
                "electric_energy_consumption": "8.6",
                "battery_technology": "",
                "battery_capacity": "8.50",
                "battery_density": "168.7",
                "battery_cycle": "1000"
            }
        },
        "Euler Motors": {
            "HiLoad DV": {
                "range": "150",
                "max_speed": "43.5",
                "electric_energy_consumption": "7.7",
                "battery_technology": "Nickel Cobalt Aluminum",
                "battery_capacity": "11.5",
                "battery_density": "141.66",
                "battery_cycle": "2000"
            },
            "HiLoad PV": {
                "range": "129",
                "max_speed": "43.5",
                "electric_energy_consumption": "9.6",
                "battery_technology": "Nickel Cobalt Aluminum",
                "battery_capacity": "11.5",
                "battery_density": "141.66",
                "battery_cycle": "2000"
            }
        },
        "Sks Trade": {
            "ARZOO LI": {
                "range": "101.6",
                "max_speed": "0",
                "electric_energy_consumption": "6.22",
                "battery_technology": "Lithium Ferro Phosphate",
                "battery_capacity": "4.4",
                "battery_density": "98",
                "battery_cycle": "2000"
            },
            "ARZOO EC-LI": {
                "range": "123",
                "max_speed": "0",
                "electric_energy_consumption": "4.35",
                "battery_technology": "Lithium Ferro Phosphate",
                "battery_capacity": "4.4",
                "battery_density": "98",
                "battery_cycle": "2000"
            }
        },
        "J.s. Auto": {
            "JSA E-RICKSHAW LI": {
                "range": "115",
                "max_speed": "00",
                "electric_energy_consumption": "5.67",
                "battery_technology": "Lithium Iron Phosphate",
                "battery_capacity": "4.10",
                "battery_density": "152.4",
                "battery_cycle": "3500"
            }
        },
        "Balan Engineering": {
            "SWACHH RATH": {
                "range": "143",
                "max_speed": "0",
                "electric_energy_consumption": "4.32",
                "battery_technology": "Lithium Ion Ferrophosphate",
                "battery_capacity": "5.10",
                "battery_density": "160",
                "battery_cycle": "2000"
            },
            "B5": {
                "range": "143",
                "max_speed": "0",
                "electric_energy_consumption": "4.32",
                "battery_technology": "",
                "battery_capacity": "5.10",
                "battery_density": "160",
                "battery_cycle": "2000"
            },
            "VISHWAS": {
                "range": "143",
                "max_speed": "0",
                "electric_energy_consumption": "4.32",
                "battery_technology": "",
                "battery_capacity": "5.10",
                "battery_density": "160",
                "battery_cycle": "2000"
            }
        },
        "Smartomatic Vehicles": {
            "SMART +": {
                "range": "124",
                "max_speed": "0",
                "electric_energy_consumption": "5.04",
                "battery_technology": "",
                "battery_capacity": "4.90",
                "battery_density": "136",
                "battery_cycle": "3000"
            },
            "SMART CARGO": {
                "range": "124",
                "max_speed": "0",
                "electric_energy_consumption": "5.04",
                "battery_technology": "",
                "battery_capacity": "4.90",
                "battery_density": "136",
                "battery_cycle": "3000"
            }
        },
        "Efev Charging": {
            "Muver": {
                "range": "103",
                "max_speed": "0",
                "electric_energy_consumption": "5.7",
                "battery_technology": "",
                "battery_capacity": "5.30",
                "battery_density": "157.5",
                "battery_cycle": "2000"
            },
            "HAULER": {
                "range": "103",
                "max_speed": "0.0",
                "electric_energy_consumption": "5.73",
                "battery_technology": "",
                "battery_capacity": "5.30",
                "battery_density": "157.5",
                "battery_cycle": "2000"
            }
        },
        "Fitwel Mobility": {
            "JOVY": {
                "range": "154",
                "max_speed": "40",
                "electric_energy_consumption": "5.12",
                "battery_technology": "",
                "battery_capacity": "5.10",
                "battery_density": "160",
                "battery_cycle": "2000"
            },
            "APIS": {
                "range": "154",
                "max_speed": "40",
                "electric_energy_consumption": "5.12",
                "battery_technology": "",
                "battery_capacity": "5.10",
                "battery_density": "160",
                "battery_cycle": "2000"
            }
        },
        "Green Evolve": {
            "EVAUM": {
                "range": "117",
                "max_speed": "40",
                "electric_energy_consumption": "6.76",
                "battery_technology": "",
                "battery_capacity": "10.20",
                "battery_density": "142.22",
                "battery_cycle": "5000"
            }
        },
        "Ti Clean": {
            "MONTRA ELECTRIC ePV": {
                "range": "152",
                "max_speed": "45.7",
                "electric_energy_consumption": "7.47",
                "battery_technology": "",
                "battery_capacity": "7.50",
                "battery_density": "248",
                "battery_cycle": "2000"
            },
            "Montra Electric ePV 2.0": {
                "range": "197",
                "max_speed": "45.7",
                "electric_energy_consumption": "7.12",
                "battery_technology": "",
                "battery_capacity": "9.50",
                "battery_density": "248",
                "battery_cycle": "2000"
            },
            "MONTRA ELECTRIC ePX 2.0": {
                "range": "197",
                "max_speed": "45.7",
                "electric_energy_consumption": "7.12",
                "battery_technology": "",
                "battery_capacity": "9.50",
                "battery_density": "248",
                "battery_cycle": "2000"
            }
        }
    },
    "2 wheeler": {
        "Ather Energy": {
            "ATHER 450": {
                "range": "105",
                "max_speed": "57.7",
                "electric_energy_consumption": "6.38",
                "battery_technology": "Lithium ion",
                "battery_capacity": "2.7",
                "battery_density": "260.4",
                "battery_cycle": "1000"
            },
            "Ather450": {
                "range": "105",
                "max_speed": "48",
                "electric_energy_consumption": "6.22",
                "battery_technology": "Lithium ion",
                "battery_capacity": "2.7",
                "battery_density": "260.4",
                "battery_cycle": "1000"
            },
            "Ather 450 X": {
                "range": "117",
                "max_speed": "78.3",
                "electric_energy_consumption": "4.1",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt)",
                "battery_capacity": "2.9",
                "battery_density": "260",
                "battery_cycle": "1000"
            },
            "Ather 450X": {
                "range": "146",
                "max_speed": "79.3",
                "electric_energy_consumption": "4.0",
                "battery_technology": "",
                "battery_capacity": "3.70",
                "battery_density": "260",
                "battery_cycle": "1000"
            }
        },
        "Greaves Electric": {
            "ZEAL": {
                "range": "108",
                "max_speed": "41.6",
                "electric_energy_consumption": "2.26",
                "battery_technology": "LI ion NCM",
                "battery_capacity": "1.8",
                "battery_density": "168",
                "battery_cycle": "1000"
            },
            "Magnus": {
                "range": "90",
                "max_speed": "48",
                "electric_energy_consumption": "2.5",
                "battery_technology": "Lithium ion",
                "battery_capacity": "1.8",
                "battery_density": "168",
                "battery_cycle": "1000"
            },
            "Zeal VX1": {
                "range": "84",
                "max_speed": "41.6",
                "electric_energy_consumption": "2.47",
                "battery_technology": "Lithium ion",
                "battery_capacity": "1.96",
                "battery_density": "266",
                "battery_cycle": "1000"
            },
            "ZEAL-CA": {
                "range": "90",
                "max_speed": "42",
                "electric_energy_consumption": "2.52",
                "battery_technology": "Lithium Nickel Manganese Cobalt Oxide",
                "battery_capacity": "1.8",
                "battery_density": "168",
                "battery_cycle": "1000"
            },
            "ZEAL EX": {
                "range": "124",
                "max_speed": "44.3",
                "electric_energy_consumption": "2.60",
                "battery_technology": "Lithium Nickel Manganese Cobalt Oxide",
                "battery_capacity": "2.3",
                "battery_density": "191",
                "battery_cycle": "1000"
            },
            "MAGNUS EX": {
                "range": "120",
                "max_speed": "46.4",
                "electric_energy_consumption": "2.70",
                "battery_technology": "Lithium Nickel Manganese Cobalt oxide",
                "battery_capacity": "2.3",
                "battery_density": "191",
                "battery_cycle": "1000"
            },
            "ZEAL CA EX": {
                "range": "94",
                "max_speed": "44.3",
                "electric_energy_consumption": "3",
                "battery_technology": "Lithium Nickel Manganese Cobalt oxide",
                "battery_capacity": "2.30",
                "battery_density": "191",
                "battery_cycle": "1000"
            }
        },
        "Okinawa Autotech": {
            "RIDGE+": {
                "range": "84",
                "max_speed": "41",
                "electric_energy_consumption": "3.6",
                "battery_technology": "Lithium ion",
                "battery_capacity": "1.7",
                "battery_density": "172.3",
                "battery_cycle": "2000"
            },
            "iPRAISE": {
                "range": "159",
                "max_speed": "48.4",
                "electric_energy_consumption": "3.5",
                "battery_technology": "Lithium ion",
                "battery_capacity": "2.6",
                "battery_density": "195.3",
                "battery_cycle": "1100"
            },
            "Praise Pro": {
                "range": "88",
                "max_speed": "52",
                "electric_energy_consumption": "2.75",
                "battery_technology": "Lithium ion",
                "battery_capacity": "1.9",
                "battery_density": "217.5",
                "battery_cycle": "1000"
            },
            "iPRAISE+": {
                "range": "139",
                "max_speed": "51.2",
                "electric_energy_consumption": "2.72",
                "battery_technology": "Lithium ion",
                "battery_capacity": "3.3",
                "battery_density": "217.5",
                "battery_cycle": "1000"
            },
            "OKHI 90": {
                "range": "159",
                "max_speed": "74.2",
                "electric_energy_consumption": "3.1",
                "battery_technology": "",
                "battery_capacity": "3.60",
                "battery_density": "202",
                "battery_cycle": "1000"
            },
            "DUAL 100": {
                "range": "129",
                "max_speed": "54",
                "electric_energy_consumption": "2.8",
                "battery_technology": "",
                "battery_capacity": "3.10",
                "battery_density": "224",
                "battery_cycle": "1000"
            },
            "PRAISEE PRO": {
                "range": "86",
                "max_speed": "49.2",
                "electric_energy_consumption": "3.3",
                "battery_technology": "",
                "battery_capacity": "2.20",
                "battery_density": "207",
                "battery_cycle": "1000"
            },
            "RIDGE 100": {
                "range": "149",
                "max_speed": "50",
                "electric_energy_consumption": "2.4",
                "battery_technology": "",
                "battery_capacity": "3.10",
                "battery_density": "224",
                "battery_cycle": "1000"
            },
            "iPRAISE+ (Battery capacity 3.6 kWh)": {
                "range": "137",
                "max_speed": "49.6",
                "electric_energy_consumption": "3.1",
                "battery_technology": "",
                "battery_capacity": "3.60",
                "battery_density": "236",
                "battery_cycle": "2000"
            },
            "PRAISE PRO (Battery Capacity 2.1 kWh)": {
                "range": "81",
                "max_speed": "50.2",
                "electric_energy_consumption": "3.2",
                "battery_technology": "",
                "battery_capacity": "2.10",
                "battery_density": "224",
                "battery_cycle": "1000"
            }
        },
        "Jitendra New": {
            "JMT1000HS": {
                "range": "90.38",
                "max_speed": "40",
                "electric_energy_consumption": "2.89",
                "battery_technology": "Nickel-Manganese-Cobalt",
                "battery_capacity": "2.0",
                "battery_density": "201.1",
                "battery_cycle": "1500"
            },
            "JMT 1000 HS CARGO": {
                "range": "88.33",
                "max_speed": "51.93",
                "electric_energy_consumption": "2.77",
                "battery_technology": "Lithium Ion battery (Nickel Manganese Cobalt)",
                "battery_capacity": "2.0",
                "battery_density": "201.1",
                "battery_cycle": "1500"
            },
            "JMT 1000 48V": {
                "range": "83",
                "max_speed": "40",
                "electric_energy_consumption": "3.34",
                "battery_technology": "Lithium Iron NMC",
                "battery_capacity": "2.2",
                "battery_density": "220",
                "battery_cycle": "3000"
            },
            "DREAM 1.2PV": {
                "range": "97.8",
                "max_speed": "0",
                "electric_energy_consumption": "5.9",
                "battery_technology": "Lithium Iron phosphate",
                "battery_capacity": "4.3",
                "battery_density": "143",
                "battery_cycle": "2000"
            },
            "DREAM 1.2CV": {
                "range": "97.8",
                "max_speed": "0",
                "electric_energy_consumption": "5.9",
                "battery_technology": "Lithium Iron phosphate",
                "battery_capacity": "4.3",
                "battery_density": "143",
                "battery_cycle": "2000"
            },
            "DREAM 1.2DV": {
                "range": "97.8",
                "max_speed": "0",
                "electric_energy_consumption": "5.9",
                "battery_technology": "Lithium Iron phosphate",
                "battery_capacity": "4.3",
                "battery_density": "143",
                "battery_cycle": "2000"
            },
            "JMT 1000 HS PLUS": {
                "range": "156",
                "max_speed": "42",
                "electric_energy_consumption": "3.23",
                "battery_technology": "Lithium-Ion",
                "battery_capacity": "4.04",
                "battery_density": "200",
                "battery_cycle": "1001"
            },
            "JMT 1000 3K": {
                "range": "117",
                "max_speed": "40",
                "electric_energy_consumption": "3.20",
                "battery_technology": "Lithium-Ion",
                "battery_capacity": "3.20",
                "battery_density": "200",
                "battery_cycle": "1001"
            }
        },
        "Hero Electric": {
            "Photon LP": {
                "range": "91",
                "max_speed": "51",
                "electric_energy_consumption": "2.53",
                "battery_technology": "Lithium ion",
                "battery_capacity": "1.7",
                "battery_density": "217.5",
                "battery_cycle": "1100"
            },
            "NYX HS 500 ER": {
                "range": "127",
                "max_speed": "45",
                "electric_energy_consumption": "3.01",
                "battery_technology": "Lithium ion",
                "battery_capacity": "3.07",
                "battery_density": "168",
                "battery_cycle": "1000"
            },
            "OPTIMA HS 500 ER": {
                "range": "113",
                "max_speed": "47",
                "electric_energy_consumption": "3.10",
                "battery_technology": "Lithium ion",
                "battery_capacity": "3.07",
                "battery_density": "168",
                "battery_cycle": "1000"
            },
            "OPTIMA PRO": {
                "range": "95",
                "max_speed": "49.5",
                "electric_energy_consumption": "3.13",
                "battery_technology": "Li ion battery (Lithium Nickel Manganese Cobalt oxide)",
                "battery_capacity": "2.02",
                "battery_density": "193",
                "battery_cycle": "1000"
            },
            "NYX Pro": {
                "range": "94",
                "max_speed": "48.1",
                "electric_energy_consumption": "2.9",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "2.15",
                "battery_density": "193",
                "battery_cycle": "1100"
            },
            "OPTIMA e5": {
                "range": "82",
                "max_speed": "47.6",
                "electric_energy_consumption": "3.25",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "1.54",
                "battery_density": "156",
                "battery_cycle": "1000"
            },
            "NYX HX": {
                "range": "212",
                "max_speed": "43.1",
                "electric_energy_consumption": "3.58",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "4.6",
                "battery_density": "156",
                "battery_cycle": "1000"
            },
            "NYX e5": {
                "range": "82",
                "max_speed": "44.3",
                "electric_energy_consumption": "3.18",
                "battery_technology": "Lithium ion (Lithium Iron phosphate)",
                "battery_capacity": "1.54",
                "battery_density": "156",
                "battery_cycle": "1000"
            },
            "N61a": {
                "range": "92",
                "max_speed": "45",
                "electric_energy_consumption": "2.95",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt)",
                "battery_capacity": "2.17",
                "battery_density": "223",
                "battery_cycle": "1000"
            },
            "NYX N23a": {
                "range": "92",
                "max_speed": "47",
                "electric_energy_consumption": "3.1",
                "battery_technology": "Li ion battery (Nickel Cobalt Aluminum)",
                "battery_capacity": "1.9",
                "battery_density": "211",
                "battery_cycle": "1000"
            },
            "OPTIMA PRO 2.02 kwh": {
                "range": "98",
                "max_speed": "46.3",
                "electric_energy_consumption": "3.0",
                "battery_technology": "Nickel Manganese Cobalt",
                "battery_capacity": "2.02",
                "battery_density": "183",
                "battery_cycle": "1000"
            },
            "Optima CX": {
                "range": "82",
                "max_speed": "41.6",
                "electric_energy_consumption": "3.2",
                "battery_technology": "",
                "battery_capacity": "1.60",
                "battery_density": "156",
                "battery_cycle": "2000"
            },
            "Optima CX er": {
                "range": "140",
                "max_speed": "41.8",
                "electric_energy_consumption": "3.0",
                "battery_technology": "",
                "battery_capacity": "3.20",
                "battery_density": "156",
                "battery_cycle": "2000"
            },
            "NYX N51a": {
                "range": "82",
                "max_speed": "45.0",
                "electric_energy_consumption": "3.0",
                "battery_technology": "",
                "battery_capacity": "1.60",
                "battery_density": "188",
                "battery_cycle": "1000"
            },
            "Nyx CX": {
                "range": "81",
                "max_speed": "45",
                "electric_energy_consumption": "2.8",
                "battery_technology": "",
                "battery_capacity": "1.60",
                "battery_density": "156",
                "battery_cycle": "2000"
            },
            "Nyx CX er": {
                "range": "130",
                "max_speed": "45",
                "electric_energy_consumption": "3.1",
                "battery_technology": "",
                "battery_capacity": "3.20",
                "battery_density": "156",
                "battery_cycle": "2000"
            }
        },
        "Revolt Intellicorp": {
            "RV300": {
                "range": "102",
                "max_speed": "62.2",
                "electric_energy_consumption": "3.09",
                "battery_technology": "Lithium ion",
                "battery_capacity": "2.7",
                "battery_density": "222",
                "battery_cycle": "1000"
            },
            "RV400": {
                "range": "147",
                "max_speed": "40.8",
                "electric_energy_consumption": "2.59",
                "battery_technology": "Lithium ion",
                "battery_capacity": "3.2",
                "battery_density": "222",
                "battery_cycle": "1000"
            }
        },
        "Li-ions Elektrik": {
            "SPOCK": {
                "range": "107.38",
                "max_speed": "40",
                "electric_energy_consumption": "4.03",
                "battery_technology": "Lithium ion",
                "battery_capacity": "2.9",
                "battery_density": "213",
                "battery_cycle": "1500"
            }
        },
        "Tvs Motor": {
            "TVS iQUBE ELECTRIC": {
                "range": "86.1",
                "max_speed": "40",
                "electric_energy_consumption": "5.15",
                "battery_technology": "Nickel Manganese Cobalt",
                "battery_capacity": "2.25",
                "battery_density": "94.5",
                "battery_cycle": "1000"
            },
            "TVS iQUBE ELECTRIC SMARTXONNECT": {
                "range": "115",
                "max_speed": "40",
                "electric_energy_consumption": "4.62",
                "battery_technology": "",
                "battery_capacity": "3.40",
                "battery_density": "146",
                "battery_cycle": "1000"
            },
            "TVS iQUBE ELECTRIC S": {
                "range": "113",
                "max_speed": "40",
                "electric_energy_consumption": "5.29",
                "battery_technology": "",
                "battery_capacity": "3.40",
                "battery_density": "146",
                "battery_cycle": "1000"
            }
        },
        "Benling India": {
            "Aura": {
                "range": "82.11",
                "max_speed": "40",
                "electric_energy_consumption": "2.54",
                "battery_technology": "Nickel Manganese Cobalt",
                "battery_capacity": "2.9",
                "battery_density": "170",
                "battery_cycle": "1500"
            },
            "Aura LI": {
                "range": "119",
                "max_speed": "48",
                "electric_energy_consumption": "3.9",
                "battery_technology": "",
                "battery_capacity": "3.20",
                "battery_density": "199.5",
                "battery_cycle": "1000"
            },
            "BELIEVE": {
                "range": "119",
                "max_speed": "48",
                "electric_energy_consumption": "3.9",
                "battery_technology": "",
                "battery_capacity": "3.20",
                "battery_density": "224",
                "battery_cycle": "1000"
            }
        },
        "Tunwal E-motors": {
            "T 133": {
                "range": "99",
                "max_speed": "44.9",
                "electric_energy_consumption": "2.60",
                "battery_technology": "Li ion battery (Lithium Nickel Manganese Cobalt oxide)",
                "battery_capacity": "2.4",
                "battery_density": "180",
                "battery_cycle": "1200"
            },
            "Storm ZX Plus": {
                "range": "99",
                "max_speed": "44.9",
                "electric_energy_consumption": "2.6",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt oxide)",
                "battery_capacity": "2.4",
                "battery_density": "180",
                "battery_cycle": "1000"
            },
            "TEM G33": {
                "range": "99",
                "max_speed": "44.9",
                "electric_energy_consumption": "2.6",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt oxide)",
                "battery_capacity": "2.4",
                "battery_density": "180",
                "battery_cycle": "1000"
            },
            "RomaS": {
                "range": "99",
                "max_speed": "44.9",
                "electric_energy_consumption": "2.6",
                "battery_technology": "Li ion battery (Nickel Manganese Cobalt oxide)",
                "battery_capacity": "2.4",
                "battery_density": "180",
                "battery_cycle": "1000"
            },
            "TZ 3.3": {
                "range": "107",
                "max_speed": "56.7",
                "electric_energy_consumption": "3.55",
                "battery_technology": "NMC (Nickel Manganese Cobalt)",
                "battery_capacity": "2.9",
                "battery_density": "199.5",
                "battery_cycle": "1000"
            }
        },
        "Bajaj Auto": {
            "CHETAK 2403 Premium": {
                "range": "154",
                "max_speed": "61.1",
                "electric_energy_consumption": "2.8",
                "battery_technology": "Lithium Nickel Cobalt Aluminum oxide",
                "battery_capacity": "3.0",
                "battery_density": "240",
                "battery_cycle": "1000"
            },
            "CHETAK 2403 Urbane": {
                "range": "154",
                "max_speed": "61.1",
                "electric_energy_consumption": "2.8",
                "battery_technology": "Lithium Nickel Cobalt Aluminum oxide",
                "battery_capacity": "3.0",
                "battery_density": "240",
                "battery_cycle": "1000"
            },
            "Chetak 2413 Premium": {
                "range": "108",
                "max_speed": "61.7",
                "electric_energy_consumption": "3.1",
                "battery_technology": "Lithium Nickel Cobalt Aluminum oxide",
                "battery_capacity": "2.9",
                "battery_density": "231",
                "battery_cycle": "1000"
            }
        },
        "Kabira Mobility": {
            "Intercity 300": {
                "range": "134",
                "max_speed": "58.4",
                "electric_energy_consumption": "2.7",
                "battery_technology": "Nickel Manganese Cobalt",
                "battery_capacity": "2.82",
                "battery_density": "224",
                "battery_cycle": "1000"
            },
            "Intercity 350": {
                "range": "134",
                "max_speed": "52.4",
                "electric_energy_consumption": "2.7",
                "battery_technology": "Nickel Manganese Cobalt",
                "battery_capacity": "2.82",
                "battery_density": "224",
                "battery_cycle": "1000"
            },
            "Hermes 75": {
                "range": "122",
                "max_speed": "52",
                "electric_energy_consumption": "2.9",
                "battery_technology": "Nickel Manganese Cobalt",
                "battery_capacity": "2.82",
                "battery_density": "224",
                "battery_cycle": "1000"
            },
            "KM 3000": {
                "range": "95",
                "max_speed": "65",
                "electric_energy_consumption": "2.7",
                "battery_technology": "",
                "battery_capacity": "2.80",
                "battery_density": "224",
                "battery_cycle": "1000"
            },
            "KM 4000": {
                "range": "95",
                "max_speed": "75.4",
                "electric_energy_consumption": "2.7",
                "battery_technology": "",
                "battery_capacity": "2.80",
                "battery_density": "224",
                "battery_cycle": "1000"
            }
        },
        "Microcon I2i": {
            "Anav12": {
                "range": "81.98",
                "max_speed": "40",
                "electric_energy_consumption": "3.46",
                "battery_technology": "Lithium Ion",
                "battery_capacity": "2.0",
                "battery_density": "221",
                "battery_cycle": "1000"
            }
        },
        "Ola Electric": {
            "Ola S1 (E2W-AC-04)": {
                "range": "141",
                "max_speed": "75.3",
                "electric_energy_consumption": "3.3",
                "battery_technology": "Nickel Manganese Cobalt Oxide",
                "battery_capacity": "2.98",
                "battery_density": "269",
                "battery_cycle": "2000"
            },
            "Ola S1 Pro (E2W-AB-04)": {
                "range": "144",
                "max_speed": "78.6",
                "electric_energy_consumption": "3.4",
                "battery_technology": "Nickel Manganese Cobalt Oxide",
                "battery_capacity": "3.97",
                "battery_density": "269",
                "battery_cycle": "2000"
            }
        },
        "Booma Innovative": {
            "ANAV1200": {
                "range": "80",
                "max_speed": "40",
                "electric_energy_consumption": "3.6",
                "battery_technology": "Lithium-Ion",
                "battery_capacity": "2.00",
                "battery_density": "221",
                "battery_cycle": "1000"
            }
        },
        "Lectrix Ev": {
            "ecity zipD40": {
                "range": "89",
                "max_speed": "40",
                "electric_energy_consumption": "3.65",
                "battery_technology": "Lithium Ion",
                "battery_capacity": "2.00",
                "battery_density": "183",
                "battery_cycle": "1000"
            },
            "ecity zipC40": {
                "range": "89",
                "max_speed": "40",
                "electric_energy_consumption": "3.65",
                "battery_technology": "Lithium Ion",
                "battery_capacity": "2.00",
                "battery_density": "183",
                "battery_cycle": "1000"
            },
            "ecity zipCE40": {
                "range": "91",
                "max_speed": "40",
                "electric_energy_consumption": "3.14",
                "battery_technology": "",
                "battery_capacity": "1.90",
                "battery_density": "231.27",
                "battery_cycle": "1000"
            },
            "LXS": {
                "range": "100",
                "max_speed": "40",
                "electric_energy_consumption": "2.64",
                "battery_technology": "",
                "battery_capacity": "2.00",
                "battery_density": "183",
                "battery_cycle": "1000"
            }
        },
        "Maruthisan Private": {
            "MS 3.0": {
                "range": "140",
                "max_speed": "77.7",
                "electric_energy_consumption": "3",
                "battery_technology": "",
                "battery_capacity": "2.88",
                "battery_density": "199.5",
                "battery_cycle": "1000"
            }
        },
        "Okaya Ev": {
            "FAAST F4": {
                "range": "163",
                "max_speed": "40",
                "electric_energy_consumption": "5.06",
                "battery_technology": "",
                "battery_capacity": "4.40",
                "battery_density": "120",
                "battery_cycle": "2000"
            },
            "FAAST F2B": {
                "range": "85",
                "max_speed": "40",
                "electric_energy_consumption": "4.56",
                "battery_technology": "",
                "battery_capacity": "2.20",
                "battery_density": "120",
                "battery_cycle": "2000"
            },
            "FAAST F2T": {
                "range": "85",
                "max_speed": "40",
                "electric_energy_consumption": "4.56",
                "battery_technology": "",
                "battery_capacity": "2.20",
                "battery_density": "120",
                "battery_cycle": "2000"
            }
        },
        "Bgauss Auto": {
            "BGAUSS D15 PRO": {
                "range": "115",
                "max_speed": "58.3",
                "electric_energy_consumption": "3.4",
                "battery_technology": "",
                "battery_capacity": "3.20",
                "battery_density": "250",
                "battery_cycle": "1000"
            },
            "BGAUSS D15 i": {
                "range": "115",
                "max_speed": "58.3",
                "electric_energy_consumption": "3.4",
                "battery_technology": "",
                "battery_capacity": "3.20",
                "battery_density": "250",
                "battery_cycle": "1000"
            }
        },
        "Battre Electric": {
            "Stor:ie": {
                "range": "132",
                "max_speed": "40",
                "electric_energy_consumption": "3.23",
                "battery_technology": "",
                "battery_capacity": "3.10",
                "battery_density": "204.68",
                "battery_cycle": "1000"
            }
        },
        "Twenty Two": {
            "e.1": {
                "range": "80",
                "max_speed": "40",
                "electric_energy_consumption": "3.40",
                "battery_technology": "",
                "battery_capacity": "1.90",
                "battery_density": "231",
                "battery_cycle": "1000"
            }
        },
        "Chetak Technology": {
            "Chetak 2423 Premium": {
                "range": "115",
                "max_speed": "62.1",
                "electric_energy_consumption": "3",
                "battery_technology": "",
                "battery_capacity": "2.90",
                "battery_density": "231",
                "battery_cycle": "1000"
            }
        },
        "Amo Mobility": {
            "Jaunty+": {
                "range": "108",
                "max_speed": "40",
                "electric_energy_consumption": "2.54",
                "battery_technology": "",
                "battery_capacity": "2.40",
                "battery_density": "135",
                "battery_cycle": "2000"
            }
        },
        "Hero Motocorp": {
            "VIDA V1 Plus": {
                "range": "143",
                "max_speed": "52",
                "electric_energy_consumption": "2.7",
                "battery_technology": "",
                "battery_capacity": "3.40",
                "battery_density": "257",
                "battery_cycle": "1000"
            },
            "VIDA V1 Pro": {
                "range": "165",
                "max_speed": "53",
                "electric_energy_consumption": "2.4",
                "battery_technology": "",
                "battery_capacity": "4.00",
                "battery_density": "257",
                "battery_cycle": "1000"
            }
        },
        "Tork Motors": {
            "KRATOS-R": {
                "range": "113",
                "max_speed": "40",
                "electric_energy_consumption": "4.87",
                "battery_technology": "",
                "battery_capacity": "4.00",
                "battery_density": "257",
                "battery_cycle": "1000"
            }
        }
    }
}
connector_type = ["AC-TYPE-1", "AC-TYPE-2", "DC-CHAdeMO", "DC-CCS", "DC-Type 2"]


def get_vehicle_data_set():
    # TODO: Currently providing temp data from here later we will move it to database
    return vehicle_data


class VehicleMake:
    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type

    def get_list_of_make(self):
        return {"make_list": list(vehicle_data[self.vehicle_type].keys())}





class VehicleModel:
    def __init__(self, vehicle_type, vehicle_make):
        self.vehicle_type = vehicle_type
        self.vehicle_make = vehicle_make

    def get_list_of_models(self):
        return {"model_list": list(vehicle_data[self.vehicle_type][self.vehicle_make].keys()), "connector_list": connector_type}


class RegisterVehicleOperations:
    def __init__(self, current_user, db_operation):
        self.current_user: data_schemas.FirstTimeUser = current_user
        self.db_operation: UserRelatedDbOperations = db_operation
        self.vehicle_field_name = "vehicle_data"

    async def _get_current_vehicle_details_of_user(self) -> list:
        try:
            current_user: data_schemas.InitUser = await self.db_operation.get_user(self.current_user)
        except HTTPException:
            raise
        else:
            vehicle_details: list = current_user.vehicle_data
            logger.debug(f"Got user data and vehicle details are {vehicle_details}")
            return vehicle_details

    async def update_vehicle_data_for_current_user(self, current_vehicle_data: list) -> dict:
        try:
            updated_vehicle_data: dict = {self.vehicle_field_name: current_vehicle_data}
            logger.info(f"Updated vehicle data is {updated_vehicle_data}")
            response = await self.db_operation.update_user_data(self.current_user, updated_vehicle_data)
        except HTTPException:
            raise
        else:
            logger.info(f"Here is the response of vehicle update {response}")
            return response["Attributes"]

    @staticmethod
    def check_vehicle_exist_in_current_list(vehicle, current_vehicle_data) -> int:
        for i, vehicle_now in enumerate(current_vehicle_data):
            if vehicle_now["registration_number"] == vehicle.registration_number \
                    and vehicle_now["model"] == vehicle.model:
                return i
        else:
            return -1

    def get_vehicle_related_metdata(self, vehicle: data_schemas.RegisterNewVehicle) -> data_schemas.RegisterNewVehicle:
        try:
            vehicle_metadata = get_vehicle_data_set()[vehicle.vehicle_type][vehicle.make][vehicle.model]
        except KeyError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please enter correct data")

        vehicle.power_capacity = vehicle_metadata["battery_capacity"]
        vehicle.electric_energy_consumption = vehicle_metadata["electric_energy_consumption"]
        vehicle.max_speed = vehicle_metadata["max_speed"]
        vehicle.range = vehicle_metadata["range"]
        vehicle.battery_technology = vehicle_metadata["battery_technology"]
        vehicle.battery_density = vehicle_metadata["battery_density"]
        vehicle.battery_cycle = vehicle_metadata["battery_cycle"]
        return vehicle

    async def add_a_vehicle_with_metadata(self, vehicle, currently_stored_vehicle_list: list) -> list:
        filled_vehicle_data = self.get_vehicle_related_metdata(vehicle)
        currently_stored_vehicle_list.append(filled_vehicle_data.dict())
        return currently_stored_vehicle_list

    async def add_vehicle_for_current_user(self, vehicle: data_schemas.RegisterNewVehicle):
        current_vehicle_data = await self._get_current_vehicle_details_of_user()
        if self.check_vehicle_exist_in_current_list(vehicle, current_vehicle_data) >= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This vehicle data already exist")
        else:
            added_vehicle_data_for_user = await self.add_a_vehicle_with_metadata(vehicle, current_vehicle_data)
            logger.info(f"Adding a new vehicle {vehicle}")
            response = await self.update_vehicle_data_for_current_user(added_vehicle_data_for_user)
            return {"status_code": status.HTTP_201_CREATED, "message": f"Vehicle details registered",
                    "data": response}

    async def get_list_of_vehicles_for_current_user(self):
        current_vehicle_data = await self._get_current_vehicle_details_of_user()
        return {
            "status_code": 200,
            "message": "here is the list of vehicles",
            "data": {
                self.vehicle_field_name: current_vehicle_data
            }
        }

    async def get_short_list_of_vehicles_for_current_user(self):
        current_vehicle_data = await self._get_current_vehicle_details_of_user()
        list_of_vehicle_strings = []
        for vehicle in current_vehicle_data:
            list_of_vehicle_strings.append({"name": f"{vehicle['model']}_{vehicle['registration_number']}",
                                            "type": vehicle["vehicle_type"]})
        return list_of_vehicle_strings

    async def remove_vehicle(self, vehicle: data_schemas.RegisterNewVehicle):
        current_vehicle_data = await self._get_current_vehicle_details_of_user()
        registered_vehicle_index = self.check_vehicle_exist_in_current_list(vehicle, current_vehicle_data)
        if registered_vehicle_index < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This vehicle is not registered. No need to delete")
        else:
            logger.info(f"removing vehicle {vehicle}")
            current_vehicle_data.pop(registered_vehicle_index)
            response = await self.update_vehicle_data_for_current_user(current_vehicle_data)
            return {"status_code": status.HTTP_200_OK, "message": f"Vehicle deleted from user's list",
                    "data": response}

    async def edit_vehicle(self, old_vehicle_data: data_schemas.RegisterNewVehicle,
                           edited_vehicle_data: data_schemas.RegisterNewVehicle):
        currently_stored_vehicles = await self._get_current_vehicle_details_of_user()
        registered_vehicle_index = self.check_vehicle_exist_in_current_list(old_vehicle_data, currently_stored_vehicles)
        if registered_vehicle_index < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This vehicle is not registered. Editing is not possible")
        else:
            currently_stored_vehicles.pop(registered_vehicle_index)
            latest_vehicle_data = await self.add_a_vehicle_with_metadata(edited_vehicle_data, currently_stored_vehicles)
            logger.debug(f"Updating  database with edited {edited_vehicle_data} in place of {old_vehicle_data}")
            response = await self.update_vehicle_data_for_current_user(latest_vehicle_data)
            return {"status_code": status.HTTP_200_OK, "message": f"Vehicle data updated",
                    "data": response}


if __name__ == '__main__':
    print(vehicle_data["vehicle_type"].keys())
