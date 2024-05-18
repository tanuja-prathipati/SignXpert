from flask import Flask, render_template, jsonify, request
import speech_recognition as sr
from nlp import process_text

app = Flask(__name__)

# Function to record audio and convert it to text
def record_and_convert_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio_data = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle recording audio and returning text
@app.route('/record', methods=['GET'])
def record_audio():
    text = record_and_convert_audio()
    nlp_result = process_text(text)
    print("Processed Text:", nlp_result)  # Print processed text to the console
    return jsonify({"text": text})  # Return only the recorded speech to the frontend

if __name__ == "__main__":
    app.run(debug=True)
