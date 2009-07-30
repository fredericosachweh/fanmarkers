VOTE_WEIGHT     =       [       (1, "I have no idea what I'm talking about"),
                                (2, "I read about it somewhere"),
                                (3, "Heard it from a friend-of-a-friend"),
                                (4, "Heard it from someone I know very well"),
                                (5, "I have first hand experience")
                        ]

JUMPSEAT_TYPE   =       [       (0, "Not Known"),
                                (1, "None"),
                                (2, "Custom Agreement"),
                                (3, "CASS")
                        ]

PAY_TYPE        =       [       (0, "Not Known"),
                                (1, "The pilot pays the full price of training"),
                                (2, "The pilot pays for part of the training"),
                                (3, "No Pay"),
                                (4, "Pilot gets reduced salary during training"),
                                (5, "Pilot gets full salary during training")
                        ]



CERT_LEVEL      =       [
                                (0, "None"),
                                (1, "Private"),
                                (2, "Endorsed"),
                                (3, "Commercial"),
                                (4, "Frozen ATPL"),
                                (5, "ATP")
                        ]

MECH_CERT_LEVEL =       [       (0, "None"),
                                (1, "A&P"),
                                (2, "AI"),
                                (3, "Other")
                        ]


DEGREE          =       [       (0, "No degree required"),
                                (1, "High School Degree"),
                                (2, "4-year University Degree"),
                                (3, "Graduate Degree"),
                        ]

JOB_DOMAIN      =       [       (1, "Captain: Crew"),
                                (2, "Captain: Single Pilot"),
                                (3, "Captain: Crew/Single Pilot"),
                                (4, "Line SIC"),
                                (5, "Instructor Pilot"),
                                (6, "Flight Engineer"),
                                (7, "Flight Attendant"),
                                (8, "Management/Pilot"),
                                (9, "Mechanic/Pilot"),
                                (10, "Mechanic"),
                                (11, "Management"),
                                (12, "Dispatcher"),
                                (13, "Other Non-flying"),
                                (14, "Other Flying"),
                        ]

HIRING_STATUS   =       {       "not": "Not Hiring",
                                "assign": "Currently Hiring (assign)",
                                "choice": "Currently Hiring (choice)",
                                "unknown": "Hiring Status Unknown",
                                "layoff": "Laying-off/Furloughing",
                        }

SALARY_TYPE     =       [       (1, "/flight hour"),
                                (2, "/duty hour"),
                                (3, "/day"),
                                (4, "/week"),
                                (5, "/month"),
                                (6, "/year"),
                                (7, "/flight"),
                                (8, "/contract")
                        ]

SCHEDULE_TYPE   =       [       (0, "Not Known"),
                                (1, "Scheduled"),
                                (2, "On Call"),
                                (3, "You pick your schedule"),
                                (4, "Little bit of all three")
                        ]

BUSINESS_TYPE   =       [       (1, "FBO-type flight school"),
                                (2, "Academy-type flight school"),
                                (3, "Cargo Airline"),
                                (4, "Passenger Airline"),
                                (5, "Passenger/Cargo Airline"),
                                (6, "Aircraft Ferry"),
                                (7, "Cloud Seeding"),
                                (8, "Aerial Application"),
                                (9, "Aerial Photography"),
                                (10, "Aerial Survey"),
                                (11, "Scenic flights / Aerial Tours"),
                                (13, "Private Charters"),
                                (14, "Corporate Flight Department"),
                                (15, "Sky Diving Drop Zone"),
                                (12, "Other")
                        ]

MINS_TYPE       =       [       (1, "Fixed Wing"),
                                (2, "Any Aircraft"),
                                (3, "Instrument Airplane"),
                                (3, "Single-Engine"),
                                (4, "Multi-Engine"),
                                (5, "Tailwheel"),
                                (6, "Single-Engine Tailwheel"),
                                (7, "Multi-Engine Tailwheel"),
                                (8, "Seaplanes"),
                                (9, "Single-Engine Seaplanes"),
                                (10, "Multi-Engine Seaplanes"),
                                (11, "Helicopters"),
                                (12, "Airplane Simulator"),
                                (13, "Helicopter Simulator"),
                                (14, "Turbine Engine Aircraft"),
                                (15, "Jet Engine Aircraft"),
                                (16, "Multi-Engine Turbine"),
                        ]


PART_135        =       [       (0, "None"),
                                (1, "VFR"),
                                (2, "IFR"),
                        ]

TYPE_RATING     =       [       (0, "None"),
                                (1, "PIC"),
                                (2, "SIC")
                        ]

MINIMUMS_VERBOSE=       {       "total":                "Total",
                                "night":                "Night",
                                "inst":                 "Instrument",
                                "dual_given":           "Instruction Given",
                                "xc":                   "Cross Country",
                                "pic":                  "PIC",
                                "t_pic":                "Turbine PIC",
                                "jet_pic":              "Jet PIC",
                                "jet":                  "Jet",
                                "turbine":              "Turbine",
                                "cert_level":           "Certification Level",
                                "instructor":           "Instructor Privileges",
                                "inst_instructor":      "Instrument Instructor Privileges",
                                "inst_rating":          "Instrument Rating",
                                "endorsed":             "Endorsed",

                                "type_rating":          "Type-Rating",

                                "degree":               "Education",
                                "years_exp":            "Years of Experience",
                                "years_company":        "Years With This Company",
                                "seniority":            "Enough Seniority",
                                "rec":                  "Internal Recommendation",
                                "mech_cert":            "Mechanic Certification",
                                "cert_agency":          "Certification Agency",
                                "atp_mins":             "ATP Minimums",
                                "part_135":             "Part 135 Minimums",
                                "tailwheel":            "Tailwheel Endorsement",
                        }
