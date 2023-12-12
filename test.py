import tkinter as tk
from tkinter import ttk
import revised_final as rf


def on_first_button_click():
    label.config(text="Do you want to start a new database, or you want to use a previously installed local database")

    # Create two new buttons
    global new_button1, new_button2
    new_button1 = tk.Button(root, text="New database", command=on_new_button1_click)
    new_button1.pack(pady=10)
    new_button2 = tk.Button(root, text="Previous database", command=on_new_button2_click)
    new_button2.pack(pady=10)

    # Destroy the initial button
    button.destroy()

def on_new_button1_click():
    label.config(text="You are using a new database. Please make sure you have an internet connection.")
    create_input_widgets(1)
    # Destroy the "New database" and "Previous database" buttons
    new_button1.destroy()
    new_button2.destroy()

def on_new_button2_click():
    label.config(text="You are using a local database. If your input is not in the local database, it will search online.")
    create_input_widgets(2)
    # Destroy the "New database" and "Previous database" buttons
    new_button1.destroy()
    new_button2.destroy()

def create_input_widgets(flag):
    create_tabs(["search food","find food base on nutrient","calculate total","display database"])
    if flag == 1:##new
        global new_data
        new_data = rf.read_data_from_json("new.json")
        categorized = rf.category_food(new_data)
        for nutrient_type, food_name, protein, fat, carbs in categorized:
            nutrient_tracker.add_food(nutrient_type, food_name, protein, fat, carbs)
        pass
    if flag ==2:##local
        global data
        data = rf.read_data_from_json("local.json")
        categorized = rf.category_food(data)
        for nutrient_type, food_name, protein, fat, carbs in categorized:
            nutrient_tracker.add_food(nutrient_type, food_name, protein, fat, carbs)
        pass

def create_tabs(tab_names):
    # Create a notebook (tabbed window)

    # Create tabs
    for i, tab_name in enumerate(tab_names):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=tab_name)
        if i ==0:
        # Create a label in each tab
            tab_label = tk.Label(tab, text=f"Enter the food you want to search:")
            tab_label.pack(padx=10, pady=10)
            tab_entry = tk.Entry(tab)
            tab_entry.pack(pady=5)
            tab_button = tk.Button(tab, text=f"Search food", command=lambda entry=tab_entry: handle_tab_button(1, entry))
            tab_button.pack(pady=10)
            
        if i ==1:
            tab_label = tk.Label(tab, text=f"find food base on nutrient:")
            tab_label.pack(padx=10, pady=10)
            tab_button = tk.Button(tab, text=f"Food have more Protein", command=lambda i=i: handle_tab_button(2))
            tab_button.pack(pady=10)
            tab_button = tk.Button(tab, text=f"Food have more Fat", command=lambda i=i: handle_tab_button(3))
            tab_button.pack(pady=10)
            tab_button = tk.Button(tab, text=f"Food have more Carbs", command=lambda i=i: handle_tab_button(4))
            tab_button.pack(pady=10)
            
        if i ==2:
             tab_label = tk.Label(tab, text=f"calculate total nutrient")
             tab_label.pack(padx=10, pady=10)
             tab_entry = tk.Entry(tab,text = "enter all the food you want to calculate")
             tab_entry.pack(pady=5)
             tab_button = tk.Button(tab, text=f"Search food", command=lambda entry=tab_entry: handle_tab_button(5, entry))
             tab_button.pack(pady=10)
        if i ==3:
             tab_label = tk.Label(tab, text=f"display my local database")
             tab_label.pack(padx=10, pady=10)
             tab_button = tk.Button(tab, text=f"Display", command=lambda i=i: handle_tab_button(6))
             tab_button.pack(pady=10)


 

