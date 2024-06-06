import re
import pandas as pd
import sqlite3

neighbourhoods = [
    "yıldırım", "kartaltepe", "muratpaşa", "altıntepsi", "kocatepe", "cevatpaşa", "yenidoğan", "terazidere", "orta", "ismetpaşa", "vatan" # add all neighbourhood names here
]

def extract_data(line):
    data = {
        "tarih": None,
        "mahalle": None,
        "sokak": None,
        "mikroçip no": None,
        "küpe no": None
    }
    
    date_match = re.search(r"\d{2}/\d{2}/\d{4}", line)
    if date_match:
        data["tarih"] = date_match.group(0)
    
    for neighbourhood in neighbourhoods:
        if neighbourhood in line:
            data["mahalle"] = neighbourhood
            break

    microchip_match = re.search(r"mikroçip(?: no.)?\s*(9\d{13,14})", line, re.IGNORECASE)
    if microchip_match:
        data["mikroçip no"] = microchip_match.group(1)
    
    earring_match = re.search(r"küpe no.?\s*(\d+|ibb)", line, re.IGNORECASE)
    if earring_match:
        if earring_match.group(1).lower() == "ibb":
            data["küpe no"] = None
        else:
            data["küpe no"] = earring_match.group(1)
    
    if data["mahalle"]:
        street_match = re.search(rf"{data['mahalle']}.*?(mah\.|m\.|mh|m|mh\.|mah)(.*?)(mikroçip(?: no.)?|$)", line)
        if street_match:
            data["sokak"] = street_match.group(2).strip()
    
    return data

input_file = r"C:\Users\begum\Desktop\captions.txt" 
lines = open(input_file, "r", encoding="utf-8").readlines()

data_list = []
for line in lines:
    data = extract_data(line)
    data_list.append(data)

df = pd.DataFrame(data_list)

excel_output_file = r"C:\Users\begum\Desktop\output.xlsx"  
df.to_excel(excel_output_file, index=False)

conn = sqlite3.connect(r"C:\Users\begum\Desktop\database.db") 
df.to_sql("animal_data", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Data extraction complete. Output saved to", excel_output_file, "and SQL database.")
