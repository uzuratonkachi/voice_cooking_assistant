import speech_recognition as sr
import pyttsx3
import json
import requests
import string

recognizer = sr.Recognizer()
speaker = pyttsx3.init()






with open("recipes.json") as f:
	recipes = json.load(f)

current_recipe = None
current_step = 0

def generate_recipe(recipe_name):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={recipe_name}"
    response = requests.get(url)
    data = response.json()

    if data["meals"]:
        meal = data["meals"][0]
        instructions = meal["strInstructions"]
        # Split instructions into steps
        steps = instructions.split(". ")
        return steps
    else:
        return [f"Sorry, I couldn’t find a recipe for {recipe_name}."]


def listen():
	with sr.Microphone() as source:
		print("Listening...")
		audio = recognizer.listen(source)
	try:
		text = recognizer.recognize_google(audio)
		print(f"You said :{text}")
		return text
	except sr.UnknownValueError:
		print("Sorry, I could not understand.")
		return ""
	except sr.RequestError:
		print("Could not request results; check your internet connection")
		return ""

def handle_greetings(command):
	greetings = ["hello","hi","hey", "good morning", "good evening", "good night"]
	
	command_clean = command.lower().translate(str.maketrans('', '', string.punctuation))	
	for word in greetings:
		if word in command_clean:
			speak("Hello! I'm your cooking assistant. What would you like to cook today?")
			return True
	return False

def speak(text):
	speaker.say(text)
	speaker.runAndWait()

if __name__ == "__main__":
	speak("Hello! I am your cooking assistant. How can I help?")
	while True:
		command = listen()
		if handle_greetings(command):
			continue
		if "stop" in command or "exit" in command:
			speak("Goodbye!")
			break
		elif "make" in command:
			found = False
			for recipe_name in recipes.keys():
				if recipe_name in command: 
					current_recipe = recipe_name 
					current_stop = 0 
					speak(f"Let's start making {recipe_name}.") 
					speak(recipes[recipe_name][current_step])
					found = True
					break
			if not found :
				speak("Sorry, I don't know that recipe.")

		elif "next" in command and current_recipe:
			if current_step+1<len(recipes[current_recipe]):
				current_step +=1
				speak(recipes[current_recipe][current_step])
			else:
				speak("You have finished all the steps!")

		elif "repeat" in command and current_recipe:
			speak(recipes[current_recipe][current_step])

		else:
			speak(f"You said : {command}")
