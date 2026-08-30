from __future__ import annotations
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import column_index_from_string
from openpyxl.utils import get_column_letter
from collections import Counter
import string


wb = openpyxl.load_workbook('skiltracker-main.xlsx', data_only=True)

ids = wb['ID']
skills = wb['Skills']

# Defining default values.
candidateid = None
candidatename = None
candidateln = None
band = None
sector = None
id_charlength = 6

error_codes = {
    "0": "All good",
    "1": "Excel file cannot be found (Read).",
    "2": "Blank search. Please enter at least one value.",
    "3": "No results.",
    "3a": "Invalid character(s) in search parameters.",
    "4": "Error writing to excel file",
    "5": "Excel file cannot be found (Write)",
    "6": "Duplicate ID.",
    "6a": "No ID found.",
    "7a": "Enter an ID.",
    "7b": "Enter the name.",
    "7c": "Enter the band.",
    "7d": "Enter the sector.",
    "7e": "Enter at least one skill for each Category.",
    "7f": "Enter at least one skill.",
    "8": f"Invalid ID Length. Please make sure the ID is {id_charlength} characters long.",
    "9": "ID rows do not match in the Excel file. Please check it.",
    "10a": "Invalid characters (ID)",
    "10b": "Invalid characters (Name or Last Name)",
    "10c": "Invalid characters (Band)",
    "10d": "Invalid characters (Sector)",
    "10e": "Invalid characters (Skill)",
}

# Defining custom values
existing_bands = [0]
existing_sectors = [0]

for cell in ids['D']:
    if cell.row != 1:
        if cell.value not in existing_bands:
            existing_bands.append(cell.value)

print(existing_bands)

for cell in ids['E']:
    if cell.row != 1:
        if cell.value not in existing_sectors:
            existing_sectors.append(cell.value)

print(existing_sectors)


def saveinfo(candidateid, candidatename, candidateln, band, sector, cat1, cat2, cat3):
    # input to define the values goes here
    error_code = error_codes["0"]

    id_digitcheck = len(candidateid)
    print(f"Candidate ID contains  {id_digitcheck} characters.")

    if id_digitcheck != id_charlength:
        print(f"Candidate ID contains does not contain {id_charlength} digits.")
        error_code = error_codes["8"]
        return False, error_code
    else: print("Proceeding with correct candidate ID length.")

    for cell in ids["A"]: # Checks for duplicate ID
        if cell.value == candidateid:
            error_code = error_codes["6"]
            print("Duplicate ID. Code cannot continue.")
            return False, error_code

    next_empty_row = None
    ids_row = None
    skills_row = None

    # IDs worksheet
    # Loop through the designated column up to the max row
    for cell in ids["A"]:
        if cell.value is None:
            next_empty_row = cell.row
            break

    # If no empty cell was found in existing rows, use the next fresh row
    if next_empty_row is None:
        next_empty_row = ids.max_row + 1

    print(f"The next empty cell in Column A is at row {next_empty_row} in the worksheet IDs")
    ids_row = next_empty_row

    next_empty_row = None

    # Skills worksheet
    # Loop through the designated column up to the max row
    for cell in skills["A"]:
        if cell.value is None:
            next_empty_row = cell.row
            break
    
    # If no empty cell was found in existing rows, use the next fresh row
    if next_empty_row is None:
        next_empty_row = skills.max_row + 1
    
    print(f"The next empty cell in Column A is at row {next_empty_row} in the worksheet Skills")
    skills_row = next_empty_row

    if skills_row != ids_row:
        error_code = error_codes["9"]
        return False, error_code

    # Validation Block
    if not candidateid.isalnum() or candidateid == "": # ID CHECK
        error_code = error_codes["10a"]
        return False, error_code
        
    for names in [candidatename, candidateln]: # NAME AND LAST NAME CHECK
        if any(char.isdigit() for char in names) or names == "":
            error_code = error_codes["10b"]
            return False, error_code

    if type(band) != int: # BAND CHECK
        error_code = error_codes["10c"]
        return False, error_code

    if not sector.isalpha() or sector == "": # SECTOR CHECK
        error_code = error_codes["10d"]
        return False, error_code

    output, skill_code = validateinitialentry(cat1,cat2,cat3) # SKILL CHECK
    if output == False:
        error_code = skill_code
        return False, error_code

    # Assignments
    ids[f"A{ids_row}"] = candidateid
    skills[f"A{skills_row}"] = candidateid
    ids[f"B{ids_row}"] = candidatename
    ids[f"C{ids_row}"] = candidateln
    ids[f"D{ids_row}"] = band
    ids[f"E{ids_row}"] = sector

    # Making sure each category has its maximum, padded by Nones to make empty cells.
    cat1 = cat1 + [None] * (2 - len(cat1))
    cat2 = cat2 + [None] * (5 - len(cat2))
    cat3 = cat3 + [None] * (5 - len(cat3))
    
    combined_skills = cat1 + cat2 + cat3
    for index, value in enumerate(combined_skills):
        index += 2 #adds 2 to each index number to match column number
        index = get_column_letter(index)
        skills[f"{index}{skills_row}"] = value

    wb.save("skiltracker-main.xlsx")
    print("Saved successfully.")
    return True, error_code

