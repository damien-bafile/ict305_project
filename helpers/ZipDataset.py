import io
import os
import zipfile
from typing import List

def zip_dataset(folder_path: str, file_names: List[str]) -> io.BytesIO:
    """
    :param folder_path: The path of the folder where the files are located.
    :param file_names: A list of file names to include in the zip file.
    :return: A BytesIO object containing the zipped file data.
    """
    zip_buffer = io.BytesIO()

    # Create the zip file in the buffer
    with zipfile.ZipFile(
            zip_buffer, "w", zipfile.ZIP_DEFLATED, allowZip64=True
    ) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                # Check if the file name is in the specified list
                if file in file_names:
                    file_path = os.path.join(root, file)
                    # Add file to the zip with a relative path
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

    # Move the cursor to the start of the buffer
    zip_buffer.seek(0)
    return zip_buffer


