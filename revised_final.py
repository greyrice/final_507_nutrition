import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import random
import json
import requests

class Nutrient:
    def __init__(self):
        self.graph = nx.Graph()

    def add_food(self, nutrient_type, food_name, protein, fat, carbs):
        self.graph.add_node(food_name, nutrient_type=nutrient_type, protein=protein, fat=fat, carbs=carbs)
        self.graph.add_node(nutrient_type)  # Nutrient type is also a node
        self.graph.add_edge(nutrient_type, food_name)

    def display_info(self):
        for node, data in self.graph.nodes(data=True):
            if "nutrient_type" in data:
                nutrient_type = data["nutrient_type"]
                print(f"{node} ({nutrient_type}):", end=" ")
                if "protein" in data:
                    print(f"Protein: {data['protein']}g", end=" ")
                if "fat" in data:
                    print(f"Fat: {data['fat']}g", end=" ")
                if "carbs" in data:
                    print(f"Carbs: {data['carbs']}g", end=" ")
                print()

    def display_graph(self):
        plt.figure(figsize=(50, 25))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True,font_size=10, font_weight='bold', node_size=1000, node_color='skyblue')

        # Add nutritional information as labels to nodes
        labels = {}
        for node, data in self.graph.nodes(data=True):
            label = node
            if "nutrient_type" in data:
                label += f"\nType: {data['nutrient_type']}"
            if "protein" in data:
                label += f"\nProtein: {data['protein']}g"
            if "fat" in data:
                label += f"\nFat: {data['fat']}g"
            if "carbs" in data:
                label += f"\nCarbs: {data['carbs']}g"
            labels[node] = label

        nx.draw_networkx_labels(self.graph, pos, labels, font_size=8, verticalalignment="center")

        plt.title("Nutrient Graph")
        plt.show()

    def search_food(self, start_food, target_food):
        visited = set()
        queue = deque([(start_food, None)])

        while queue:
            current_food, parent = queue.popleft()
            food_list = [component.strip().lower() for component in target_food.split(',')]
            if any(current_food.lower() for component in food_list):
                if parent is not None and parent != start_food:
                    print(f"{target_food} not directly connected to {start_food}.")
                else:
                    print(f"Found {target_food}!")#ling this to another class to display protin fat or carbs
                return

            visited.add(current_food)

            for neighbor in self.graph.neighbors(current_food):
                if neighbor not in visited:
                    queue.append((neighbor, current_food))

        print(f"{target_food} not found in the graph.")
  
    def get_foods_above_nutrient_level(self, nutrient, nutrient_num=10, num_foods=10):
        foods = []
        for node, data in self.graph.nodes(data=True):
            try:
                if nutrient in data:
                    if data[nutrient] > nutrient_num:
                        foods.append(node)
            except:
                continue
                    
                
        if not foods:
            print(f"No foods found for nutrient type: {nutrient} with nutrient values above {nutrient_num}")
            return

        random_foods = random.sample(foods, min(num_foods, len(foods)))
        return random_foods
    

def getAPI(food_names):
    for i in food_names:
        url = f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key=90Vy6IBfXTpSqFEVx5JMTam3r55ftnphWU0yKagh&query={i}&dataType=Foundation&pageSize=1'
        result = requests.get(url)
        data = result.json()
        return data

def get_food_nutrient(food_data):
    ##append element into a list and use that to make a list 
    data = food_data
    
    print((f"{data['Name']} has {data['Protein']}g protein{data['Fat']}g Fat and {data['Carbs']}g Carbs"))
    return {
                'Name': data['Name'],
                'Protein': data['Protein'],
                'Fat': data['Fat'],
                'Carbs': data['Carbs']
            }
        
            

def read_data_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return



def update_data(new_data, file_path):
    # Load existing data from the file
    try:
        print("uppend")
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
            existing_data.append(new_data[0])
            with open(file_path, 'w') as file:
                json.dump(existing_data, file, indent=2)
                return
    except (FileNotFoundError , AttributeError) :
        # If the file doesn't exist, initialize with an empty dictionary
        existing_data = {}

    try:
        print("update")
        with open(file_path, 'r') as file:
            existing_data = [json.load(file)]
            new = existing_data.update(new_data)
            with open(file_path, 'w') as file:
                json.dump(new, file, indent=2)
                return
    except (FileNotFoundError , AttributeError):
        # If the file doesn't exist, initialize with an empty dictionary
        existing_data = {}

        
        with open(file_path, 'w') as file:
                json.dump(new_data, file, indent=2)
    
def clean_data(data):
    data1={"Name":data["foods"][0]["description"],"Protein":None,"Fat":None,"Carbs":None}
    for i in data["foods"][0]['foodNutrients']:
        if i["nutrientNumber"] == "203": #203 protein 204 fat 205 carbs
            if float(i["value"])<0:
                data1["Protein"] = 0
            else:
                data1["Protein"] = i['value']
        if i["nutrientNumber"] == "204":
            if float(i["value"])<0:
                data1["Fat"] = 0
            else:
                data1["Fat"] = i['value']
        if i["nutrientNumber"] == "205":
            if float(i["value"])<0:
                data1["Carbs"] = 0
            else:
                data1["Carbs"] = i['value']
                
    return data1
def clean_database(data):
    list1=[]
   
    for i in data["FoundationFoods"]:
        data1={"Name":None,"Protein":None,"Fat":None,"Carbs":None}
        data1["Name"] = i['description']
        for k in i['foodNutrients']:
            
            nutrient_number = k["nutrient"]["number"]
            if nutrient_number == "203": #203 protein 204 fat 205 carbs   
                
                data1["Protein"] = k["amount"]
            if nutrient_number == "204":
             
                data1["Fat"] = k["amount"]
            if nutrient_number == "205":
              
                data1["Carbs"] = k["amount"]
            
            
        list1.append(data1)
    print("clean_database complete")
    return list1

def category_food(data):
    new_list = []

    for item in data:
        food_name = item["Name"]
        protein = item.get("Protein", 0)
        fat = item.get("Fat", 0)
        carbs = item.get("Carbs", 0)
        
        if protein ==None or protein< 0:
            protein = 0
        if fat == None or fat <0:
            fat = 0
        if carbs == None or carbs < 0:
            carbs = 0
        if protein > 1:
            new_list.append(("Protein", food_name, protein, fat, carbs))

        if fat > 1:
            new_list.append(("Fat", food_name, protein, fat, carbs))

        if carbs > 1:
            new_list.append(("Carbs", food_name, protein, fat, carbs))
    print("category food complete")
    return new_list

def binary_search_nutrients(data, target_name):#for list
    left, right = 0, len(data) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_item = data[mid]
        print(target_name.lower(),mid_item['Name'].lower())
        if target_name.lower() in mid_item['Name'].lower() :
            return {
                'Name': mid_item['Name'],
                'Protein': mid_item.get('Protein', None),
                'Fat': mid_item.get('Fat', None),
                'Carbs': mid_item.get('Carbs', None)
            }
        elif mid_item['Name'].lower() < target_name.lower():
            left = mid + 1
        else:
            right = mid - 1

    return None










# Example usage:
if __name__ == "__main__":
    nutrient_tracker = Nutrient()