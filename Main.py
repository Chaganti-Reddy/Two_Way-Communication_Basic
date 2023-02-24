import speech_recognition as sr
import pyttsx3
import openai

# Load OpenAI API key from .env file
openai.api_key_path = ".env"

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Set the voice to a female voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Set default volume level
default_volume = engine.getProperty('volume')

# Set pause and resume thresholds for listening
pause_threshold = 1
resume_threshold = 0.5


def listen_and_respond():
    """Listens for speech input and responds based on the input"""
    with sr.Microphone() as source:
        # Prompt the user to speak
        print("Speak something:")
        audio = r.listen(source)

        # Try to recognize the speech input using Google Speech Recognition
        print("Recognizing...")
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)

        # If speech input cannot be recognized, handle the exception and notify the user
        except sr.UnknownValueError:
            print("Oops! Didn't catch that...")
            engine.say("Oops! Didn't catch that...")
            engine.runAndWait()
            return True

        # If there is an error with the Google Speech Recognition service, handle the exception and notify the user
        except sr.RequestError as e:
            print(
                "Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            engine.say(
                "Uh oh! Couldn't request results from Google Speech Recognition service.")
            engine.runAndWait()
            return True

        # If the user says to stop listening, exit the program
        if text.lower() in ["stop listening", "stop listening now", "quit", "exit"]:
            print("Exiting program...")
            engine.say("I am Exiting program...")
            engine.stop()
            return False

        # If the user says to pause listening, pause the listening and notify the user
        elif text.lower() == "pause listening":
            # global pause_threshold
            pause_threshold = 1000
            r.adjust_for_ambient_noise(source)
            print("Listening paused...")
            engine.say("Listening paused...")
            engine.runAndWait()
            return True

        # If the user says to resume listening, resume the listening and notify the user
        elif text.lower() == "resume listening":
            # global pause_threshold
            pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            print("Listening resumed...")
            engine.say("Listening resumed...")
            engine.runAndWait()
            return True

        # If the user says to set the volume to a specific level, set the volume and notify the user
        elif "set volume to" in text.lower():
            try:
                volume_level = int(text.split()[-2]) / 100
                engine.setProperty('volume', volume_level)
                print("Volume set to", volume_level)
                engine.say("Volume set to " + str(volume_level))
                engine.runAndWait()
            except:
                print("Invalid volume level")
                engine.say("Invalid volume level")
                engine.runAndWait()
            return True

        # If the user says to change the voice to a specific language and gender, change the voice and notify the user
        elif "change voice to" in text.lower():
            try:
                lang = text.split()[-2]
                gender = text.split()[-3]
                for voice in voices:
                    if lang in voice.languages and gender in voice.name:
                        engine. setProperty('voice', voice.id)
                        print("Voice changed to", voice.name)
                        engine.say("Voice changed to " + voice.name)
                        engine.runAndWait()
                        return True
                    else:
                        print("Invalid language or gender")
                        engine.say("Invalid language or gender")
                        engine.runAndWait()
                        return True
            except:
                print("Error changing voice")
                engine.say("Error changing voice")
                engine.runAndWait()
                return True
                # If the user does not provide any specific command, use OpenAI's GPT-3 to generate a response based on their input
        else:
            try:
                # Use OpenAI's GPT-3 to generate a response based on the input
                prompt = text.lower().strip()
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=250,
                    n=1,
                    stop=None,
                    temperature=0.7,
                    timeout=20,
                    best_of=1,
                )

                # Speak the response and print it to the console
                output_text = response.choices[0].text.strip()
                print("AI: " + output_text)
                engine.say(output_text)
                engine.runAndWait()

            # If there is an error with the OpenAI API, handle the exception and notify the user
            except Exception as e:
                print("Oops! An error occurred:", e)
                engine.say("Oops! An error occurred")
                engine.runAndWait()
                return True

    return True


while True:
    listening = listen_and_respond()

    if not listening:
        break
