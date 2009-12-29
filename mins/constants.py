MINIMUMS_VERBOSE =      {       "total":                "Total",
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
