import os
import subprocess

folder_path = r'\\fs1\Common\Quality\08511 - Preventive Maintenance'

for filename in os.listdir(folder_path):
    if filename.endswith('.oxps'):
        file_path = os.path.join(folder_path, filename)
        converted_filename = filename.replace('.oxps', '_Converted.xps')
        converted_file_path = os.path.join(folder_path, converted_filename)
        
        # Corrected PowerShell command
        command = f'powershell -Command "Start-Process -FilePath \\"{file_path}\\" -ArgumentList \\"{converted_file_path}\\""'
        subprocess.run(command, shell=True)