def handle_tab_button(button,entry=None):

    if button == 1 and entry is not None:
        
        try: 
            sorted_data = sorted(data,key=lambda x: x['Name'])
        except:
            sorted_data = sorted(new_data,key=lambda x: x['Name'])
        result = rf.binary_search_nutrients(sorted_data, entry.get())
        if result:
            label_tab.config(text=f"{rf.get_food_nutrient(result)}")
        else:
            if " " in entry.get():
                name = entry.get().replace(" ", "%20")
                result = rf.clean_data(rf.getAPI([name]))
                rf.update_data([result],"new.json")
                label_tab.config(text=f"{rf.get_food_nutrient(result)}")
            if " " not in entry.get():
                name = entry.get()
                result = rf.clean_data(rf.getAPI([name]))
                rf.update_data([result],"new.json")
                label_tab.config(text=f"{rf.get_food_nutrient(result)}")
            else:
                label_tab.config(text=f"did not find{entry.get()}")

    if button == 2:
        random_protein_foods = nutrient_tracker.get_foods_above_nutrient_level('protein')
        label_tab.config(text=f"{random_protein_foods}")
    if button ==3:
        random_protein_foods = nutrient_tracker.get_foods_above_nutrient_level('fat')
        label_tab.config(text=f"{random_protein_foods}")
    if button ==4:
        random_protein_foods = nutrient_tracker.get_foods_above_nutrient_level('carbs')
        label_tab.config(text=f"{random_protein_foods}")
    if button == 5 and entry is not None:
        input1 = str(entry.get())
        print(input1)
        name = input1.split(",")
        print(name)
        try: 
            protein = 0
            fat = 0
            carbs = 0
            sorted_data = sorted(data,key=lambda x: x['Name'])
            for i in name:
                print(i+"ajsfkljasklfaklsfjj")
                result = rf.binary_search_nutrients(sorted_data, i)
                print(protein, fat, carbs)
                if result:
                    protein += float(result["Protein"])
                    fat += float(result["Fat"])
                    carbs += float(result["Carbs"])
                else:
                    name = i
                    result = rf.clean_data(rf.getAPI([name]))
                    search = rf.get_food_nutrient(result)
                    protein += float(search["Protein"])
                    fat += float(search["Fat"])
                    carbs += float(search["Carbs"])
                print(protein, fat, carbs)
            
            label_tab.config(text=f"total protein: {round(protein,2)}g, total fat is: {round(fat,2)}g, total carbs is: {round(carbs,)}g")
                    

        except:
            sorted_data = sorted(new_data,key=lambda x: x['Name'])
            protein = 0
            fat = 0
            carbs = 0
            for i in name:
                print(i+"ajsfkljasklfaklsfjj")
                result = rf.binary_search_nutrients(sorted_data, i)
                print(protein, fat, carbs)
                if result:
                    protein += float(result["Protein"])
                    fat += float(result["Fat"])
                    carbs += float(result["Carbs"])
                else:
                    name = i
                    result = rf.clean_data(rf.getAPI([name]))
                    search = rf.get_food_nutrient(result)
                    protein += float(search["Protein"])
                    fat += float(search["Fat"])
                    carbs += float(search["Carbs"])
                print(protein, fat, carbs)
            
            label_tab.config(text=f"total protein: {round(protein,2)}g, total fat is: {round(fat,2)}g, total carbs is: {round(carbs,)}g")
        
            
            
    if button == 6:
        nutrient_tracker.display_graph()

    

# Create the main window
root = tk.Tk()
root.title("Nutrient Finder")

# Set the window size
# window_width = 450
# window_height = 500
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# x_coordinate = (screen_width - window_width) // 2
# y_coordinate = (screen_height - window_height) // 2
# root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


# Create the initial button
button = tk.Button(root, text="Start", command=on_first_button_click)
button.pack(pady=10)

# Create a label
initial_text = "Welcome Nutrient Finder, click the button to start finding some food you want to search"
label = tk.Label(root, text=initial_text, wraplength=400)  # Set wraplength to the desired maximum width
label.pack(pady=10)

# Declare new_button1 and new_button2 outside of the functions to make them accessible for destruction
new_button1 = None
new_button2 = None
label_tab = tk.Label(root, text="")
label_tab.pack(pady=10)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)
# Start the main loop
ori = rf.read_data_from_json("foundationDownload.json")
database=rf.clean_database(ori)
rf.update_data(database,"local.json")
nutrient_tracker = rf.Nutrient()
root.mainloop()