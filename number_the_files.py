import os

def number_the_files(folder_path):
    
    file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('.csv')])  # ←
    for i, file_name in enumerate(file_list):
        
        new_file_name = f"generated_{i:03}.csv"  # ←
        
        os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))

# Specify the folder path here
folder_path = 'D:/-programs-/Copilot_with_GUI/Test/output/generate_0_99'
number_the_files(folder_path)