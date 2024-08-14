# Book downloader

This script provides functionality to convert PDFs to MP3 audio files, download images from a URL to create PDFs, and convert those images into a single PDF document. Below are detailed instructions on how to use each feature of the script.
## Installation📦
    git clone https://github.com/Borooooo/booksdownloader.git


## Recommended Python Version🐍
- The recommended version for Python 3 is 3.4.x

## Dependencies🔧
- Pillow
- PyPDF2
- gTTS
- requests
- tqdm

  ```pip install -r requirements.txt```
## Usage💡

     python bookdownloader.py
``` 
  - Select option 1 to download images.

 Enter the base URL where images are hosted (e.g., http://example.com/image-).

 Enter the name of the folder where images will be saved.

  - Select option 2 to convert images to PDF.

 Enter the name of the folder containing the images.

 The script will compile all .jpg images in the folder into a PDF named after the folder.
 Create an Audiobook from PDF

  - Select option 3 to create an audiobook from PDF.

 Ensure that the pdf folder contains PDF files to be converted.

 The script will list available PDF files. Enter the number corresponding to the file you want to convert.

 The script will convert the selected PDF file to an MP3 file, saved in the mp3 folder.

```

##  Additional Information✨
 For the script to work correctly, it is necessary that PDF files be recognized or that it is possible to highlight the characters contained in them, since this is necessary for the script to read text from files and the links needs to be base links