from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo

import speech_recognition as sr
from nlp import process_text

app = Flask(__name__)

# Configure MongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/feedbackdb'  # Replace with your MongoDB URI
mongo = PyMongo(app)

# Map of words to sign images
SIGN_IMAGE_MAP = {
    "hello": "/static/sign_images/hello.png",
    "friend": "/static/sign_images/friend.png",
    "goodbye": "/static/sign_images/goodbye.png",
    "thank you": "/static/sign_images/thankyou.png",
    "yesterday": "/static/sign_images/yesterday.png",
    "tomorrow": "/static/sign_images/tomorrow.png",
    "confession": "/static/sign_images/confession.png",
    "afternoon": "/static/sign_images/afternoon.png",
    "doctor": "/static/sign_images/doctor.png",
    "interpreter": "/static/sign_images/interpreter.png",
    "manager": "/static/sign_images/manager.png",
    # Add more mappings as needed
}

# Function to record audio and convert to text
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

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle recording audio
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

# Route for the feedback form
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Route to handle submitting feedback
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        # Process the feedback form data
        name = request.form.get('name')
        email = request.form.get('email')
        feedback = request.form.get('feedback')

        # Store the feedback in MongoDB
        feedback_collection = mongo.db.feedback
        feedback_collection.insert_one({
            'name': name,
            'email': email,
            'feedback': feedback
        })

        # Return a JSON response indicating success
        return jsonify({"message": "Feedback submitted successfully!"}), 200
    except Exception as e:
        # Return a JSON response indicating failure
        return jsonify({"message": f"Error submitting feedback: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
