import tkinter as tk
import json
from assistant import listen, speak, handle_greetings, generate_recipe

with open("recipes.json") as f:
	recipes = json.load(f)
current_recipe = None
current_step =0

class CookingAssistantApp(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Voice Cooking Assistant")
		self.geometry("400x300")

		self.recipe_label = tk.Label(self,text = "Recipe: None", font = ("Helvetica",14))
		self.recipe_label.pack(pady = 10)

		self.step_label = tk.Label(self,text = "Step:None", wraplength = 350, justify = "left")
		self.step_label.pack(pady = 10)

		start_button = tk.Button(self, text = "Start (Say Recipe)", command = self.start_recipe)
		start_button.pack(pady = 5)
		
		next_button =  tk.Button(self, text = "Next Step", command = self.next_step)
		next_button.pack(pady =5)
		
		repeat_button = tk.Button(self, text = "Repeat Step", command = self.repeat_step)
		repeat_button.pack(pady = 5)

		stop_button = tk.Button(self,text="Stop", command = self.quit)
		stop_button.pack(pady = 5)


	def start_recipe(self):
		global current_recipe, current_step
		command = listen().lower()
		print(f"Debug: Recognized command : {command}")

		
		if handle_greetings(command):
			return
		
		found = False
		if "make" in command:
			for recipe_name in recipes.keys():
				if recipe_name in command:
					current_recipe = recipe_name 
					current_step = 0 
					self.recipe_label.config(text = f"Recipe:{recipe_name}") 
					self.step_label.config(text = recipes[recipe_name][current_step])
					speak(f"Let's start making {recipe_name}.")
					speak(recipes[recipe_name][current_step])
					found = True
					break
			if not found:
				speak(f"I don't know how to make that. Let me find it for you.")
				steps = generate_recipe(command.replace("make", "").strip())
				if steps:
					new_recipe_name = command.replace("make", "").strip()
					recipes[new_recipe_name] = steps
				
					with open("recipes.json","w" ) as f:
						json.dump(recipes, f, indent = 4)
		
					current_recipe = new_recipe_name
					current_step = 0
					self.recipe_label.config(text=f"Recipe: {new_recipe_name}")
					self.step_label.config(text=steps[0])
					speak(steps[0])
			
		else:
			speak("Sorry, I didn't understand. Please say which recipe you want to make.")

	def next_step(self):
		global current_step
		if current_recipe:
			if current_step + 1< len(recipes[current_recipe]):
				current_step +=1
				self.step_label.config(text = recipes[current_recipe][current_step])
				speak(recipes[current_recipe][current_step])
			else:
				speak("You have finished all the steps!")
	
	def repeat_step(self):
		if current_recipe:
			speak(recipes[current_recipe][current_step])
	
if __name__ =="__main__":
	app = CookingAssistantApp()
	app.mainloop()
