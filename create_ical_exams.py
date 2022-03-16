# Create calendar elements for exams at UniLj
#
# Read Excel, filter lecturer, create iCalendar entries for all exams.
#
# Krištof Oštir
# 2016-09-15

# Load libraries
import pandas as pd

# Processing parameters
exams_list_fn = "/Users/Kristof/Documents/Predavanja/urnik/Izpitni roki_2016_2017_pripombe pedagogov_1.xlsx"
exams_calendar = "/Users/Kristof/Documents/Predavanja/urnik/izpiti_201617.ics"
lecturer = "Oštir"
subjects = [
    "Programska orodja v geodeziji",
    "Avtomatska obdelava podatkov",
    "Daljinsko zaznavanje I",
    "Avtomatska obdelava podatkov",
    "Uporabno daljinsko zaznavanje",
    "Analize prostorskih podatkov",
]

# Read list of exams and extract important columns
exams_list = pd.read_excel(exams_list_fn)
exams_list = exams_list[
    [
        "Vrsta študija",
        "letnik",
        "Izvajalec",
        "Predmet",
        "Datum izpita",
        "Datum izpita.1",
        "Datum izpita.2",
        "Dodaten rok",
    ]
]
exams_list = exams_list[exams_list["Izvajalec"].notnull()]

# print(exams_lecturer_idx)
exams_lecturer = exams_list[exams_list.Izvajalec.str.contains(lecturer)]
exams_lecturer = exams_lecturer.drop("Izvajalec", 1)
# List of subjects by lecturer
print("All subjects:", exams_lecturer["Predmet"].tolist())
print("Used subjects:", exams_lecturer["Predmet"].tolist())

# Melt dataframe
exams_lecturer_m = pd.melt(
    exams_lecturer, id_vars=["Vrsta študija", "letnik", "Predmet"], value_name="Datum"
)
exams_lecturer_m = exams_lecturer_m[exams_lecturer_m["Datum"].notnull()]
exams_lecturer_m = exams_lecturer_m.drop("variable", 1)
exams_lecturer_m = exams_lecturer_m[exams_lecturer_m["Predmet"].isin(subjects)]

# Prepare iCalendar entries
print("Writing ics", exams_calendar)
# Write to file
with open(exams_calendar, "w") as f:
    print("BEGIN:VCALENDAR", file=f)
    print("VERSION:2.0", file=f)
    print("PRODID:-//hacksw/handcal//NONSGML v1.0//EN", file=f)
    print("CALSCALE:GREGORIAN", file=f)
    for row in exams_lecturer_m.iterrows():
        print("BEGIN:VEVENT", file=f)
        print(
            "DTSTART;VALUE=DATE:", str(row[1][3])[:10].replace("-", ""), sep="", file=f
        )
        print("DESCRIPTION:", row[1][0], " - ", row[1][1], sep="", file=f)
        print("SUMMARY:Izipt - ", row[1][2], sep="", file=f)
        print("END:VEVENT", file=f)
    print("END:VCALENDAR", file=f)