def editinfo(candidateid, candidatename="", candidateln="", band=None, sector="", cat1=None, cat2=None, cat3=None):
    final_name = None
    final_ln = None
    final_band = None
    final_sector = None
    final_cat1 = None
    final_cat2 = None
    final_cat3 = None
    error_code = error_codes["0"]

    if cat1 == None:
            cat1 = []
    if cat2 == None:
            cat2 = []
    if cat3 == None:
            cat3 = []

    id_info, skills_info, ids_row = retrieveinfobyid(candidateid)

    if id_info == None:
        error_code = error_codes["6a"]
        return False, error_code

    if candidatename != "" and candidatename != id_info[1]:
        if any(char.isdigit() for char in candidatename):
            error_code = error_codes["10b"]
            return False, error_code
        else: 
            final_name = candidatename
    else: 
        final_name = id_info[1]

    if candidateln != "" and candidateln != id_info[2]:
            if any(char.isdigit() for char in candidateln):
                error_code = error_codes["10b"]
                return False, error_code
            else: 
                final_ln = candidateln
    else: 
        final_ln = id_info[2]

    if band != None and band != id_info[3]:
        if type(band) != int:
            error_code = error_codes["10c"]
            return False, error_code
        else: 
            final_band = band
    else: 
        final_band = id_info[3]

    if sector != "" and sector != id_info[4]:
        if not sector.isalpha():
                error_code = error_codes["10d"]
                return False, error_code
        else: 
            final_sector = sector
    else: 
        final_sector = id_info[4]

    existing_cat1 = skills_info[1:3]
    existing_cat2 = skills_info[3:8]
    existing_cat3 = skills_info[8:13]
    
    existing_cat1C = [item for item in existing_cat1 if item != None]
    existing_cat2C = [item for item in existing_cat2 if item != None]
    existing_cat3C = [item for item in existing_cat3 if item != None]

    if cat1 == existing_cat1C or cat1 == []:
        final_cat1 = existing_cat1C
    else:
        final_cat1 = cat1

    if cat2 == existing_cat2C or cat2 == []:
        final_cat2 = existing_cat2C
    else:
        final_cat2 = cat2

    if cat3 == existing_cat3C or cat3 == []:
        final_cat3 = existing_cat3C
    else:
        final_cat3 = cat3

    output, skill_code = validateinitialentry(final_cat1,final_cat2,final_cat3) # SKILL CHECK
    if output == False:
        error_code = skill_code
        return False, error_code

    # Making sure each category has its maximum, padded by Nones to make empty cells.
    final_cat1 = final_cat1 + [None] * (2 - len(final_cat1))
    final_cat2 = final_cat2 + [None] * (5 - len(final_cat2))
    final_cat3 = final_cat3 + [None] * (5 - len(final_cat3))

    # Assignments
    skills_row = ids_row
    ids[f"B{ids_row}"] = final_name
    ids[f"C{ids_row}"] = final_ln
    ids[f"D{ids_row}"] = final_band
    ids[f"E{ids_row}"] = final_sector
    
    combined_skills = final_cat1 + final_cat2 + final_cat3
    for index, value in enumerate(combined_skills):
        index += 2 #adds 2 to each index number to match column number
        index = get_column_letter(index)
        skills[f"{index}{skills_row}"] = value

    wb.save("skiltracker-main.xlsx")
    print("Saved successfully.")
    return True, error_code

