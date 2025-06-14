import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "."
    abs_working_directory = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_directory):
        return f'Error: "{directory}" is not a directory'
    
    try:
        directory_contents = os.listdir(abs_directory)
        output_lines = []
        for item in directory_contents:
            item_path = os.path.join(abs_directory, item)
            file_size = os.path.getsize(item_path)
            file_type = "True" if os.path.isdir(item_path) else "False"
            output_lines.append(f"- {item}: file_size={file_size} bytes, is_dir={file_type}")
        return "\n".join(output_lines)
    except Exception as e:
        return f'Error: {str(e)}'