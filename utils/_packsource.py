import os
import zipfile

ROOT_FOLDER = r'C:\Data\Dev\Payload\foliomark3'
UTILS_FOLDER = os.path.join(ROOT_FOLDER, 'utils')
ZIP_FILE_NAME = 'source.zip'

FILE_TYPES = ['.js', '.jsx', '.ts', '.tsx', '.prisma', '.json', '.md', '.yml', '.yaml', '.sh', '.scss', '.css']
EXCLUDE_FOLDERS = ['.next', 'node_modules', '.vscode', '.git']
EXCLUDE_FILES = ['package-lock.json', '*.log', '*.lock', '*.env', '*.test.js', '*.spec.js', '*.map', 'pnpm-lock.yaml', 'pnpm-workspace.yaml']
EXCLUDE_SUBDIRS = [os.path.join('src', 'app', '(payload)')]

def get_source_files(root_dir):
    file_paths = []
    
    for root, dirs, files in os.walk(root_dir):
        # Exclude folders
        dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS]
        
        # Exclude specific subdirectories
        if any(subdir in root for subdir in EXCLUDE_SUBDIRS):
            continue
        
        for file in files:
            if file.lower().endswith(tuple(FILE_TYPES)) and file not in EXCLUDE_FILES:
                file_path = os.path.join(root, file)
                
                # Get relative path to root folder
                relative_path = os.path.relpath(file_path, ROOT_FOLDER) 
                
                file_paths.append(relative_path)
                
    return file_paths

def write_source_files(file_paths, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for file in file_paths:
            f.write(f'// {file}\n')
            with open(os.path.join(ROOT_FOLDER, file), 'r', encoding='utf-8') as source_file:
                f.write(source_file.read())
            f.write('\n\n')

def zip_files(file_paths, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for file in file_paths:
            zip_file.write(os.path.join(ROOT_FOLDER, file), file)

if __name__ == '__main__':
    source_files = get_source_files(ROOT_FOLDER)
    
    # Write source files to a single file
    single_file_path = os.path.join(UTILS_FOLDER, 'all_source_files.txt')
    write_source_files(source_files, single_file_path)
    
    # Zip the single file
    zip_files([single_file_path], os.path.join(UTILS_FOLDER, ZIP_FILE_NAME))