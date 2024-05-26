import os

ROOT_FOLDER = r'C:\Data\Dev\Fullstack\Next-Portfolio'

FILE_TYPES = ['.js', '.ts', '.tsx', '.prisma', '.json']
INCLUDE_FOLDERS = ['components', 'components/vapi']
EXCLUDE_FOLDERS = ['.next', 'node_modules', '.vscode', '.git']


def get_source_files(root_dir):
    file_paths = []
    
    for root, dirs, files in os.walk(root_dir):
        if any(folder in root for folder in EXCLUDE_FOLDERS):
            continue
            
        for file in files:
            if file.lower().endswith(tuple(FILE_TYPES)):
                file_path = os.path.join(root, file)
                
                # Check if 'vapi' is in the full path of the file
                if 'vapi' in file_path.lower():
                    # Get relative path to root folder
                    relative_path = os.path.relpath(file_path, ROOT_FOLDER) 
                    
                    file_paths.append(relative_path)
                
    return file_paths

def merge_files(file_paths, output_path):
    with open(output_path, 'w') as output_file:
        for file_path in file_paths:
            with open(file_path, 'r') as input_file:
                output_file.write(f':{file_path}\n')
                output_file.write(input_file.read())
                output_file.write('\n')


if __name__ == '__main__':
    source_files = get_source_files(ROOT_FOLDER)
    
    output_path = os.path.join(ROOT_FOLDER, 'merged.txt')
    merge_files(source_files, output_path)