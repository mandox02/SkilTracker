import customtkinter as ctk
import mainscript as main
import string

app = ctk.CTk()
app.title("SkilTracker v0.6")
app.geometry("600x500+100+100")
app.resizable(False,False)
app_x = app.winfo_x()
app_y = app.winfo_y()

def temptimer():
    global app_x
    global app_y
    app_x = app.winfo_x()
    app_y = app.winfo_y()
    app.update()
    print(f"X: {app_x}, Y: {app_y}")
    print(current_mode)

    app.after(1000,temptimer)

current_mode = "idle"
viewing_id = None
resultlist = None
location = None
valid_bands = [str(n) for n in range(0,11)]
existing_bands = [str(n) for n in main.existing_bands]
existing_sectors = [str(n) for n in main.existing_sectors]
error_code = main.error_codes["0"]
popup = None

skillf = None
catf = None
bandf = None
sectorf = None
catf_toggle = None

# MAIN WINDOW

def set_mode(newmode):
    global current_mode
    current_mode = newmode

# Labels, Entry boxes and the skills frame go here
searchbyid_label = ctk.CTkLabel(app, text="Search by ID or Name:")
searchbyid_entry = ctk.CTkEntry(app)
id_label = ctk.CTkLabel(app, text="ID:")
id_entry = ctk.CTkEntry(app, state="disabled")
name_entry = ctk.CTkEntry(app,placeholder_text="Name", state="disabled")
ln_entry = ctk.CTkEntry(app,placeholder_text="Last Name", state="disabled")
band_label = ctk.CTkLabel(app, text="Band:")
band_dropdown = ctk.CTkOptionMenu(app,values=valid_bands, state="disabled")
band_dropdown.set("")
sector_label = ctk.CTkLabel(app, text="Sector:")
sector_entry = ctk.CTkEntry(app, state="disabled")
skills_frame = ctk.CTkFrame(app)
for i in range(3):
    label = ctk.CTkLabel(skills_frame,text=f"Category {i+1}")
    label.grid(row=0,column=i)

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
    error_code = main.error_codes["0"]
    term = searchbyid_entry.get()
    print(f"Read term as {term}")
    id = None
    name = None
    names = []
    ids = []

    if term == "all":
        id_list = main.retrieveall()
    else:
        # Return error for invalid characters or blank search
        if term == "":
            error_code = main.error_codes["2"]
            make_popup(error_code)
            return False

        print("entry is not empty, proceed")
        
        if any(char for char in term if char in string.punctuation):
            error_code = main.error_codes["3a"]
            make_popup(error_code)
            return False

        print("entry has no special characters, proceed")

        # Check whether the search is for a name or ID and find all possible entries. 
        id_list = main.basesearch(term)
        print("got id_list, printing: ", id_list)

    if id_list == []:
        error_code = main.error_codes["3"]
        make_popup(error_code)
        return False

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
    for index, item in enumerate(ids):
        selectbtn = ctk.CTkButton(resultlist, text=f"{ids[entrycount]} | {names[entrycount]}",command=lambda item=item: selection(item))
        selectbtn.grid(row=index, pady=5, sticky="ew")
        entrycount += 1

    resultlist.place(x=100,y=40)

    return True

def set_field(entry,value,enableflag=False):
    entry.configure(state="normal")
    entry.delete(0, "end")
    if value == None or value == "":
         entry.insert(0,"")
    else: entry.insert(0, value)
    if enableflag == False:
        entry.configure(state="disabled")

def selection(item):
    print("Selection ran.")
    global viewing_id
    viewing_id = item
    resultlist.destroy()
    if popup != None:
        popup.destroy()
    display_info(item)

