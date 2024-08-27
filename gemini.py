import speech_recognition as sr
import google.generativeai as genai

genai.configure(api_key='apikey')
# Select the specific AI model to use.
model = genai.GenerativeModel('gemini-pro')

def capture_speech():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
            print("Please say something:")
            # Adjust the recognizer sensitivity to ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            # Capture audio from the microphone
            audio_data = recognizer.listen(source)
            print("Recognizing...")
        # Recognize speech using Google Web Speech API
    try:
        text = recognizer.recognize_google(audio_data)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        
            
def send_to_gemini(request_prompt):
    # Send a prompt to Gemini using model.generate_content method
    if request_prompt != None :
        response = model.generate_content("Respond using one of these options ( curls, squats, reset, quit, null) to the message provided. make your decision based on context to the verb. if the message is about doing curls, or working out arms then return 'curls'. For example: 'i want to do some curls' or 'lets work out arms'. if its about doing squats or working out legs then return 'squat'. For example 'i want to do some squat' or 'lets work on legs now'. if its about resetting a counter then return 'reset'. For example 'reset counter' or ' lets start over this exercise' or let's go again'. if its about exiting the program then return 'quit'. For example 'shutdown' or 'i am finished for now'. if it is not related to any of the other options or the message is incomplete/unclair return null. Here is the message: "+ request_prompt)
        print(response.text)
        return response.text
    else:
        print('nontype')

    