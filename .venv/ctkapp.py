import customtkinter as ctk
import mainscript as main
import string

app = ctk.CTk()
app.title("SkilTracker v0.1")
app.geometry("600x500")

current_mode = "idle"
viewing_id = None
resultlist = None
location = None

# MAIN WINDOW

def set_mode(newmode):
    global current_mode
    current_mode = newmode

# Labels, Entry boxes and the skills frame go here
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
skills_frame = ctk.CTkFrame(app)
cat1_entries = []
cat2_entries = []
cat3_entries = []
for i in range(2):
    entry = ctk.CTkEntry(skills_frame, state="disabled")
    entry.grid(row=i+1,column=0)
    cat1_entries.append(entry)
for i in range(5):
    entry = ctk.CTkEntry(skills_frame, state="disabled")
    entry.grid(row=i+1,column=1)
    cat2_entries.append(entry)
for i in range(5):
    entry = ctk.CTkEntry(skills_frame, state="disabled")
    entry.grid(row=i+1,column=2)
    cat3_entries.append(entry)

# Commands go here
def basicsearch():
    term = searchbyid_entry.get()
    print(f"Read term as {term}")
    id = None
    name = None
    names = []
    ids = []
    # Return error for invalid characters or blank search
    if term == "":
        error_code = main.error_codes["2"]
        return id, error_code

    print("entry is not empty, proceed")
    
    if any(char for char in term if char in string.punctuation):
        error_code = main.error_codes["3a"]
        return id, error_code

    print("entry has no special characters, proceed")

    # Check whether the search is for a name or ID and find all possible entries. 
    id_list = main.basesearch(term)
    print("got id_list, printing: ", id_list)

    for item in id_list:
        list1, list2, location = main.retrieveinfobyid(item)
        name = list1[1] + " " + list1[2]
        id = list1[0]
        names.append(name)
        ids.append(id)

    # Show the list to the user and wait for it to receive a response
    global resultlist
    resultlist= ctk.CTkScrollableFrame(app)
    entrycount = 0
    for item in ids:
        bslbutton = ctk.CTkButton(resultlist, text=f"{ids[entrycount]} | {names[entrycount]}",command=lambda item=item: selection(item)).pack(pady=15)
        entrycount += 1

    resultlist.place(x=100,y=50)

    # trigger mode to viewing once user selects an entry 
    if viewing_id != None:
        resultlist.destroy()
        return viewing_id, error_code

# Buttons go here
new_button = ctk.CTkButton(app, text="New",command=lambda: print("New consultant requested."),fg_color="#4DAB3A")
edit_button = ctk.CTkButton(app, text="Edit",command=lambda: print("Edit requested."),fg_color="#4DAB3A")
delete_button = ctk.CTkButton(app, text="Delete",command=lambda: print("Deletion requested."),fg_color="#DE503A")
search_button = ctk.CTkButton(app, text="Search",command=basicsearch,fg_color="#5550DE")
advsearch_button = ctk.CTkButton(app, text="Advanced Search...",command=lambda: print("Advanced search requested."),fg_color="#5550DE")

def set_field(entry,value):
    entry.configure(state="normal")
    entry.delete(0, "end")
    entry.insert(0, value)
    entry.configure(state="disabled")

def selection(item):
    global viewing_id
    viewing_id = item
    resultlist.destroy()
    global location
    id_list, skills_list, location = main.retrieveinfobyid(item)
    set_mode("viewing")
    set_field(id_entry, id_list[0])
    set_field(name_entry,f"{id_list[1]} {id_list[2]}")
    set_field(band_entry, str(id_list[3]))
    set_field(sector_entry, id_list[4])



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