def display_info(item):
    global location
    id_list, skills_list, location = main.retrieveinfobyid(item)
    set_mode("view")
    set_field(id_entry, id_list[0])
    set_field(name_entry, id_list[1])
    set_field(ln_entry, id_list[2])
    band_dropdown.set(str(id_list[3]))
    band_dropdown.configure(state="disabled")
    set_field(sector_entry, id_list[4])

    cat1_skills = skills_list[1:3]
    cat2_skills = skills_list[3:8]
    cat3_skills = skills_list[8:13]
    for i, entry in enumerate(cat1_entries):
        set_field(entry,cat1_skills[i])
    for i, entry in enumerate(cat2_entries):
            set_field(entry,cat2_skills[i])
    for i, entry in enumerate(cat3_entries):
            set_field(entry,cat3_skills[i])

    edit_button.configure(state="normal",fg_color="#4DAB3A")
    delete_button.configure(state="normal",fg_color="#DE503A")

def clear_all(flag):
    set_field(id_entry, None, flag)
    set_field(name_entry, None, flag)
    set_field(ln_entry, None, flag)
    band_dropdown.set("")
    if flag == True:
        band_dropdown.configure(state="normal")
    else: band_dropdown.configure(state="disabled")
    set_field(sector_entry, None, flag)
    
    cat1_skills = [None,None]
    cat2_skills = [None,None,None,None,None]
    cat3_skills = [None,None,None,None,None]
    for i, entry in enumerate(cat1_entries):
        set_field(entry,cat1_skills[i], flag)
    for i, entry in enumerate(cat2_entries):
            set_field(entry,cat2_skills[i], flag)
    for i, entry in enumerate(cat3_entries):
            set_field(entry,cat3_skills[i], flag)

def save_to_excel():
    id = id_entry.get()
    print(id)
    name = name_entry.get()
    print(name)
    ln = ln_entry.get()
    print(ln)
    try:
        band = int(band_dropdown.get())
        if band == 0:
            band = ""
    except ValueError:
        band = ""
    print(band)
    sector = sector_entry.get()
    print(sector)
    cat1_skills = []
    cat2_skills = []
    cat3_skills = []
    for i, entry in enumerate(cat1_entries):
        cat1_skills.append(entry.get())
    for i, entry in enumerate(cat2_entries):
        cat2_skills.append(entry.get())
    for i, entry in enumerate(cat3_entries):
        cat3_skills.append(entry.get())

    print(cat1_skills)
    print(cat2_skills)
    print(cat3_skills)

    if current_mode == "new":
        success, error_code = main.saveinfo(id,name,ln,band,sector,cat1_skills,cat2_skills,cat3_skills)
    elif current_mode == "edit":
        success, error_code = main.editinfo(id,name,ln,band,sector,cat1_skills,cat2_skills,cat3_skills)

    if success:
        clear_all(False)
        edit_button.configure(text="Edit",command=edit_entry,state="disabled")
        delete_button.configure(text="Delete",command=ask_delete,state="disabled",fg_color="#925C54")
        new_button.configure(state="enabled",fg_color="#4DAB3A")
        set_mode("idle")
        searchbyid_entry.configure(state="normal")
        search_button.configure(state="normal",fg_color="#5550DE")
        advsearch_button.configure(state="normal",fg_color="#5550DE")
    else:
        print("Editing failed.")
        make_popup(error_code)

def new_entry():
    clear_all(True)
    set_mode("new")
    new_button.configure(state="disabled",fg_color="#46753D")
    edit_button.configure(state="normal",text="Save",command=save_to_excel,fg_color="#4DAB3A")
    delete_button.configure(state="normal",text="Cancel",command=cancel,fg_color="#DE503A")
    searchbyid_entry.configure(state="disabled")
    search_button.configure(state="disabled",fg_color="#615FA0")
    advsearch_button.configure(state="disabled",fg_color="#615FA0")

