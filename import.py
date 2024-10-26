import easyocr
import os
import glob
import hashlib
import shutil
from dataclasses import dataclass, asdict
import json

import re
import unicodedata

reader = easyocr.Reader(['en'], gpu=False)  # Disable GPU

def find_images():
    folder_path = "./images"
    image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, f"*{ext}")))

    return image_files


def file_content_hash(file_path, algorithm='md5', chunk_size=8192):
    """
    Calculate the hash of a file's contents using the specified algorithm.

    :param file_path: Path to the file
    :param algorithm: Hash algorithm to use ( 'md5', 'sha1', 'sha256')
    :param chunk_size: Size of chunks to read (default: 8192 bytes)
    :return: Hexadecimal digest of the file hash
    """
    hash_obj = hashlib.new(algorithm)

    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            hash_obj.update(chunk)

    return hash_obj.hexdigest()


def get_file_name_and_extension(file_path):
    # Get the file name with extension
    file_name = os.path.basename(file_path)
    # Split the file name and extension
    name, extension = os.path.splitext(file_name)
    extension = extension.lower()
    return name, extension


def slugify(text):
    # Convert to lowercase and remove leading/trailing whitespace
    text = text.lower().strip()

    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)

    # Remove non-word characters (everything except letters, numbers and underscores)
    text = re.sub(r'[^\w\s-]', '', text)

    # Replace all runs of whitespace with a single dash
    text = re.sub(r'[-\s]+', '-', text)

    return text

def get_image_content_ocr(image_file):
    result = reader.readtext(image_file)
    # Extract only the text from the results
    text_list = [detection[1] for detection in result]

    # Join all text into a single string
    all_text = ' '.join(text_list)
    print(f"OCR for {image_file}: {all_text}")
    return all_text

def get_image_metadata(image_file, ignore_cache = True):
    cache_file = f'{get_file_name_and_extension(image_file)[0]}.json'
    if ignore_cache == False and os.path.exists(cache_file):
        with open( os.path.join("images", cache_file), 'r') as file:
            # Load the JSON content and convert it to a Python dictionary
            data = json.load(file)
            print(f"Read metadata from cache for file {image_file}")
            return data
    content_raw = get_image_content_ocr(image_file)
    content = content_raw
    title = " ".join(content.split(" ")[0:6])  # Take 6 words
    hash = file_content_hash(image_file)[:12]
    slug = f"{slugify(title).lower()}-{hash}"
    originalImagePath = image_file
    ext = get_file_name_and_extension(image_file)[1]
    imagePath = f"{hash}{ext}"

    metadata = {
        'hash': hash,
        'contentRaw': content_raw,
        'content': content,
        'title': title,
        'slug': slug,
        'originalImagePath': originalImagePath,
        'imagePath': imagePath
    }
    write_json(metadata, os.path.join("images", cache_file))
    return metadata



def copy_file_with_new_name(source_path, destination_folder, new_name):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Construct the full destination path with the new name
    destination_path = os.path.join(destination_folder, new_name)

    # Copy the file
    shutil.copy2(source_path, destination_path)

    print(f"File copied to: {destination_path}")

def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    images = find_images()
    for image in images:
        metadata = get_image_metadata(image)
        year = 2024
        source = metadata['originalImagePath']
        destination_folder= "./src/pages/posts/2024"
        copy_file_with_new_name(metadata['originalImagePath'], destination_folder, metadata['imagePath'])
        write_json(metadata, os.path.join(destination_folder, f"{metadata['hash']}.json"))