def deleteinfo(candidateid):
    error_code = error_codes["0"]
    # find the candidate
    id_info, skills_info, id_row = retrieveinfobyid(candidateid)

    if id_info == None:
        error_code = error_codes["6a"]
        return False, error_code

    # Catch misalignment and return False and error 9 if so
    if ids[f"A{id_row}"].value != skills[f"A{id_row}"].value:
        error_code = error_codes["9"]
        return False, error_code

    # If alignment is correct, delete the entire row and save
    ids.delete_rows(id_row,1)
    skills.delete_rows(id_row,1)

    wb.save("skiltracker-main.xlsx")
    print("Saved successfully.")
    return True, error_code

def retrieveinfobyid(id_query): #Finds existing info in the workbook by ID.
    found_cell_location = None
    id_values = None
    skills_values = None

    for cell in ids["A"]:
        if cell.value == id_query:
            found_cell_location = cell.row
            print(f"found cell at A{found_cell_location}.")
            id_values = [cell.value for cell in ids[found_cell_location]]
            skills_values = [cell.value for cell in skills[found_cell_location]]
            break
    if id_values != None and skills_values != None:
        return id_values, skills_values, found_cell_location
    else: return None, None, None

def filterbyband(id_query):
    # For this one I proceeded to list all available entries by band match.
    found_cell_location = None
    found_entries = []

    try:
        id_query = int(id_query)
        query_count = 0
        
        for cell in ids["D"]:
            if cell.value == id_query:
                found_cell_location = cell.row
                found_entries.append(ids[f'A{found_cell_location}'].value)
                query_count += 1
        
        print(f"Found {query_count} entries. Those being: ")
        print(found_entries)
        band_results = found_entries
        error_code = error_codes["0"]
    except ValueError:
        band_results = []
        error_code = error_codes["3a"]

    return band_results, error_code

def filterbysector(id_query):
    # For this one I proceeded to list all available entries by sector match.
    found_cell_location = None
    found_entries = []

    if id_query.isalpha():
        id_query = id_query.capitalize()
        query_count = 0
        
        for cell in ids["E"]:
            if cell.value == id_query:
                    found_cell_location = cell.row
                    found_entries.append(ids[f'A{found_cell_location}'].value)
                    query_count += 1
        
        print(f"Found {query_count} entries. Those being: ")
        print(found_entries)
        sector_results = found_entries
        error_code = error_codes["0"]
    else:
        sector_results = found_entries
        error_code = error_codes["3a"]

    return sector_results, error_code

skill_categories = [ # defines the categories by the column range the skill is in
    (column_index_from_string('B'), column_index_from_string('C'), "1"),
    (column_index_from_string('D'), column_index_from_string('H'), "2"),
    (column_index_from_string('I'), column_index_from_string('M'), "3"),
]

def getskillcategory(col_index): # Uses the above list to return the category for the skill selected.
    for start, end, label in skill_categories:
        if start <= col_index <= end:
            return label
    return None 

def filterbyskill(id_query, category_check=""):
    found_entries = []
    found_skill_categories = []
    query_count = 0
    error_code = "0"

    if not any(char.isdigit() for char in id_query) and id_query != "":
        for column in skills:
            for cell in column:
                if cell.value == id_query:
                    found_cell_location = cell.row
                    category = getskillcategory(cell.column)
                    if category == category_check or category_check == "":
                        found_skill_categories.append(category)
                        found_entries.append(skills[f'A{found_cell_location}'].value)
                        query_count += 1
                    

        print(f"Found {query_count} entries. Those being: ")
        print(found_entries)
        print(found_skill_categories)
        skill_results = found_entries
        if not found_entries:
            error_code = error_codes["3"]
            # Should return "No Results" error
        else: error_code = error_codes["0"]
    elif id_query == "":
        skill_results = []
        error_code = error_codes["2"]
        # Should return "Blank Search" error
    else: 
        skill_results = []
        error_code = error_codes["3a"]
        # Should return "Invalid Search terms" error

    return skill_results, error_code