def edit_entry():
    set_mode("edit")
    print(id_entry.get())
    name_entry.configure(state="normal")
    ln_entry.configure(state="normal")
    sector_entry.configure(state="normal")
    band_dropdown.configure(state="normal")
    for entry in cat1_entries:
        entry.configure(state="normal")
    for entry in cat2_entries:
        entry.configure(state="normal")
    for entry in cat3_entries:
        entry.configure(state="normal")
    new_button.configure(state="disabled",fg_color="#46753D")
    edit_button.configure(text="Save",command=save_to_excel)
    delete_button.configure(text="Cancel",command=cancel)
    searchbyid_entry.configure(state="disabled")
    search_button.configure(state="disabled",fg_color="#615FA0")
    advsearch_button.configure(state="disabled",fg_color="#615FA0")

def cancel():
    new_button.configure(state="enabled",fg_color="#4DAB3A")
    searchbyid_entry.configure(state="normal")
    search_button.configure(state="normal",fg_color="#5550DE")
    advsearch_button.configure(state="normal",fg_color="#5550DE")
    delete_button.configure(text="Delete",command=ask_delete)
    edit_button.configure(text="Edit",command=edit_entry)
    if current_mode == "new":
        clear_all(False)
        set_mode("idle")
        edit_button.configure(state="disabled")
        delete_button.configure(state="disabled",fg_color="#925C54")
    elif current_mode == "edit":
        display_info(viewing_id) 

def make_popup(message,warning=True):
    global popup
    popup = ctk.CTkToplevel(app)
    popup.lift()
    popup.grab_set()
    if warning:
        popup.title("Warning")
    else: popup.title("Confirm Deletion")
    x = app_x + 100
    y = app_y + 50
    popup.geometry(f'400x200+{x}+{y}')
    popup.resizable(False,False)
    label = ctk.CTkLabel(popup,text=message)
    cancelbtn = ctk.CTkButton(popup,command=lambda: popup.destroy())
    confirmbtn = ctk.CTkButton(popup,text="Confirm",command=confirm)
    emptylabel = ctk.CTkLabel(popup,text="")
    label.pack(anchor="n")
    emptylabel.pack(anchor="center")
    if warning == True:
        cancelbtn.configure(text="OK")
        cancelbtn.pack(anchor="s")
    else:
        cancelbtn.configure(text="Cancel")
        cancelbtn.pack(side="left")
        confirmbtn.pack(side="right")

def ask_delete():
    make_popup("Are you sure you want to delete this candidate?",False)

def confirm():
    popup.destroy() 
    print("Deleting entry ID", viewing_id)
    output, error_code = main.deleteinfo(viewing_id)

    if output == False:
        make_popup(error_code)
    else:
        clear_all(False)
        edit_button.configure(text="Edit",command=edit_entry,state="disabled")
        delete_button.configure(text="Delete",command=ask_delete,state="disabled",fg_color="#925C54")
        new_button.configure(state="enabled",fg_color="#4DAB3A")
        set_mode("idle")
        searchbyid_entry.configure(state="normal")
        search_button.configure(state="normal",fg_color="#5550DE")
        advsearch_button.configure(state="normal",fg_color="#5550DE")
        make_popup("Candidate deleted.")

