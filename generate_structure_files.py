import os


class StructureFile:
    def __init__(self, file_path):
        # Check if the structure file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Read the content of the structure file
        with open(file_path, "r") as file:
            self._content = file.readlines()  # Use readlines to process line by line

    def generate(self):
        base_folder = self._get_current_folder()
        folder_stack = [base_folder]  # Stack to manage the current folder based on indentation level

        for line in self._content:
            line = line.rstrip()  # Remove trailing whitespace/newline characters

            if line.strip() == "":  # Skip empty lines
                continue

            # Handle indentation to manage nested folders
            indent_level = self._get_indent_level(line)
            clean_line = line.strip()

            # Adjust the folder stack based on the current indentation level
            folder_stack = folder_stack[:indent_level + 1]  # Keep folders up to current indent level

            if clean_line.endswith("/"):  # It's a folder
                # Create the folder and add it to the folder stack
                current_folder = os.path.join(folder_stack[-1], clean_line[:-1])  # Remove trailing '/'
                print(f"Creating folder: {current_folder}")
                if not os.path.exists(current_folder):
                    os.makedirs(current_folder)
                folder_stack.append(current_folder)
            else:  # It's a file
                file_path = os.path.join(folder_stack[-1], clean_line)
                print(f"Creating file: {file_path}")
                with open(file_path, "w") as f:  # Create an empty file
                    pass  # Empty file creation, add content here if needed

    def _get_current_folder(self) -> str:
        """Get the current folder where the script is located."""
        return os.path.dirname(os.path.abspath(__file__))

    def _get_indent_level(self, line: str) -> int:
        """Get the number of leading tabs to handle nested structures."""
        return len(line) - len(line.lstrip('\t'))  # Count the number of leading tabs

