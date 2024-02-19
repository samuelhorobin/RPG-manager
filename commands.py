import os
import json
import inspect
from datetime import datetime
from prettytable import PrettyTable

def help():
    ''' Print names, descriptions, and parameters of all functions with parameters '''
    functions = [create_campaign, create]

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

def create(campaign: str, category: str, desired_file_name: str, template_name: str):
    ''' Create a new item based on the template
        ie: create wonderful_campaign characters gerald default_character_template'''
    template_path = os.path.join("campaigns", campaign, 'templates', f'{template_name}.json')
    output_folder = os.path.join("campaigns", campaign, category)

    try:
        # Load the template
        with open(template_path, 'r') as template_file:
            template = json.load(template_file)

        # Ask questions based on the template
        for key, value in template.items():
            user_input = input(f"{key}: ").strip()
            template[key] = user_input if user_input else value

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

def create_default_templates(campaign_folder: str):
    ''' Create default templates for NPCs, characters, items, enemies, and item recipes '''
    template_folder = os.path.join(campaign_folder, 'templates')

    # Create the 'templates' folder if it doesn't exist
    if not os.path.exists(template_folder):
        os.makedirs(template_folder)

    default_templates = {
        'NPCs': {
            "name": "NPC Name",
            "description": "NPC Description",
            "role": "NPC Role",
            "alignment": "NPC Alignment",
            "personality": "NPC Personality",
            "background": "NPC Background"
        },
        'characters': {
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
            "equipment": [],
            "features_and_traits": [],
            "backstory": "Character Backstory"
        },
        'items': {
            "name": "Item Name",
            "type": "Item Type",
            "description": "Item Description",
            "value": 0
        },
        'enemies': {
            "name": "Enemy Name",
            "type": "Enemy Type",
            "description": "Enemy Description",
            "hp": 10,
            "attack": 5,
            "defense": 5
        },
        'item_recipes': {
            "name": "Recipe Name",
            "ingredients": [],
            "result": "Resulting Item"
        }
    }

    for category, template_data in default_templates.items():
        template_path = os.path.join(template_folder, f'{category}_template.json')
        with open(template_path, 'w') as template_file:
            json.dump(template_data, template_file, indent=2)

        print(f"Created {template_path}")

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

if __name__ == "__main__":
    # Add create_campaign to the list of functions
    functions = [create_campaign, create]
    help()

