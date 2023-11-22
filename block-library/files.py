import os
import json

def generate_file_structure(directory, i):
    if(i != 0):
        file_structure = {
            'label': os.path.basename(directory),
            'children': {}
        }
    else:
        file_structure = {
        }

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            if(i != 0):
                file_structure['children'][item] = generate_file_structure(item_path, i+1)
            else:
                file_structure[item] = generate_file_structure(item_path, i+1)
        else:
            if(item.endswith('.json')):
                file_structure['children'][item[:-5]] = {'label': os.path.splitext(item)[0]}

    return file_structure

def write_json_file(file_structure, output_file='./frontend/src/VisualCircuit-resources/block-library/file_structure.json'):
    with open(output_file, 'w') as json_file:
        json.dump(file_structure, json_file, indent=4)

if __name__ == "__main__":
    directory_to_scan = "/home/toshan/VisualCircuit/frontend/src/VisualCircuit-resources/block-library/"

    if os.path.isdir(directory_to_scan):
        file_structure = generate_file_structure(directory_to_scan, 0)
        write_json_file(file_structure)
        print(f"File structure JSON created successfully at file_structure.json")
    else:
        print("Invalid directory path. Please provide a valid directory.")
