# eBook and AudioBook Web Application

## Author
Allen Rehkemper
MS587 - Module 2.1
Professor Hinton

## Description
This web application serves as both an eBook and audiobook platform. Users can:
- Browse a collection of stories
- Read stories online
- Download stories as text files
- Listen to audio previews
- Download complete audiobook versions

## Features
- Flask web framework for robust web application development
- Text-to-speech conversion using pyttsx3
- Responsive web design
- On-demand audio generation
- Cross-platform compatibility

## Technical Requirements
- Python 3.x
- Flask
- pyttsx3
- Additional requirements listed in requirements.txt

## Installation
1. Clone the repository:
```bash
git clone [your-repository-url]
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the application at: http://localhost:5000

## Project Structure
```
ebook_audiobook_app/
├── static/
│   ├── audio/      # Generated audiobook files
│   ├── books/      # Text versions of stories
│   └── images/     # Cover images
├── templates/      # HTML templates
├── app.py         # Main application file
└── requirements.txt
```

## Usage
- Visit the home page to see all available books
- Click on a book to read its content
- Use the audio player to preview the story
- Download options available for both text and audio versions

## License
This project is created for educational purposes as part of MS587 coursework. 