def adv_search():

    global popup
    global skillf
    global catf
    global bandf
    global sectorf
    global catf_toggle
    category = [str(n) for n in range(1,4)]
    popup = ctk.CTkToplevel(app)
    popup.lift()
    popup.grab_set()
    popup.title("Advanced Search")
    x = app_x + 150
    y = app_y + 50
    popup.geometry(f'300x400+{x}+{y}')
    popup.resizable(False,False)
    label = ctk.CTkLabel(popup,text="Find a candidate by...")
    searchbtn = ctk.CTkButton(popup,text="Search",command=advsearch_exe)
    cancelbtn = ctk.CTkButton(popup,text="Cancel",command=lambda: popup.destroy())
    label.grid(row=0,column=0,columnspan=2)

    skillf_label = ctk.CTkLabel(popup,text="Skill:")
    skillf = ctk.CTkEntry(popup)
    catf_label = ctk.CTkLabel(popup,text="Category:")
    catf_toggle = ctk.CTkCheckBox(popup,text="")
    catf = ctk.CTkOptionMenu(popup,values=category,width=50)
    bandf_label = ctk.CTkLabel(popup,text="Band:")
    bandf = ctk.CTkOptionMenu(popup,values=existing_bands)
    sectorf_label = ctk.CTkLabel(popup,text="Sector:")
    sectorf = ctk.CTkOptionMenu(popup,values=existing_sectors)

    global resultlist
    resultlist= ctk.CTkScrollableFrame(popup)

    skillf_label.grid(row=1,column=0)
    skillf.grid(row=1,column=1)
    catf_label.grid(row=2,column=0)
    catf_toggle.grid(row=2,column=1)
    catf.grid(row=2,column=1)
    bandf_label.grid(row=3,column=0)
    bandf.grid(row=3,column=1)
    sectorf_label.grid(row=4,column=0)
    sectorf.grid(row=4,column=1)
    searchbtn.grid(row=5,column=0)
    cancelbtn.grid(row=5,column=1)
    resultlist.grid(row=6,column=0,columnspan=2)

def advsearch_exe():

    skill = skillf.get()
    if catf_toggle.get() == 1:
        cat = catf.get()
    else: cat = ""
    try:
        band = int(bandf.get())
        if band == 0:
            band = ""
    except ValueError:
        band = ""

    if sectorf.get() == "0":
        sector = ""
    else: sector = sectorf.get()

    id = None
    name = None
    names = []
    ids = []

    id_list, suberror = main.advancedsearch(skill,cat,band,sector)

    print(id_list)
    id_list = [item for sublist in id_list for item in sublist]
    print(id_list)

    if suberror != main.error_codes["0"]:
        make_popup(suberror)
        return False

    for item in id_list:
        list1, list2, location = main.retrieveinfobyid(item)
        print(list1)
        print(list2)
        print(location)
        name = list1[1] + " " + list1[2]
        id = list1[0]
        names.append(name)
        ids.append(id)

    # Show the list to the user and wait for it to receive a response (Yes, copied from above)
    global resultlist
    entrycount = 0

    for index, item in enumerate(ids):
        selectbtn = ctk.CTkButton(resultlist, text=f"{ids[entrycount]} | {names[entrycount]}",command=lambda item=item: selection(item))
        selectbtn.grid(row=index, pady=5, sticky="ew")
        entrycount += 1




# delete color when enabled should be fg_color="#DE503A"

# Buttons go here
new_button = ctk.CTkButton(app, text="New",command=new_entry,fg_color="#4DAB3A")
edit_button = ctk.CTkButton(app, text="Edit",command=edit_entry,fg_color="#46753D",state="disabled")
delete_button = ctk.CTkButton(app, text="Delete",command=ask_delete,fg_color="#925C54",state="disabled")
search_button = ctk.CTkButton(app, text="Search",command=basicsearch,fg_color="#5550DE")
advsearch_button = ctk.CTkButton(app, text="Advanced Search...",command=adv_search,fg_color="#5550DE")

# Activation goes here
searchbyid_label.grid(row=0,column=0)
searchbyid_entry.grid(row=0,column=1)
search_button.grid(row=0,column=2)
advsearch_button.grid(row=0,column=3)

id_label.grid(row=1,column=0)
id_entry.grid(row=1,column=1)
name_entry.grid(row=1,column=2)
ln_entry.grid(row=1,column=3)

band_label.grid(row=2,column=0)
band_dropdown.grid(row=2,column=1)
sector_label.grid(row=2,column=2)
sector_entry.grid(row=2,column=3)

app.grid_rowconfigure(3,minsize=40) 

skills_frame.grid(row=4,column=1,columnspan=3)

app.grid_rowconfigure(5,minsize=40) 

new_button.grid(row=6,column=0)
edit_button.grid(row=6,column=1)
delete_button.grid(row=6,column=2)

temptimer()

app.mainloop()