import json
import os
import requests
from io import BytesIO

def download_image(url, save_path):
    """
    Download an image from a URL and save it to a file.
    
    Parameters:
    - url: URL of the image.
    - save_path: Path to save the downloaded image.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        image_data = BytesIO(response.content)
        
        # Determine the file extension from the content type
        content_type = response.headers['Content-Type']
        if 'jpeg' in content_type:
            file_extension = 'jpg'
        elif 'png' in content_type:
            file_extension = 'png'
        else:
            raise ValueError("Unsupported image format")

        file_path = f"{save_path}.{file_extension}"
        
        # Save image to file
        with open(file_path, 'wb') as file:
            file.write(image_data.read())
        
        print(f"Image saved to {file_path}")
        
    except requests.RequestException as e:
        print(f"Error downloading image from URL {url}: {e}")

def parse_ndjson_file(ndjson_file_path, save_folder):
    """
    Parse NDJSON file and download images to a specified folder.
    
    Parameters:
    - ndjson_file_path: Path to the NDJSON file.
    - save_folder: Folder to save the downloaded images.
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    with open(ndjson_file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                data_row = data.get('data_row', {})
                image_url = data_row.get('row_data')
                
                if image_url:
                    # Generate a unique filename based on the URL
                    image_name = image_url.split('/')[-1].split('?')[0]
                    save_path = os.path.join(save_folder, image_name)
                    download_image(image_url, save_path)
                else:
                    print(f"No image URL found in line: {line}")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
            except Exception as e:
                print(f"Error processing line: {line}, {e}")

# Example usage
ndjson_file_path = 'C:/kkt/2024_07_ColonyCounter/JSON_File/Colony_Counterbox.ndjson'
save_folder = 'C:/kkt/2024_07_ColonyCounter/Images'
parse_ndjson_file(ndjson_file_path, save_folder)
