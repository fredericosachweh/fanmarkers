VOTE_WEIGHT	=	(	(1, "I have no idea what I'm talking about"),
				(2, "I read about it somewhere"),
				(3, "Heard it from a friend-of-a-friend"),
				(4, "Heard it from someone I know very well"),
				(5, "I have first hand experience")
			)
			
JUMPSEAT_TYPE	=	(	(0, "Unknown"),
				(1, "None"),
				(2, "Custom Agreement"),
				(3, "CASS") )
				
PAY_TYPE	=	(	(0, "Unknown"),
				(1, "Full Pay"),
				(2, "Partial Pay"),
				(3, "No Pay"),
				(4, "You Pay Them Partially"),
				(5, "You Pay Them in Full") )
			
AIRPORT_TYPE	=	(	(0, "Unknown"),
				(1, "Small Airport"),
				(2, "Medium Airport"),
				(3, "Large Airport"),
				(4, "Closed"),
				(5, "Heliport"),
				(6, "Seaplane Base"),
				(7, "Balloon Port") )
				
BASE_ENTRY	=	(	(0, "Unknown"),
				(1, "Guaranteed"),
				(2, "Choice; Likely"),
				(3, "Choice; Unlikely"),
				(4, "Assigned: Likely"),
				(5, "Assigned: Unlikely") )
				
HIRING_STATUS	=	(	(1, "Not Hiring"),
				(2, "Hiring"),
				(3, "Lay-offs") )
				
HIRING_METHOD	=	(	(0, "Unknown"),
				(1, "Outside Only"),
				(2, "Anywhere"),
				(3, "Only from within") )	
				
ENGINE_TYPE	=	(	(0, "None"),
				(1, "Low Performance Piston"),
				(2, "High Performance Piston"),
				(3, "Turboprop"),
				(4, "Jet") )
				
CERT_LEVEL	=	(	(0, "None"),
				(1, "Private"),
				(2, "Commercial"),
				(3, "Commercial + Instrument"),
				(4, "Frozen ATPL"),
				(5, "ATP") )
				
MECH_CERT_LEVEL	=	(	(0, "None"),
				(1, "A&P"),
				(2, "AI"),
				(3, "Other") )
				
CERT_AGENCY	=	(	(0, "None"),
				(1, "FAA"),
				(2, "JAR"),
				(3, "Any ICAO"),
				(4, "Other") )
				
DEGREE		=	(	(0, "Unknown"),
				(1, "No degree required"),
				(2, "High School Degree"),
				(3, "4-year University Degree"),
				(4, "Graduate Degree"),
			)
				
JOB_DOMAIN	=	(	(1, "Crew Captain"),
				(2, "Single Pilot Captain"),
				(3, "Line SIC"),
				(4, "Instructor Pilot"),
				(5, "Flight Engineer"),
				(6, "Flight Attendant"),
				(7, "Management/Pilot"),
				(8, "Mechanic/Pilot"),
				(9, "Mechanic"),
				(10, "Management"),
				(12, "Dispatcher"),
				(13, "Other Non-flying"),
				(14, "Other Flying") )
				
SALARY_TYPE	=	(	(1, "/flight hour"),
				(2, "/duty hour"),
				(3, "/day"),
				(4, "/week"),
				(5, "/month"),
				(6, "/year"),
				(7, "/flight"),
				(8, "/contract") )
				
SCHEDULE_TYPE	=	(	(0, "Unknown"),
				(1, "Scheduled"),
				(2, "On Call"),
				(3, "You pick your schedule"),
				(4, "Little bit of all three") )

BUSINESS_TYPE	=	(	(1, "FBO-type flight school"),
				(2, "Academy-type flight school"),
				(3, "Small cargo airline"),
				(4, "Large cargo airline"),
				(5, "Small passenger airline"),
				(6, "Large passenger Airline"),
				(7, "Aircraft ferry"),
				(8, "Cloud seeding"),
				(9, "Aerial Application"),
				(10, "Aerial Photography"),
				(11, "Aerial Survey"),
				(12, "Scenic flights / Aerial Tours"),
				(12, "Other") )
				
CAT_CLASSES	=	(	(1, "Airplane SEL"),
				(2, "Airplane MEL"),
				(3, "Airplane SES"),
				(4, "Airplane MES"),
				(5, "Glider"),
				(6, "Helicopter"),
				(7, "Airplane Simulator"),
				(8, "Helicopter Simulator"),
				(9, "Other"), )
				
MINIMUMS_VERBOSE=	{	"total":		"Total",
				"night":		"Night",
				"instrument":		"Instrument",
				"dual_given":		"Instruction Given",
				"xc":			"Cross Country",
				"pic":			"PIC",
				"t_pic":		"Turbine PIC",
				"jet_pic":		"Jet PIC",
				"jet":			"Jet",
				"turbine":		"Turbine",
				"cert_level":		"Certification Level",
				"instructor":		"Instructor Privileges",
				"instrument_instructor":"Instrument Instructor Privileges",
				
				"degree":		"Education",
				"years_exp":		"Years of Experience",
				"years_company":	"Years With This Company",
				"seniority":		"Enough Seniority",
				"rec":			"Internal Recommendation",
				"mech_cert":		"Mechanic Certification",
				"cert_agency":		"Certification Agency",
				"atp":			"ATP Minimums",
				"i135":			"Part 135 IFR Minimums",
				"v135":			"Part 135 VFR Minimums",
				"tailwheel":		"Tailwheel Endorsement",
				"type_rating":		"Type Rating",
				"on_type":		"Time on Type",
			}
				
				
