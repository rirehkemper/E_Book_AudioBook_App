#Allen Rehkemper
#2025-06-02
#Module 2.1 MS587
#Professor Hinton
#This application is a simple web application that allows users to read and listen to books.
# Flask: Web framework for routing and template rendering
# os: Operating system interface for file operations
# pyttsx3: Text-to-speech conversion library Though it is not my favorite, it is a good library for this project.
# Path: Object-oriented filesystem paths
from flask import Flask, render_template, send_file, jsonify
import os
import pyttsx3
from pathlib import Path

# Initialize Flask application instance
# This creates the WSGI application object that handles all requests
app = Flask(__name__)

# Configure static asset directories using Path for cross-platform compatibility
# Path objects provide an object-oriented interface to filesystem paths
# This approach is more robust than string concatenation for path handling
BOOKS_FOLDER = Path('static/books')
AUDIO_FOLDER = Path('static/audio')
IMAGES_FOLDER = Path('static/images')

# Ensure required directories exist before application starts
# mkdir with parents=True creates intermediate directories as needed
# exist_ok=True prevents errors if directories already exist
BOOKS_FOLDER.mkdir(parents=True, exist_ok=True)
AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)
IMAGES_FOLDER.mkdir(parents=True, exist_ok=True)

# Define the book collection as a list of dictionaries
# This data structure allows for easy iteration and access to book properties
# Each book has a unique ID, title, description, and associated media files
books = [
    {
        'id': 1,
        'title': 'Waffles the Rabbit Finds a Hat',
        'description': 'A delightful tale about a rabbit\'s adventure with a mysterious hat.',
        'cover_image': 'Waffles_the_Rabbit_Finds_a_Hat.jpg',
        'audio_file': 'Waffles_the_Rabbit_Finds_a_Hat.mp3',
        'text_file': 'Waffles_the_Rabbit_Finds_a_Hat.txt'
    },
    {
        'id': 2,
        'title': 'The Last Cup of Tea',
        'description': 'A heartwarming story about finding comfort in life\'s simple pleasures.',
        'cover_image': 'The_Last_Cup_of_Tea.jpg',
        'audio_file': 'The_Last_Cup_of_Tea.mp3',
        'text_file': 'The_Last_Cup_of_Tea.txt'
    },
    {
        'id': 3,
        'title': 'The Great Jellybean Sky Race',
        'description': 'An exciting adventure in a world where jellybeans can fly.',
        'cover_image': 'The_Great_Jellybean_SkyRace.jpg',
        'audio_file': 'The_Great_Jellybean_Sky_Race.mp3',
        'text_file': 'The_Great_Jellybean_Sky_Race.txt'
    },
    {
        'id': 4,
        'title': 'The Last Breath',
        'description': 'A mysterious tale of suspense and discovery.',
        'cover_image': 'The_Last_Breath.jpg',
        'audio_file': 'The_Last_Breath.mp3',
        'text_file': 'The_Last_Breath.txt'
    },
    {
        'id': 5,
        'title': 'The Realm of Echoes',
        'description': 'A magical journey through a world where sounds come alive.',
        'cover_image': 'The_Realm_of_Echoes.jpg',
        'audio_file': 'The_Realm_of_Echoes.mp3',
        'text_file': 'The_Realm_of_Echoes.txt'
    }
]

# Route decorator for the home page
# Maps the root URL ('/') to this function
@app.route('/')
def index():
    """
    Render the home page with all books
    Returns: Rendered HTML template with the books list
    """
    return render_template('index.html', books=books)

# Route decorator for individual book pages
# Dynamic routing with book_id parameter
# The <int:book_id> syntax ensures the parameter is converted to an integer
@app.route('/book/<int:book_id>')
def book_detail(book_id):
    """
    Show detailed view of a specific book
    Args:
        book_id (int): The unique identifier for the book
    Returns:
        Rendered template or error message with appropriate HTTP status code
    """
    # Use next() with a generator expression for efficient book lookup
    # Returns None if no book matches the ID
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        try:
            # Construct the full path to the book file using Path for safety
            book_path = BOOKS_FOLDER / book['text_file']
            # Open file with explicit UTF-8 encoding to handle special characters
            with open(book_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return render_template('book_detail.html', book=book, content=content)
        except Exception as e:
            # Return error message with 500 status code for server errors
            return f'Error reading book: {str(e)}', 500
    # Return 404 status code if book not found
    return 'Book not found', 404

# Route for audio file downloads
# Handles dynamic generation and serving of audio files
@app.route('/download/audio/<int:book_id>')
def download_audio(book_id):
    """
    Download or generate audio version of the book
    Args:
        book_id (int): The unique identifier for the book
    Returns:
        Audio file download response or error message
    """
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        audio_path = AUDIO_FOLDER / book['audio_file']
        if not audio_path.exists():
            # Generate audio on-demand if it doesn't exist
            book_path = BOOKS_FOLDER / book['text_file']
            try:
                with open(book_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                generate_audio(text, book['audio_file'])
            except Exception as e:
                return f'Error generating audio: {str(e)}', 500
        
        if audio_path.exists():
            # Use send_file for secure file serving
            # as_attachment=True prompts download instead of playing in browser
            return send_file(
                audio_path,
                as_attachment=True,
                download_name=f"{book['title']}.mp3"
            )
    return 'Audio file not found', 404

# Route for eBook downloads
# Serves the original text files for download
@app.route('/download/ebook/<int:book_id>')
def download_ebook(book_id):
    """
    Download text version of the book
    Args:
        book_id (int): The unique identifier for the book
    Returns:
        Text file download response or error message
    """
    book = next((book for book in books if book['id'] == book_id), None)
    if book and os.path.exists(BOOKS_FOLDER / book['text_file']):
        return send_file(
            BOOKS_FOLDER / book['text_file'],
            as_attachment=True,
            download_name=book['text_file']
        )
    return 'eBook file not found', 404

# Helper function for text-to-speech conversion
def generate_audio(text, output_file):
    """
    Generate audio file from text using pyttsx3
    Args:
        text (str): The text to convert to speech
        output_file (str): The filename for the generated audio
    Raises:
        Exception: If audio generation fails
    """
    try:
        # Initialize text-to-speech engine
        engine = pyttsx3.init()
        
        # Configure voice properties for optimal quality
        # Reduce rate for better clarity (default is 200)
        engine.setProperty('rate', 145)
        
        # Select and configure the voice
        voices = engine.getProperty('voices')
        if voices:
            # Use Zira voice (index 1) for more natural narration
            engine.setProperty('voice', voices[1].id)
        
        # Set volume to 90% for optimal audio levels
        engine.setProperty('volume', 0.9)
        
        # Generate and save the audio file
        engine.save_to_file(text, str(AUDIO_FOLDER / output_file))
        engine.runAndWait()
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        raise

# Application entry point
# The debug=True flag enables development features
if __name__ == '__main__':
    app.run(debug=True) 