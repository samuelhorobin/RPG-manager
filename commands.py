import os
import json
import inspect
from datetime import datetime
from prettytable import PrettyTable

import numpy as np
import matplotlib.pyplot as plt

def help():
    ''' Print names, descriptions, and parameters of all functions with parameters '''
    functions = [create_campaign, select_campaign , create]

    table = PrettyTable()
    table.field_names = ["Function Name", "Description", "Parameters"]

    for func in functions:
        func_name = func.__name__
        func_doc = func.__doc__ if func.__doc__ else "No description available."

        # Get the function parameters with their types
        params = inspect.signature(func).parameters
        param_str = ', '.join([f"{param}: {param_type}" for param, param_type in
                               [(name, param.annotation.__name__) for name, param in params.items()] if param_type is not inspect.Parameter.empty])

        if params:  # Only include functions with parameters
            table.add_row([func_name, func_doc, param_str])

    print(table)

# User functions

def create(desired_file_name: str, template_name: str):
    ''' Create a new item based on the template
        ie: create gerald default_character_template'''
    campaign = get_campaign()

    

    template_path = os.path.join("campaigns", campaign, 'templates', f'{template_name}.json')

    with open(template_path, 'r') as template_file:
                template = json.load(template_file)
                category = template["dest"]

    output_folder = os.path.join("campaigns", campaign, category)

    try:
        # Load the template
        with open(template_path, 'r') as template_file:
            template = json.load(template_file)
            template["name"]

        # Ask questions based on the template
        for key, value in template.items():
            if key == "dest": continue
            user_input = input(f"{key}: ").strip()
            if key == "tags": template[key] = value
            else: template[key] = user_input if user_input else value

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Create the JSON file with the provided information
        output_file_path = os.path.join(output_folder, f'{desired_file_name}.json')
        with open(output_file_path, 'w') as output_file:
            json.dump(template, output_file, indent=2)

        print(f"Created {output_file_path}")
    except FileNotFoundError:
        print(f"Error: Template '{template_name}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def generate_map(humidity: float = 0.5,            # Range: 0.0 to 1.0
                humidity_variance: float = 0.2,     # Range: 0.0 to 1.0
                temperature: float = 0.4,            # Range: 0.0 to 1.0
                temperature_variance: float = 0.3,    # Range: 0.0 to 1.0

                # Geographical Variables
                sea_level: float = 0.0,          # Height in meters above or below sea level
                height_peak: float = 2000.0,         # Height of the highest point in meters above sea level
                height_trough: float = -500.0,         # Depth of the lowest point in meters below sea level
                terrain_smoothness: float = 0.5,         # Range: 0.0 to 1.0: Smoothing after-effect for terrain

                # Geological Variables
                cave_density: float = 0.005,  # Number of caves or caverns per square kilometer
                volcano_presence: bool = True, # True if there are active volcanoes, False otherwise
                island_count: int = 5,          # Number of distinct islands
                flood_risk: float = 0.7,         # Measure of flood risk (0.0 to 1.0)
                geological_stability: float = 0.8, # Measure of seismic activity or stability (0.0 to 1.0)
    ):
    pass

