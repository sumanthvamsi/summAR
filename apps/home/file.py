import os
def combine(file_name, content,path):
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path, file_name)
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File '{file_path}' created successfully.")
    except Exception as e:
        print(f"Error creating file: {e}")