def advancedsearch(skill="",category="",band="",sector=""):

    active_filters = []
    final_error_code = error_codes["0"]
    final_results = []
    skill_results = []
    skill_error = "0"
    band_results = []
    band_error = "0"
    sector_results = []
    sector_error = "0"
    search_type = ""

    if all([skill=="",band=="",sector==""]): # checks for error 2 here.
        final_error_code = error_codes["2"]
        return [], final_error_code
    else:
        if skill != "":
            print("Skill detected.")
            skill_results, skill_error = filterbyskill(skill, category)
            if skill_error != error_codes["0"]:
                return [], skill_error
            else:
                print("Appending.")
                active_filters.append(skill_results)

        if band != "":
            print("Band detected.")
            band_results, band_error = filterbyband(band)
            if band_error != error_codes["0"]:
                return [], band_error
            else:
                print("Appending.")
                active_filters.append(band_results)

        if sector != "":
            print("Sector detected.")
            sector_results, sector_error = filterbysector(sector)
            if sector_error != error_codes["0"]:
                return [], sector_error
            else:
                print("Appending.")
                active_filters.append(sector_results)

        print(f"Active filters: {len(active_filters)}")

        # Output depends on active_filters length value, if more than 2 triggers advanced search
        if len(active_filters) >= 2:
            print("Advanced search detected.")
            print(f"Input: {active_filters}")
            final_results = list(set(active_filters[0]).intersection(*active_filters[1:]))
            search_type = "Advanced"
        else:
            final_results = active_filters
            search_type = "Standard"

        if final_results == []:
            final_error_code = error_codes["3"]

    print(f"Search performed: {search_type}")
    return final_results, final_error_code

def validateskillentry(id_row):
    error_code = error_codes["0"]
    if any(skills.cell(row=id_row,column=col).value != None for col in range(2,14)):
        for start, end, label in skill_categories:
            if any(skills.cell(row=id_row,column=col).value != None for col in range(start,end+1)):
                print("Success.")
            else: 
                print("Any one of these categories has a missing value. All of them should have at least one. Category missing: ", label)
                error_code = error_codes["7e"]
                return False, error_code
        return True, error_code
    else: 
        error_code = error_codes["7f"]
        return False, error_code

def validateinitialentry(cat1,cat2,cat3):
    error_code = error_codes["0"]
    for category in [cat1,cat2,cat3]:
        print(category)
        if category != []:
            for skill in category:
                if skill == "":
                    skill = None
                elif any(char.isdigit() for char in skill):
                    error_code = error_codes["10e"]
                    return False, error_code

            print("Success.")
        else:
            print("This category is empty. Code cannot proceed.")
            error_code = error_codes["7e"]
            return False, error_code
    
    return True, error_code

def basesearch(term):
    resultlist = []
     # Check whether the search is for a name or ID
    if any(char.isdigit() for char in term):
        if char.isalpha():
            char.upper()
        # Searching by ID match
        for char in term:
            if char.isalpha():
                char.upper()
        for cell in ids["A"]:
            if term in cell.value:
                resultlist.append(cell.value)
    else: 
        # Searching by name match
        print("searching by name")
        for cell in ids["B"]:

            if term in cell.value.lower():
                location = cell.row
                resultlist.append(ids[f"A{location}"].value)
        for cell in ids["C"]:
            if term in cell.value.lower():
                location = cell.row
                if ids[f"A{location}"].value not in resultlist:
                    resultlist.append(ids[f"A{location}"].value)
    return resultlist

def retrieveall(): #Finds all registered IDs and returns them to the UI to display.
    resultlist = []

    for cell in ids["A"]:
        location = cell.row
        if location != 1:
            resultlist.append(ids[f"A{location}"].value)

    return resultlist