def create_campaign(campaign_name: str):
    ''' Create a new campaign folder with specified name '''
    if not campaign_name:
        print("Error: Please provide a name for the campaign.")
        return

    campaign_folder = os.path.join("campaigns", campaign_name)

    try:
        # Create the 'campaigns' folder if it doesn't exist
        if not os.path.exists("campaigns"):
            os.makedirs("campaigns")

        # Create the campaign folder
        os.makedirs(campaign_folder)

        # Create subfolders for NPCs, characters, items, enemies, maps, item recipes, etc.
        subfolders = ['NPCs', 'characters', 'items', 'enemies', 'maps', 'item_recipes', 'templates']
        for subfolder in subfolders:
            os.makedirs(os.path.join(campaign_folder, subfolder))
            print(f"Created {subfolder}")

        # Additional folders
        additional_folders = ['logs_and_notes', 'house_rules']
        for folder in additional_folders:
            folder_path = os.path.join(campaign_folder, folder)
            os.makedirs(folder_path)
            print(f"Created {folder}")

            # Create individual .txt files for logs_and_notes, house_rules
            if folder == 'logs_and_notes':
                logs_notes_file_path = os.path.join(folder_path, "notes.txt")
                with open(logs_notes_file_path, 'w') as logs_notes_file:
                    logs_notes_file.write("Campaign Notes:\n")
                print(f"Created {logs_notes_file_path}")

            if folder == 'house_rules':
                house_rules_file_path = os.path.join(folder_path, "rules.txt")
                with open(house_rules_file_path, 'w') as house_rules_file:
                    house_rules_file.write("House Rules:\n")
                print(f"Created {house_rules_file_path}")

        # Create default templates
        create_default_templates(campaign_folder)

        # Create the 'information' file
        information_file_path = os.path.join(campaign_folder, "information.txt")
        with open(information_file_path, 'w') as info_file:
            info_file.write(f"Welcome to your campaign!\nFeel free to delete this file.\n")
            info_file.write(f"Date Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"Campaign '{campaign_name}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")

def select_campaign():
    ''' Select an existing campaign via a menu '''
    settings_path = os.path.abspath("settings.json")
    campaigns_fstring = get_campaigns_select_menu()
    campaign_count = len(campaigns_fstring.split("\n"))
    if campaign_count == 1: return None

    campaign_index = try_loop(message=f"What campaign do you want to select?\n{campaigns_fstring}",
                                conditions={"is_between": (0, campaign_count+1)})

    if int(campaign_index) == len(get_campaigns())+1:
        campaign = None
    else:
        campaign = get_campaigns()[int(campaign_index)-1]
    
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    
    settings["campaign"] = campaign

    with open(settings_path, "w") as file:
        json.dump(settings, file)
        
# Backend functions
class Invalid_Answer(Exception):
    "Answer is not correct for try_loop"
    def __init__(self, condition, parameters) -> None:
        message = f"Incorrect answer, failed to pass condition: {condition}: {parameters}"
        super().__init__(message)

def try_loop(message: str, conditions: dict, whitelisted: list = None, blacklisted: list = None, custom_exception: Exception = None):
    ''' Conditions: is_between : (val, val),
    '''
    while True:
        try:
            answer = input(f"{message}\n")


            for condition in conditions.keys():
                if condition == "is_between": 
                    if not is_between(int(answer), conditions[condition]):
                        raise Invalid_Answer(condition, conditions[condition])
            if whitelisted:
                if answer not in whitelisted:
                    raise Invalid_Answer("Not whitelisted", answer)
            if blacklisted:
                if answer in blacklisted:
                    raise Invalid_Answer("Blacklisted", answer)

            return answer
        except Exception as e:
            print(e)

def is_between(val, bounds):
    if val > bounds[0] and val < bounds[1]: return True
    else:
        return False

def create_default_templates(campaign_folder: str):
    ''' Create default templates for NPCs, characters, items, enemies, and item recipes '''
    template_folder = os.path.join(campaign_folder, 'templates')

    # Create the 'templates' folder if it doesn't exist
    if not os.path.exists(template_folder):
        os.makedirs(template_folder)

    default_templates = {
        'NPC': {
            "name": "NPC Name",
            "description": "NPC Description",
            "role": "NPC Role",
            "alignment": "NPC Alignment",
            "personality": "NPC Personality",
            "background": "NPC Background",
            "dest": "NPCs",
            "tags": []
        },
        'character': {
            "name": "Character Name",
            "race": "Character Race",
            "class": "Character Class",
            "background": "Character Background",
            "alignment": "Character Alignment",
            "level": 1,
            "hp": 10,
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
            "backstory": "Character Backstory",
            "dest": "characters",
            "tags": []
        },
        'item': {
            "name": "Item Name",
            "type": "Item Type",
            "description": "Item Description",
            "value": 0,
            "dest": "items",
            "tags": []
        },
        'enemy': {
            "name": "Enemy Name",
            "type": "Enemy Type",
            "description": "Enemy Description",
            "hp": 10,
            "attack": 5,
            "defense": 5,
            "dest": "enemies",
            "tags": []
        },
        'item_recipe': {
            "name": "Recipe Name",
            "ingredients": [],
            "result": "Resulting Item",
            "tags": []
        }
    }

    for category, template_data in default_templates.items():
        template_path = os.path.join(template_folder, f'{category}_template.json')
        with open(template_path, 'w') as template_file:
            json.dump(template_data, template_file, indent=2)

        print(f"Created {template_path}")

def list_to_numbered_fstring(input_list: list):
    return '\n'.join(f"{index + 1}: {item}" for index, item in enumerate(input_list))

def get_campaigns():
    campaigns = [f for f in os.listdir("campaigns")]
    return campaigns

def get_campaign():
    settings_path = os.path.abspath("settings.json")
    with open(settings_path, 'r') as file:
        settings = json.load(file)
        campaign = settings["campaign"]
    
    return campaign

def get_campaigns_select_menu():
    campaigns = get_campaigns()
    campaigns.append("None")
    campaigns_select_menu = list_to_numbered_fstring(campaigns)
    return campaigns_select_menu

def initialise():
    settings_path = os.path.abspath("settings.json")
    if not os.path.exists(settings_path):
        settings = {
            "campaign": None,
            "gpt-api-key": None
        }
    
        with open(settings_path, "w") as file:
            json.dump(settings, file)

    data_path = os.path.abspath("data.json")
    if not os.path.exists(data_path):
        data = {"tags" : {
    "Physical Attributes": [
        "Tangible", "Large", "Compact", "Fragile", "Flexible", "Durable", "Disposable", 
        "Biodegradable", "Industrial", "Magnetic", "Synthetic", "Unique", "Invisible", 
        "Precious", "Synthetic", "Fragile", "Compact", "Disposable", "Portable", "Mechanical", 
        "Digital", "Ancient", "Compact", "Durable", "Portable", "Magnetic", "Mechanical", 
        "Industrial", "Fragile", "Disposable", "Synthetic", "Biodegradable", "Durable", 
        "Mechanical", "Synthetic", "Durable", "Disposable", "Fragile", "Imperishable", "Versatile"
    ],
    "Functionality and Usage": [
        "Interior", "Practical", "Moving Parts", "Communication", "Transportation", "Tool", 
        "Entertainment", "System", "Technology", "Education", "Possession", "Wearable", 
        "Recreation", "Ritualistic", "Navigation", "Magnetic", "Musical", "Interactive", 
        "Personal", "Community", "Celebratory", "Recreational", "Tactical", "Eco-Friendly", 
        "Remote", "Autonomous", "Virtual", "Transformative"
    ],
    "Natural and Environmental": [
        "Organic", "Natural", "Living", "Health", "Energy", "Consumable", "Biodegradable", 
        "Sustainable", "Spiritual", "Biological", "Eco-Friendly"
    ],
    "Cultural and Social": [
        "Common", "Global", "Manufactured", "Religious", "Luxury", "Traditional", 
        "Customizable", "Community", "Cultural"
    ],
    "Emotional and Abstract": [
        "Symbolic", "Aesthetic", "Spiritual", "Mythology", "Nostalgic", "Imaginative", 
        "Mysterious", "Magical", "Supernatural", "Harmonious"
    ],
    "Time-related": [
        "Historical", "Futuristic", "Antique", "Vintage", "Ancient", "Revolutionary", 
        "Modern", "Contemporary", "Ageless", "Timeless", "Timely", "Epochal", 
        "Epoch-making", "Time-honored"
    ],
    "Color and Appearance": [
        "Vivid", "Monochromatic", "Radiant", "Glossy", "Matte", "Shiny", "Metallic", 
        "Transparent", "Opaque", "Luminous", "Translucent", "Holographic", "Iridescent", 
        "Neon", "Pastel", "Subdued", "Muted", "Bold", "Subtle", "Vibrant", "Earthy", 
        "Translucent", "Fluorescent", "Glossy", "Lustrous", "Glittering", "Sheen", 
        "Satin", "Polished", "Frosted", "Sparkling", "Gleaming", "Opalescent"
    ]}

        }
    
        with open(data_path, "w") as file:
            json.dump(data, file)

def settings_warnings():
    settings_path = os.path.abspath("settings.json")
    path_printed = False
    with open(settings_path, 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            for key, value in data.items():
                if value is None:
                    if not path_printed:
                        print(f"Problem(s) at {settings_path}:")
                        path_printed = True
                    print(f"Warning: Value for key '{key}' is None.")

if __name__ == "__main__":
    initialise()