import pyttsx3
from pathlib import Path
from docx import Document
import sys

def read_docx(file_path):
    """Read content from a .docx file"""
    doc = Document(file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

def generate_audio(text, output_file):
    """Generate audio file from text using pyttsx3"""
    try:
        engine = pyttsx3.init()
        # Adjust the speech rate (default is 200)
        engine.setProperty('rate', 150)
        # Set voice to be more natural
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.save_to_file(text, str(output_file))
        engine.runAndWait()
        print(f"Successfully generated: {output_file}")
    except Exception as e:
        print(f"Error generating audio for {output_file}: {str(e)}")
        raise

def main():
    # Setup directories
    BOOKS_FOLDER = Path('static/books')
    AUDIO_FOLDER = Path('static/audio')
    
    # Ensure audio directory exists
    AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)
    
    # Process each book
    for book_file in BOOKS_FOLDER.glob('*.docx'):
        print(f"\nProcessing {book_file.name}...")
        
        # Generate output filename
        audio_file = AUDIO_FOLDER / f"{book_file.stem}.mp3"
        
        # Skip if audio file already exists
        if audio_file.exists():
            print(f"Audio file already exists for {book_file.name}, skipping...")
            continue
        
        try:
            # Read the book content
            text = read_docx(book_file)
            
            # Generate the audio
            print(f"Generating audio for {book_file.name}...")
            generate_audio(text, audio_file)
            
        except Exception as e:
            print(f"Error processing {book_file.name}: {str(e)}")
            continue

if __name__ == "__main__":
    print("Starting audio generation for all books...")
    main()
    print("\nAudio generation complete!") 