from flask import Flask, render_template, jsonify, request, redirect, url_for
import speech_recognition as sr
from nlp import process_text

app = Flask(__name__)

# Map of words to sign images
SIGN_IMAGE_MAP = {
    "hello": "/static/sign_images/hello.png",
    "day": "/static/sign_images/day.png",
    "friend": "/static/sign_images/friend.png",
    "love": "/static/sign_images/love.png",
    "goodbye": "/static/sign_images/goodbye.png",
    "no": "/static/sign_images/no.png",
    "please": "/static/sign_images/please.png",
    "thank you": "/static/sign_images/thankyou.png",
    "yes": "/static/sign_images/yes.png",
    "yesterday": "/static/sign_images/yesterday.png",
    # Add more mappings as needed
}

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['GET'])
def record_audio():
    text = record_and_convert_audio()
    nlp_result = process_text(text)
    
    image_path = SIGN_IMAGE_MAP.get(text.lower(), None)  # Fetch the image path based on the text
    
    response = {
        "text": text,
        "image_path": image_path  # Include the image path in the response
    }
    
    return jsonify(response)

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Process the feedback (e.g., save to database, send email, etc.)
    print(f"Received feedback from {name} ({email}): {message}")
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return "Thank you for your feedback!"

if __name__ == "__main__":
    app.run(debug=True)
