import os
import glob
import requests
from PIL import Image
from PyPDF2 import PdfReader
from gtts import gTTS
from tqdm import tqdm

def banner():
    text = r'''
   ___            __             __                __             __       
  / _ )___  ___  / /__ ___   ___/ /__ _    _____  / /__  ___ ____/ /__ ____
 / _  / _ \/ _ \/  '_/(_-<  / _  / _ \ |/|/ / _ \/ / _ \/ _ `/ _  / -_) __/
/____/\___/\___/_/\_\/___/  \_,_/\___/__,__/_//_/_/\___/\_,_/\_,_/\__/_/
#coded by Boro @Borooooo
'''
    print(text)

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_images(base_url, folder_name):
    create_folder(folder_name)
    page_number = 1

    while True:
        image_url = f"{base_url}{page_number}.jpg"
        print(f"Attempting to download image: {image_url}")

        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_path = os.path.join(folder_name, f"{page_number}.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded image: {page_number}.jpg")
                page_number += 1
            else:
                print(f"Page {page_number} does not exist or couldn't be downloaded. Status code: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Failed to download image {page_number}.jpg due to an error: {e}")
            break

    print("Finished downloading")

def convert_images_to_pdf(folder_name):
    output_pdf = f"{folder_name}.pdf"
    image_files = sorted([f for f in os.listdir(folder_name) if f.endswith('.jpg')])

    if not image_files:
        print("No images found in the folder")
        return

    image_list = []
    for image_file in image_files:
        image_path = os.path.join(folder_name, image_file)
        try:
            image = Image.open(image_path).convert('RGB')
            image_list.append(image)
        except Exception as e:
            print(f"Error opening image file: {image_file}")
            print(e)

    try:
        image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])
        print(f"Saved as {output_pdf}")
    except Exception as e:
        print(f"Error saving PDF file: {output_pdf}")
        print(e)

def create_audiobook_from_pdf():
    create_folder('mp3')
    create_folder('pdf')

    pdf_files = glob.glob('pdf/*.pdf')
    if not pdf_files:
        print('No PDF files found in the "pdf" folder.')
        return

    print('List of PDF files:')
    for i, file_path in enumerate(pdf_files):
        file_name = os.path.basename(file_path)
        print(f'{i+1}. {file_name}')

    while True:
        file_number = input('Enter PDF file number to convert to MP3 or enter "0" to exit: ')
        try:
            file_number = int(file_number)
            if file_number == 0:
                return
            if file_number < 1 or file_number > len(pdf_files):
                print(f'The number must be from 1 to {len(pdf_files)}.')
            else:
                pdf_file_to_convert = pdf_files[file_number-1]
                break
        except ValueError:
            print('Enter an integer.')

    try:
        pdf_reader = PdfReader(pdf_file_to_convert)
    except Exception as e:
        print(f"Error reading PDF file: {pdf_file_to_convert}")
        print(e)
        return

    text = ''
    total_pages = len(pdf_reader.pages)
    with tqdm(total=total_pages, desc='Converting', unit='page') as pbar:
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            if page.extract_text():
                text += page.extract_text().strip().replace("\n", " ").replace(" ' ", "'")
            pbar.update(1)

    print("The file is being written. Waiting...")
    with tqdm(total=1, desc='Writing', unit='file') as pbar:
        tts = gTTS(text=text, slow=False)
        mp3_file_name = os.path.splitext(os.path.basename(pdf_file_to_convert))[0] + '.mp3'
        mp3_file_path = os.path.join('mp3', mp3_file_name)

        try:
            tts.save(mp3_file_path)
            pbar.update(1)
            print(f'{mp3_file_name} file successfully created in mp3 folder.\n')
        except Exception as e:
            print(f"Error saving MP3 file: {mp3_file_path}")
            print(e)

def main():
    banner()
    def option1():
        base_url = input("Enter the base URL of the images: ")
        folder_name = input("Enter the name of the folder to save the images in: ")
        print("Downloading images...")
        download_images(base_url, folder_name)

    def option2():
        folder_name = input("Enter the directory of the folder containing the images: ")
        print("Converting images to PDF...")
        convert_images_to_pdf(folder_name)

    def option3():
        print("Creating audiobook from PDF...")
        create_audiobook_from_pdf()

    menu_opcje = {
      "1": option1,
      "2": option2,
      "3": option3
    }

    print("Menu Options:")
    print("1. Download images")
    print("2. Convert images to PDF")
    print("3. Create audiobook from PDF")

    choice = input("Enter your choice (1/2/3): ")
    menu_opcje.get(choice, lambda: print("Invalid choice"))()

if __name__ == "__main__":
    main()
