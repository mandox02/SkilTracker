import customtkinter as ctk
import mainscript as main
import string

app = ctk.CTk()
app.title("ConsulTracker v0.1")
app.geometry("600x500")

current_mode = "idle"

def set_mode(newmode):
    global current_mode
    current_mode = newmode

def basicsearch(term):
    results = []
    # Return error for invalid characters or blank search
    if any(char for char in term if char == string.punctuation):
        error_code = main.error_codes["3a"]
        return results, error_code

    if term == "":
        error_code = main.error_codes["2"]
        return results, error_code

    # Check whether the search is for a name or ID
    if any(char.isdigit() for char in term):
        id_info, skills_info, location = main.retrieveinfobyid(term)
    else: id_info, skills_info, location = main.retrieveinfobyname(term)

    foundid = id_info[0]
    fullname = id_info[1] + " " + id_info[2]


    # Show the list to the user and wait for it to receive a response
    # trigger mode to viewing

# Labels and Entry boxes go here
searchbyid_label = ctk.CTkLabel(app, text="Search by ID or Name:")
searchbyid_entry = ctk.CTkEntry(app)
id_label = ctk.CTkLabel(app, text="ID:")
id_entry = ctk.CTkEntry(app)
name_label = ctk.CTkLabel(app, text="Name:")
name_entry = ctk.CTkEntry(app)
band_label = ctk.CTkLabel(app, text="Band:")
band_entry = ctk.CTkEntry(app)
sector_label = ctk.CTkLabel(app, text="Sector:")
sector_entry = ctk.CTkEntry(app)

# Buttons go here
new_button = ctk.CTkButton(app, text="New",command=lambda: print("New consultant requested."),fg_color="#4DAB3A")
edit_button = ctk.CTkButton(app, text="Edit",command=lambda: print("Edit requested."),fg_color="#4DAB3A")
delete_button = ctk.CTkButton(app, text="Delete",command=lambda: print("Deletion requested."),fg_color="#DE503A")
search_button = ctk.CTkButton(app, text="Search",command=basicsearch(searchbyid_entry.get()),fg_color="#5550DE")
advsearch_button = ctk.CTkButton(app, text="Advanced Search...",command=lambda: print("Advanced search requested."),fg_color="#5550DE")


# Activation goes here
searchbyid_label.grid(row=0,column=0)
searchbyid_entry.grid(row=0,column=1)
search_button.grid(row=0,column=2)
advsearch_button.grid(row=0,column=3)

id_label.grid(row=1,column=0)
id_entry.grid(row=1,column=1)
name_label.grid(row=1,column=2)
name_entry.grid(row=1,column=3)

band_label.grid(row=2,column=0)
band_entry.grid(row=2,column=1)
sector_label.grid(row=2,column=2)
sector_entry.grid(row=2,column=3)

new_button.grid(row=3,column=0)
edit_button.grid(row=3,column=1)
delete_button.grid(row=3,column=2)

app.mainloop()