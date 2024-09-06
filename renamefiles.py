import os

folder_path = r'K:\Quality\08511 - Preventive Maintenance'

for filename in os.listdir(folder_path):
    if 'Converted' in filename:
        new_filename = filename.replace('[Converted]', '')
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))