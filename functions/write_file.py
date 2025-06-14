import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_filepath = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_filepath.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure the directory exists
        if not os.path.exists(os.path.dirname(abs_filepath)):
            os.makedirs(os.path.dirname(abs_filepath))

        with open(abs_filepath, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'
