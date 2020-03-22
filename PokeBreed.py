import time
import os
import os.path
import sys
import random
import platform
from datetime import datetime
from collections import OrderedDict
from copy import deepcopy as deepcopy

#--------------- SETUP ------------------

if platform.system() == 'Linux': #These 3 statements check the OS, so the getch-function is inputted in accordance with OS syntax
	import getch as msvcrt
elif platform.system() == 'Windows':
	import msvcrt
else:
	print("ERROR: Unknown OS.")
	time.sleep(1)
	sys.exit()

def platformcheck(): #Checks the platform in order to correctly define the clearscreen function in accordance with the OS
	if platform.system() == 'Linux':
		def clearscreen(): return os.system('clear')
	elif platform.system() == 'Windows':
		def clearscreen(): return os.system('cls')
	else:
		def clearscreen(): return ('clear')
	return clearscreen
clearscreen = platformcheck()

def prRed(prt): print("\033[91m {}\033[00m" .format(prt)) #These are functions that enable colored output to the user
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
def prBlue(prt): print("\033[94m {}\033[00m" .format(prt))
def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))

#-------------------------------------------

#-------------- GLOBAL VARIABLES ---------------------

natures = ["lonely", "brave", "adamant", "naughty", "bold", "relaxed", "impish", "lax", "timid", "hasty", "jolly", "naive", "modest", "mild", "quiet", "rash", "calm", "gentle", "sassy", "careful", "hardy", "docile", "serious", "bashful", "quirky", "none"]
stat_abr = ["atk","def","hp","sat","sde","spe"]
everstone_cost = 7000
braces_cost = 10000
gender_cost_average = 5000

#-----------------------------------------------------

def menues(optionlist, menuheader, option=0): #This function is called inside the main code every time a menu is required. It's what enables menu navigation in the code. List of options and menu header are brought upon being invoked.
	optioninput = 'w'
	optionlw=0
	optioninputlw = 'w'

	while optioninput != '\r': #Loop continues as long as the option isn't "\r", i.e. "enter"
		clearscreen()
		print(menuheader) #The menuheader is a static menu that is printed out at the start of each loop.
		if optioninput == 'w' and option==0: #The following conditions cover all of the possible menu situations, from start to end (example: first iteration at first option, etc.)
			prGreen(optionlist[option]) #Options are tracked and iterated for when the user hits "w" or "s". The respective element from the option list is printed with a highlight (this is defined before the function is called).
			optioninputlw = 'w'
			optionlw = 0
		elif optioninput == 'w' and option>0:			
			option-=1
			optionlw = option
			optioninputlw = 'w'
			prGreen(optionlist[option])
		elif optioninput == 's' and option<len(optionlist)-1: #This covers all the "down" iterations from the user, but stops from exceeding the total length of the menu.
			option+=1
			optionlw = option
			optioninputlw = 's'
			prGreen(optionlist[option])
		elif option == len(optionlist)-1:
			try:
				if not 1 <= int(optioninput) <= len(optionlist): #The user can also select an option via the number keys. This checks if the input coincides with a number on the menu.
					prGreen(optionlist[option])
				else:
					option = int(optioninput)-1
					optioninput = '\r' #If the number exists, optioninput is set to "\r" to convince the function that the user has hit "enter".
					continue
			except ValueError:
				prGreen(optionlist[option])
		elif optioninput == '\r':
			return option
		else:
			try:
				if 1 <= int(optioninput) <= len(optionlist): #A partial repeat of the above code, in order to ensure the user's number input is understood by the function.
					option = int(optioninput)-1
					optioninput = '\r'
					continue
				else:
					optioninput = optioninputlw
					option = optionlw
					prGreen(optionlist[option])
			except ValueError:
				optioninput = optioninputlw
				option = optionlw
				prGreen(optionlist[option])
		optioninput = msvcrt.getch()
		try:
			optioninput = bytes.decode(optioninput)
		except UnicodeDecodeError:
			continue
	clearscreen()
	return option #Returns the option number so that the correct action is taken in the next part of the program, wherever menues() is invoked.


def main():
	clearscreen()
	print("\n-------------------------- P o k é B r e e d e r --------------------------\n")
	print("Welcome to PokéBreeder, the breeding tool designed for use in PokeMMO!\nIts function is simple: to simplify the complex breeding process and reduce risk!")
	print("How it works: the user designs a Pokemon, and the tool builds a plan!\nIt's really that easy, and it's trivial to learn - I promise!")
	print("\nThis tool was designed by u/destructiveinfluence in March 2020. Happy breeding!")
	input("\nPress Enter to continue...")

	mainloop = 1

	while mainloop>0:

		optionlist = ["\n  \033[0;32;47m(1) Deploy Pokémon\033[0m\n  \033[92m(2) Create New Pokémon\033[00m\n  \033[92m(3) Help\033[00m\n  \033[92m(4) Exit\033[00m", \
		"\n  \033[92m(1) Deploy Pokémon\033[00m\n  \033[0;32;47m(2) Create New Pokémon\033[0m\n  \033[92m(3) Help\033[00m\n  \033[92m(4) Exit\033[00m", \
		"\n  \033[92m(1) Deploy Pokémon\033[00m\n  \033[92m(2) Create New Pokémon\033[00m\n  \033[0;32;47m(3) Help\033[0m\n  \033[92m(4) Exit\033[00m", \
		"\n  \033[92m(1) Deploy Pokémon\033[00m\n  \033[92m(2) Create New Pokémon\033[00m\n  \033[92m(3) Help\033[0m\n  \033[0;32;47m(4) Exit\033[0m"]
		menuheader = ("\n \033[95m\n \033[92m-- MAIN SELECTION --\033[00m")
		returned = menues(optionlist, menuheader)
		try:
			if returned == 0:
				clearscreen()
				pokedeploy()
			elif returned == 1:
				clearscreen()
				pokecreate()
			elif returned == 2:
				clearscreen()
				prGreen("\n--------------------- HELP ---------------------")
				prGreen("\nBasic navigation in POKEBREEDER is done with the 'w' and 's'-buttons, or by hitting the associated numbers.\nThis is only possible for menu options listed 1-9.\n"\
					"It's HIGHLY recommended to put POKEBREEDER in its own dedicated directory.\nIf you don't, be prepared for cluttering in your current directory.\n\n\n"\
					"POKEBREEDER has two modes: Pokémon deployment (1), and Pokémon creation (2).\n\n\nIn Pokémon creation, you add or remove traits to and from a Pokémon until it suits your needs.\n"\
					"This is done by typing a stat and number (e.g. atk 31),\nor adding a nature by typing 'nature' followed by a valid nature.\nAs you build your Pokémon, you'll see a report in real-time at the top of the screen.\n"\
					"The report shows your Pokémon stats, but also an estimated value, braces, and more.\nOnce finished, you can type 'save' and save the Pokémon, thus readying it for deployment.\n"
					"Once you're ready to deploy and breed for your Pokémon,\nuse the Deploy Pokémon option in the main menu.\n"\
					"This will bring up a selection of Pokémon you have created.\nThese Pokémon are stored in files created by POKEBREEDER.\n"\
					"Select your desired Pokémon and proceed (including the extension is not required).\n\n\n"\
					"In the Deployment section, you're presented with a 'blank slate'.\nHere, you manually create your first generation using the 'add' and 'rem' commands.\n"\
					"Example on how to add a first gen breeding Pokémon: 'add 1 atk f'.\nThis command means \"add a female Pokémon to row 1 with attack dominant stat\".\n\n"\
					"Once you're ready to breed your first gen Pokémon, type 'breed'.\nPOKEBREEDER will then do quality assurance and ensure that the correct traits are passed on.\n"\
					"If your first gen passes the test, keep typing 'breed' to proceed to next generations.\nOnce you reach the goal, you can proceed to the next stage by typing 'stage'.\n"\
					"This assumes that you have another stage to proceed to (i.e. a natured Pokémon).\nIf you don't, POKEBREEDER will take you to the report screen and your work will be done.\n"
					"There are more commands at your disposal in both the creation and deployment sections.\nTo learn more about these, simply type 'help' while in those respective sections.\n"
					"At any time, you can save your current progress and leave.\nYour progress will be stored, and you can continue from where you left off by loading te respective file!\n\n\n"\
					"A special thanks to u/XIPD for inspiring me to upload this to Reddit!\n\nHappy breeding!\n~u/destructiveinfluence")
				input("\033[94m\nPress Enter to return... \033[00m")

			elif returned == 3:
				clearscreen()
				prPurple("\n\n\n\n\n\n-------------------------------------")
				prRed("\n-------------------------------------")
				prBlue("\n-------------------------------------")
				prYellow("\n-------------------------------------")
				prGreen("\n|~ THANK YOU FOR USING POKEBREEDER ~|")
				prYellow("\n-------------------------------------")
				prBlue("\n-------------------------------------")
				prRed("\n-------------------------------------")
				prPurple("\n-------------------------------------\n")
				time.sleep(1.2)
				clearscreen()
				mainloop = 0
			else:
				clearscreen()
				prYellow("\nERROR! Incorrect input...")
				input("\033[94m\nPress Enter to return... \033[00m")
		except Exception as e:
			prRed("Uh oh! Something went wrong...")
			print("ERROR: "+str(e))
			input("\033[94m\nPress Enter to return... \033[00m")


def pokedeploy():
	deployloop = 1
	loadloop = 1

	while deployloop>0:
		while loadloop>0:
			directoryl = os.listdir() #This lists all the directories in user's working directory.
			clearscreen()
			prGreen("\nHere's a list of suggested files in your directory: \n")
			filesexist = 0
			for line in directoryl:
				extensioncheck = line[-6:]
				if ('.breed' in extensioncheck):
					filesexist = 1
					prPurple(line)
				else:
					continue
			if filesexist == 0:
				clearscreen()
				prYellow("\nThere are no breed-files in your current directory!\nYou will have to create a Pokémon first...")
				loadloop = 0
				deployloop = 0
				editloop = 0
				input("\033[94m\nPress Enter to return...\033[00m ")
				break
				
			else:
				pass
			filetemp = input("\n\033[92mWhat file would you like to target (or type 'exit' to go back)?\nName: \033[00m") #Asks user for file name
			if filetemp.endswith(".breed"):
				pass
			else:
				if filetemp.lower() == "exit":
					pass
				else:
					filetemp = filetemp + ".breed"

			if not (os.path.isfile(filetemp) and os.access(filetemp, os.R_OK)): #Checks if requested file exists in current directory, and is accessable. Returns to main menu for boolean FALSE
				if filetemp == 'exit':
					clearscreen()
					deployloop = 0
					loadloop = 0
					editloop = 0
				else:
					clearscreen()
					prYellow("\nERROR: Specified file is either unreadable or does not exist in current directory!")
					input("\033[94m\nPress Enter to return...\033[00m ")
					continue
			else:
				try:
					with open(filetemp, 'r') as f:
						raw_text = f.read()

						raw_cat = raw_text.split("***")
						profile = raw_cat[0].split("\n")
						phases = raw_cat[1].split("\n")
						generations = raw_cat[2].split("\n")

						for ind,each in enumerate(profile):
							if each == "":
								del profile[ind]

						for ind,each in enumerate(phases):
							if each == "":
								del phases[ind]

						for ind,each in enumerate(generations):
							if each == "":
								del generations[ind]

						name = profile[0].split("::")[1]
						stats_numb = profile[1].split("::")[1].split("/")
						stats_names = profile[1].split("::")[0].split("/")

						stats_dict = {}

						for ind,each in enumerate(stats_numb):
							stats_numb[ind] = int(stats_numb[ind])
							stats_dict[stats_names[ind]] = stats_numb[ind]

						hp = stats_numb[0]
						atk = stats_numb[1]
						dfs = stats_numb[2]
						sat = stats_numb[3]
						sde = stats_numb[4]
						spe = stats_numb[5]
						nature_literal = profile[2].split("::")[1]
						breeders = int(profile[3].split("::")[1])
						braces = int(profile[4].split("::")[1])
						braces_nat = int(profile[5].split("::")[1])
						everstone = int(profile[6].split("::")[1])
						gender = int(profile[7].split("::")[1])
						cost = int(profile[7].split("::")[1])

						stage = phases[0].split("::")[1]
						if stage == " ":
							stage = "iv"
						else:
							pass

						gen_counter = phases[1].split("::")[1]
						if gen_counter == " ":
							gen_counter = 1
						else:
							gen_counter = int(gen_counter)

						nature_breeder = []
						if stage.lower() == "iv":
							gen1 = generations[0].split("::")[1].split("|")
						else:
							gen1 = generations[1].split("::")[1].split("|")
							gen1_unique = set(gen1)
							for each in gen1_unique:
								nature_breeder.append(str(each[0:3]))

						clearscreen()
						prGreen("\nSuccessfully loaded "+str(filetemp)+"!")
						input("\033[94m\nPress Enter to continue... \033[00m")
						loadloop = 0
						editloop = 1
					f.close()

					for each in gen1:
						if len(each)<3:
							gen1.remove(each)
						else:
							pass

					length_gen1 = len(gen1)
					for i in range(0,breeders):
						if i<(length_gen1):
							pass
						else:
							if len(str(i+1)) == 1:
								gen1.append("0"+str(i+1)+": STDBY")
							else:
								gen1.append(str(i+1)+": STDBY")

					breedstats = []

					for names in stats_dict:
						if stats_dict[names] > 0:
							breedstats.append(names)

					iv_amount = len(breedstats)
					breedstring = ", ".join(breedstats)
					breedstats_abr = []

					for each in breedstats:
						if str(each).lower() == "hp":
							breedstats_abr.append("hpt")
						elif str(each).lower() == "attack":
							breedstats_abr.append("atk")
						elif str(each).lower() == "defense":
							breedstats_abr.append("def")
						elif str(each).lower() == "sp.atk":
							breedstats_abr.append("sat")
						elif str(each).lower() == "sp.def":
							breedstats_abr.append("sde")
						elif str(each).lower() == "speed":
							breedstats_abr.append("spe")

					if gen_counter == 1:
						gen2 = ""
						gen3 = ""
						gen4 = ""
						gen5 = ""
						gen6 = ""
					elif gen_counter == 2:
						gen2 = []
						gen3 = ""
						gen4 = ""
						gen5 = ""
						gen6 = ""

						for index in range(0,len(gen1)):
							if index%2 == 0:
								gen2.append(str(gen1[index][0:3])+ "|" + str(gen1[index+1][0:3]))
							else:
								continue
					elif gen_counter == 3:
						gen2 = []
						gen3 = []
						gen4 = ""
						gen5 = ""
						gen6 = ""

						for index in range(0,len(gen1)):
							if index%2 == 0:
								gen2.append(str(gen1[index][0:3])+ "|" + str(gen1[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen2)):
							if index%2 == 0:
								gen3.append(str(gen2[index][0:3])+ "|" + str(gen2[index+1][0:3]))
							else:
								continue
					elif gen_counter == 4:
						gen2 = []
						gen3 = []
						gen4 = []
						gen5 = ""
						gen6 = ""

						for index in range(0,len(gen1)):
							if index%2 == 0:
								gen2.append(str(gen1[index][0:3])+ "|" + str(gen1[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen2)):
							if index%2 == 0:
								gen3.append(str(gen2[index][0:3])+ "|" + str(gen2[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen3)):
							if index%2 == 0:
								gen4.append(str(gen3[index][0:3])+ "|" + str(gen3[index+1][0:3]))
							else:
								continue
					elif gen_counter == 5:
						gen2 = []
						gen3 = []
						gen4 = []
						gen5 = []
						gen6 = ""

						for index in range(0,len(gen1)):
							if index%2 == 0:
								gen2.append(str(gen1[index][0:3])+ "|" + str(gen1[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen2)):
							if index%2 == 0:
								gen3.append(str(gen2[index][0:3])+ "|" + str(gen2[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen3)):
							if index%2 == 0:
								gen4.append(str(gen3[index][0:3])+ "|" + str(gen3[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen4)):
							if index%2 == 0:
								gen5.append(str(gen4[index][0:3])+ "|" + str(gen4[index+1][0:3]))
							else:
								continue
					elif gen_counter == 6:
						gen2 = []
						gen3 = []
						gen4 = []
						gen5 = []
						gen6 = []

						for index in range(0,len(gen1)):
							if index%2 == 0:
								gen2.append(str(gen1[index][0:3])+ "|" + str(gen1[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen2)):
							if index%2 == 0:
								gen3.append(str(gen2[index][0:3])+ "|" + str(gen2[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen3)):
							if index%2 == 0:
								gen4.append(str(gen3[index][0:3])+ "|" + str(gen3[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen4)):
							if index%2 == 0:
								gen5.append(str(gen4[index][0:3])+ "|" + str(gen4[index+1][0:3]))
							else:
								continue

						for index in range(0,len(gen5)):
							if index%2 == 0:
								gen6.append(str(gen5[index][0:3])+ "|" + str(gen5[index+1][0:3]))
							else:
								continue
					else:
						gen2 = ""
						gen3 = ""
						gen4 = ""
						gen5 = ""
						gen6 = ""

					
					final_poke_string = ""

					iv_breeder = deepcopy(breedstats_abr)

				except Exception as e:
					prRed("Uh oh! Something went wrong...")
					print("Error: "+str(e))
					input("\033[94m\nPress Enter to return... \033[00m")			

		while editloop>0:
			clearscreen()
			

			pokepaint(gen1, gen2, gen3, gen4, gen5, gen6, stage, name, hp, atk, dfs, sat, sde, spe, nature_literal, breedstring, iv_amount, gen_counter, iv_breeder, nature_breeder, final_poke_string, braces_cost, everstone_cost, gender_cost_average)

			if stage.lower() == "final_present":
				editloop = 0
				loadloop = 0
				deployloop = 0
			else:
				pass

						

			comm = input("\033[94m\n\n Command ('help' for a list of commands): \033[00m")

			try:
				if comm.lower() == 'help':
					clearscreen()
					prGreen("\n--------------------------------\nAvailable Commands:"\
						"\n\n\n'exit' : Exits the current plan and takes you back to the previous screen."\
						"\n\n'help' : Brings you to this menu."\
						"\n\n'add [1-32] [role] [f|m]' : Add Pokémon to column 1-32, with gender f/m, with specific role (atk,def,etc.)."\
						"\n\n'rem [1-32]' : Remove Pokémon from column."\
						"\n\n'breed' : Breeds the Pokémon of the current stage." \
						"\n\n'explain' : Explains the use of commands (detailed help)." \
						"\n\n'save' : Saves the Pokémon and stages it for deployment."\
						"\n\n'reset' : Resets your Pokémon."\
						"\n\n--------------------------------")
					input("\033[94m\nPress Enter to return... \033[00m")
				elif comm.lower() == 'exit':
					clearscreen()
					leave = input("\033[93m\nNOTE! Unsaved changes will be lost!\033[00m\n\033[94mAre you sure you want to leave?\nY to confirm: \033[00m")
					if leave.lower() == "y":
						editloop=0
						loadloop=1
						break
					else:
						pass
				elif comm.startswith('add'):
					command = comm.split(" ")

					if command[2].lower() == "hp":
						command[2] = "hpt"
					
					if command[2].lower() in stat_abr or command[2].lower() == "hpt":
						if 1<=int(command[1])<breeders+1:
							if command[3].lower() == "f":
								gen1[int(command[1])-1] = (str(command[2].upper())+"/"+str(command[3].upper()))
							elif command[3].lower() == "m":
								gen1[int(command[1])-1] = (str(command[2].upper())+"/"+str(command[3].upper()))
							else:
								clearscreen()
								prYellow("\nERROR! Incorrect gender (add [1-32] [role] [f|m]).")
								input("\033[94m\nPress Enter to return... \033[00m")
						else:
							clearscreen()
							prYellow("\nERROR! Bad range (add [1-32] [role] [f|m]).")
							input("\033[94m\nPress Enter to return... \033[00m")
					else:
						if stage.lower() == "nat" and command[3].lower() == "nat":
							if 1<=int(command[1])<breeders+1:
								if command[3].lower() == "f":
									gen1[int(command[1])-1] = (str(command[2].upper())+"/"+str(command[3].upper()))
								elif command[3].lower() == "m":
									gen1[int(command[1])-1] = (str(command[2].upper())+"/"+str(command[3].upper()))
								else:
									clearscreen()
									prYellow("\nERROR! Incorrect gender (add [1-32] [role] [f|m]).")
									input("\033[94m\nPress Enter to return... \033[00m")
							else:
								clearscreen()
								prYellow("\nERROR! Bad range (add [1-32] [role] [f|m]).")
								input("\033[94m\nPress Enter to return... \033[00m")
						else:
							clearscreen()
							if stage == "nat":
								prYellow("\nERROR! Role wasn't an IV or 'nat' (add [1-32] [role] [f|m]).")
								input("\033[94m\nPress Enter to return... \033[00m")
							else:
								prYellow("\nERROR! Role wasn't an IV (add [1-32] [role] [f|m]).")
								input("\033[94m\nPress Enter to return... \033[00m")

				elif comm.startswith('rem'):
					if gen_counter<2:
						command = comm.split(" ")

						if 1<=int(command[1])<breeders+1:
							if len(str(command[1]))>1:
								gen1[int(command[1])-1] = str(command[1])+": STDBY"
							else:
								gen1[int(command[1])-1] = "0"+str(command[1])+": STDBY"
						
					else:
						clearscreen()
						prYellow("\nAfter breeding, Pokémon are locked. Go back to Gen 1 to unlock.")
						input("\033[94m\nPress Enter to return... \033[00m")
				
				elif comm.lower() == "breed":
					cancel = 0
					for each in gen1:
						if each == "STDBY":
							cancel = 1
							break
						else:
							pass

					if gen_counter == iv_amount:
						cancel = 2
					else:
						pass

					if cancel == 0:
						if stage.lower() == "iv":
							if gen_counter == 1:
								pairs = breeders/2
								breedstats_check_1 = list(breedstats_abr)
								breedstats_check_2 = list(breedstats_abr)
								delcount1 = 0
								delcount2 = 0

								for ind,stats_ch in enumerate(breedstats_abr):
									for i in range(0,int((len(gen1))/2)):
										if str(gen1[i][0:3]).lower() == str(stats_ch).lower():
											del breedstats_check_1[ind-delcount1]
											delcount1+=1
											break
										else:
											continue


								if len(breedstats_check_1) == 1:
									for ind,stats_ch in enumerate(breedstats_abr):					
										for i in range(int((len(gen1))/2), int(len(gen1))):
											if str(gen1[i][0:3]).lower() == str(stats_ch).lower():
												del breedstats_check_2[ind-delcount2]
												delcount2+=1
												break
											else:
												continue

									if len(breedstats_check_2) == 1:
										if breedstats_check_1[0] != breedstats_check_2[0]:
											cancel = 0
											for index,stats_ch in enumerate(gen1):
												if index%2 == 0:
													if stats_ch[-1] != gen1[index+1][-1]:
														continue
													else:
														clearscreen()
														prYellow("\nERROR! Pokémon in pair "+str(round(index/2))+" are the same gender!")
														input("\033[94m\nPress Enter to return... \033[00m")
														cancel = 1
														break

											if cancel == 0:
												gen2 = []

												for index in range(0,len(gen1)):
													if index%2 == 0:
														gen2.append(str(gen1[index][0:3])+ "|" + str(gen1[index+1][0:3]))
													else:
														continue

												gen_counter+=1

											else:
												pass

										else:
											clearscreen()
											prYellow("\nERROR! Can't breed generation. None of the groups produce the IV '"+str(breedstats_check_1[0])+")'.")
											input("\033[94m\nPress Enter to return... \033[00m")

									elif len(breedstats_check_1) == 0:
										clearscreen()
										prYellow("\nERROR! Can't breed generation. Group 2 has no overlapping IVs.")
										input("\033[94m\nPress Enter to return... \033[00m")

									else:
										breedstats_check_string = ", ".join(breedstats_check_2)
										clearscreen()
										prYellow("\nERROR! Can't breed generation. Next gen missing more than 1 IV ("+str(breedstats_check_string)+") in second group of pairs.")
										input("\033[94m\nPress Enter to return... \033[00m")

								elif len(breedstats_check_1) == 0:
									clearscreen()
									prYellow("\nERROR! Can't breed generation. Group 1 has no overlapping IVs.")
									input("\033[94m\nPress Enter to return... \033[00m")
									
								else:
									breedstats_check_string = ", ".join(breedstats_check_1)
									clearscreen()
									prYellow("\nERROR! Can't breed generation. Next gen missing more than 1 IV ("+str(breedstats_check_string)+") in first group of pairs.")
									input("\033[94m\nPress Enter to return... \033[00m")

							elif gen_counter == 2:							
								gen3 = []

								for index in range(0,len(gen2)):
									if index%2 == 0:
										gen3.append(str(gen2[index])+ "|" + str(gen2[index+1]))
									else:
										continue

								gen_counter+=1

							elif gen_counter == 3:
								gen4 = []

								for index in range(0,len(gen3)):
									if index%2 == 0:
										gen4.append(str(gen3[index])+ "|" + str(gen3[index+1]))
									else:
										continue

								gen_counter+=1

							elif gen_counter == 4:
								gen5 = []

								for index in range(0,len(gen4)):
									if index%2 == 0:
										gen5.append(str(gen4[index])+ "|" + str(gen4[index+1]))
									else:
										continue

								gen_counter+=1

							elif gen_counter == 5:
								gen6 = []

								for index in range(0,len(gen5)):
									if index%2 == 0:
										gen6.append(str(gen5[index])+ "|" + str(gen5[index+1]))
									else:
										continue

								gen_counter+=1

							else:
								pass
						elif stage.lower() == "nat":
							if gen_counter == 1:
								breedstats_abr_nat = list(breedstats_abr)
								breedstats_abr_nat.append("nat")
								pairs = breeders/2
								breedstats_check_1 = list(breedstats_abr_nat)
								breedstats_check_2 = list(breedstats_abr_nat)
								delcount1 = 0
								delcount2 = 0

								for ind,stats_ch in enumerate(breedstats_abr_nat):
									for i in range(0,int((len(gen1))/2)):
										if str(gen1[i][0:3]).lower() == str(stats_ch).lower():
											if str(gen1[i][0:3]).lower() == "nat":
												breedstats_check_2.remove('nat')
											del breedstats_check_1[ind-delcount1]
											delcount1+=1
											break
										else:
											continue


								if len(breedstats_check_1) == 1 or len(breedstats_check_1) == 2:
									for ind,stats_ch in enumerate(breedstats_abr_nat):					
										for i in range(int((len(gen1))/2), int(len(gen1))):
											if str(gen1[i][0:3]).lower() == str(stats_ch).lower():
												if str(gen1[i][0:3]).lower() == "nat":
													breedstats_check_1.remove('nat')
												del breedstats_check_2[ind-delcount2]
												delcount2+=1
												break
											else:
												continue

									if (len(breedstats_check_2) == 1 or len(breedstats_check_2) == 2) and (len(breedstats_check_2) != len(breedstats_check_1)):
										cancel = 0
										for index,stats_ch in enumerate(gen1):
											if index%2 == 0:
												if stats_ch[-1] != gen1[index+1][-1]:
													continue
												else:
													clearscreen()
													prYellow("\nERROR! Pokémon in pair "+str(round(index/2))+" are the same gender!")
													input("\033[94m\nPress Enter to return... \033[00m")
													cancel = 1
													break

										if "nat" not in breedstats_check_1 and "nat" not in breedstats_check_2:
											
											overlap_test = []
											for each in breedstats_check_1:
												overlap_test.append(each)
											for each in breedstats_check_2:
												overlap_test.append(each)

											overlap_test_unique = set(overlap_test)

											if len(overlap_test_unique) == 2:
												gen2 = []

												for index in range(0,len(gen1)):
													if index%2 == 0:
														gen2.append(str(gen1[index][0:3])+ "|" + str(gen1[index+1][0:3]))
													else:
														continue

												gen1_unique = set(gen1)
												for each in gen1_unique:
													nature_breeder.append(str(each[0:3]))

												gen_counter+=1

											else:
												clearscreen()
												prYellow("\nERROR! One IV from the Breeding IVs list must be left out!")
												input("\033[94m\nPress Enter to return... \033[00m")

										else:
											clearscreen()
											prYellow("\nERROR! Nature must be included exactly once (add [1-32] [f|m] nat.")
											input("\033[94m\nPress Enter to return... \033[00m")

									elif len(breedstats_check_1) == 0:
										clearscreen()
										prYellow("\nERROR! Can't breed generation. Group 2 has no overlapping IVs.")
										input("\033[94m\nPress Enter to return... \033[00m")

									else:
										if "nat" in breedstats_check_1 or "nat" in breedstats_check_2:
											clearscreen()
											prYellow("\nERROR! Can't breed generation. Nature was not included!")
											input("\033[94m\nPress Enter to return... \033[00m")
										else:
											breedstats_check_string = ", ".join(breedstats_check_2)
											clearscreen()
											prYellow("\nERROR! Can't breed generation. Next gen missing too many IVs or nature values ("+str(breedstats_check_string)+") in second group of pairs.")
											input("\033[94m\nPress Enter to return... \033[00m")

								elif len(breedstats_check_1) == 0:
									clearscreen()
									prYellow("\nERROR! Can't breed generation. Group 1 has no overlapping IVs.")
									input("\033[94m\nPress Enter to return... \033[00m")
									
								else:
									breedstats_check_string = ", ".join(breedstats_check_1)
									clearscreen()
									prYellow("\nERROR! Can't breed generation. Next gen missing too many IVs or nature values ("+str(breedstats_check_string)+") in first group of pairs.")
									input("\033[94m\nPress Enter to return... \033[00m")

							elif gen_counter == 2:							
								gen3 = []

								for index in range(0,len(gen2)):
									if index%2 == 0:
										gen3.append(str(gen2[index])+ "|" + str(gen2[index+1]))
									else:
										continue

								gen_counter+=1

							elif gen_counter == 3:
								gen4 = []

								for index in range(0,len(gen3)):
									if index%2 == 0:
										gen4.append(str(gen3[index])+ "|" + str(gen3[index+1]))
									else:
										continue

								gen_counter+=1

							elif gen_counter == 4:
								gen5 = []

								for index in range(0,len(gen4)):
									if index%2 == 0:
										gen5.append(str(gen4[index])+ "|" + str(gen4[index+1]))
									else:
										continue

								gen_counter+=1

							elif gen_counter == 5:
								gen6 = []

								for index in range(0,len(gen5)):
									if index%2 == 0:
										gen6.append(str(gen5[index])+ "|" + str(gen5[index+1]))
									else:
										continue

								gen_counter+=1

							else:
								pass

						elif stage.lower() == 'final':
							final_poke = []

							for each in iv_breeder:
								final_poke.append(each.upper())

							if len(nature_breeder)>1:
								for each in nature_breeder:
									if each.lower() != "nat":
										final_poke.append(each.upper())

								final_poke.append("NAT")

							final_poke = set(final_poke)

							final_poke_string = "|".join(final_poke)

							stage = 'final_present'


					elif cancel == 1:
						clearscreen()
						prYellow("\nERROR! Can't breed incomplete generation (found 'STDBY' placeholder).")
						input("\033[94m\nPress Enter to return... \033[00m")
					elif cancel == 2:
						clearscreen()
						prYellow("\nERROR! There is nothing to breed! If you just finished a build, type 'stage' to go to next stage.")
						input("\033[94m\nPress Enter to return... \033[00m")

				elif comm.lower() == 'back':
					if gen_counter>1:
						gen_counter-=1
					else:
						clearscreen()
						prYellow("\nERROR! You can't go back from the first generation! If you want to exit, type 'exit'.")
						input("\033[94m\nPress Enter to return... \033[00m")

				elif comm.lower() == 'stage':
					if gen_counter == iv_amount:
						clearscreen()
						proceed = input("\033[93m\nAre you sure you wish to proceed? You can't go back to the previous stage once done ('Y' to proceed).\033[00m")
						if str(proceed.lower()) == "y":
							gen_counter = 1
							if nature_literal.lower() != "none" and stage == "iv":
								stage = "nat"
								gen1_iv = deepcopy(gen1)
								for i in range(0,breeders):
									if len(str(i+1))>1:
										gen1[i] = str(i+1)+": STDBY"
									else:
										gen1[i] = "0"+str(i+1)+": STDBY"
							elif nature_literal.lower() == "none" and stage == "iv":
								stage = "final_present"
							elif stage == "nat":
								stage = "final"
							else:
								pass
						else:
							pass
					else:
						clearscreen()
						prYellow("\nERROR! You can't proceed to next stage before completing the current breeding stage (stage: "+str(stage)+")")
						input("\033[94m\nPress Enter to return... \033[00m")
			
				elif comm.lower() == 'save':
					sloop = 1

					while sloop>0:
						clearscreen()

						with open(filetemp, 'r') as f:
							lines = f.readlines()

						if stage.lower() == "iv":
							lines[10] = "stage::"+str(stage)+"\n"
							lines[11] = "gen_counter::"+str(gen_counter)+"\n"
							lines[13] = "gen1_iv::"+'|'.join(gen1)+"\n"
							prGreen("\nSuccessfully overwrote file '"+str(filetemp)+"'")
							input("\033[94m\nPress Enter to return... \033[00m")
							sloop=0
						elif stage.lower() == "nat":
							lines[10] = "stage::"+str(stage)+"\n"
							lines[11] = "gen_counter::"+str(gen_counter)+"\n"
							lines[13] = "gen1_iv::"+'|'.join(gen1_iv)+"\n"
							lines[14] = "gen1_nat::"+'|'.join(gen1)
							prGreen("\nSuccessfully overwrote file '"+str(filetemp)+"'")
							input("\033[94m\nPress Enter to return... \033[00m")
							sloop=0
						else:
							prGreen("\nYou have entered the final stages of the breeding - save function unavailable.")
							input("\033[94m\nPress Enter to return... \033[00m")
							sloop=0

						with open(filetemp, 'w') as f:
							f.writelines(lines)


				else:
					clearscreen()
					prYellow("\nYour input was an unrecognized command!")
					input("\033[94m\nPress Enter to return... \033[00m")


			except Exception as e:
				clearscreen()
				prYellow("\nERROR! User inputted incorrectly formatted command.\nRemember, you can type 'help' if you're unsure of the syntax.")
				print("ERROR : "+str(e))
				input("\033[94m\nPress Enter to return... \033[00m")



def pokecreate():
	clearscreen()
	prGreen("Okay, time to create a custom Pokémon!\n Remember, you can always type 'help' for assistance!")

	name = input("\033[94m\n First, input a name for your Pokémon: \033[00m")
	name = str(name).strip()
	if name.strip() == "":
		clearscreen()
		prYellow("\nERROR! Name must contain at least one character.")
		input("\033[94m\nPress Enter to return... \033[00m")

		createloop = 0

	else:
		hp = "\033[91m 0\033[00m"
		hp_literal = 0
		atk = "\033[91m 0\033[00m"
		atk_literal = 0
		dfs = "\033[91m 0\033[00m"
		dfs_literal = 0
		sat = "\033[91m 0\033[00m"
		sat_literal = 0
		sde = "\033[91m 0\033[00m"
		sde_literal = 0
		spe = "\033[91m 0\033[00m"
		spe_literal = 0
		nature = "None"
		nature_literal = "none"

		cost = 0
		braces = 0
		braces_nat = 0
		breeders = 0
		everstones = 0
		genders = 0
		n = 0

		createloop = 1

	while createloop>0:
		clearscreen()

		pokemon = OrderedDict([("Name", name), ("HP", hp_literal), ("Attack", atk_literal), ("Defense", dfs_literal), ("Sp.Atk", sat_literal), ("Sp.Def", sde_literal), ("Speed", spe_literal), ("Nature", nature_literal)])

		n = 0

		if pokemon["HP"] != 0:
			n+=1
		if pokemon["Attack"] != 0:
			n+=1
		if pokemon["Defense"] != 0:
			n+=1
		if pokemon["Sp.Atk"] != 0:
			n+=1
		if pokemon["Sp.Def"] != 0:
			n+=1
		if pokemon["Speed"] != 0:
			n+=1

		if n == 0:
			breeders = 0
		else:
			breeders = 2**(n-1)
		if n == 0:
			braces = 0
		else:
			braces = (2**n)-2

		if nature_literal != "none":
			braces_nat = ((2**n)-2)-(n-1)
		else:
			braces_nat = 0

		if nature_literal != "none":
			everstones = n
		else:
			everstones = 0

		if n == 0:
			genders = 0
		else:
			if nature_literal != "none":
				genders = round(2**(n-2))
			else:
				genders = round((2**(n-2))*2)

		
		prPurple("\nPokémon name: "+name+"\n")

		print(" |   HP    | ATTACK  | DEFENSE |  SP_ATK |  SP_DEF |  SPEED  |")
		print(" |   "+str(hp)+"    |   "+str(atk)+"    |   "+str(dfs)+"    |   "+str(sat)+"    |   "+str(sde)+"    |   "+str(spe)+"    |")



		if nature == "None":
			print("\n Nature: "+str(nature))
		else:
			print("\n Nature: \033[92m"+str(nature)+"\033[00m")

		print("\n First gen breeders         : "+str(breeders))
		print(" Braces from IV breeding    : "+str(braces))
		print(" Braces from nat breeding   : "+str(braces_nat))
		print(" Total braces               : "+str(braces+braces_nat))
		print(" Minimum everstones         : "+str(everstones))
		print(" Gender selections          : "+str(genders))

		cost = braces_cost*(braces + braces_nat) + everstone_cost*everstones + genders*gender_cost_average

		print("\n\n Estimated cost: \033[92m$ "+str(cost)+(12-len(str(cost)))*" "+"\033[00m<- Does not include cost of Pokéballs or breeder purchases")

		comm = input("\033[94m\n\n Command ('help' for a list of commands): \033[00m")


		try:
			if comm.lower() == 'help':
				clearscreen()
				prGreen("\n--------------------------------\nAvailable Commands:"\
					"\n\n\n'exit' : Exits the current plan and takes you back to the previous screen."\
					"\n\n'help' : Brings you to this menu."\
					"\n\n'{hp|atk|def|sat|sde|spe} [0-31]' : sets the \{attribute} to [0-31] (ex: hp 31)"\
					"\n\n'nature [nature]' : Sets the nature to nature in nature-list"\
					"\n\n'natures' : Shows a list of natures."
					"\n\n'save' : Saves the Pokémon and stages it for deployment."\
					"\n\n'reset' : Resets your Pokémon."\
					"\n\n'max' : Maximizes your Pokémon's IVs."\
					"\n\n--------------------------------")
				input("\033[94m\nPress Enter to return... \033[00m")
			elif comm.lower() == 'exit':
				clearscreen()
				leave = input("\033[93m\nNOTE! Unsaved changes will be lost!\033[00m\n\033[94mAre you sure you want to leave?\nY/N: \033[00m")
				if leave == "Y" or leave == "y":
					createloop=0
					break
				else:
					pass
			elif comm.lower() == 'natures':
				clearscreen()
				prPurple("Natures (lower = debuff, upper = buff)\n")
				prGreen("|  *****  |  attack | defense |  spatk  |  spdef  |  speed  |")
				prGreen("| ATTACK  |  Hardy  | Lonely  | Adamant | Naughty |  Brave  |")
				prGreen("| DEFENSE |  Bold   | Docile  | Impish  |   Lax   | Relaxed |")
				prGreen("|  SPATK  |  Modest |  Mild   | Bashful |  Rash   |  Quiet  |")
				prGreen("|  SPDEF  |  Calm   | Gentle  | Careful | Quirky  |  Sassy  |")
				prGreen("|  SPEED  |  Timid  |  Hasty  |  Jolly  |  Naive  | Serious |")
				input("\033[94m\nPress Enter to return... \033[00m")
			elif comm.lower() == 'reset':
				hp = "\033[91m 0\033[00m"
				hp_literal = 0
				atk = "\033[91m 0\033[00m"
				atk_literal = 0
				dfs = "\033[91m 0\033[00m"
				dfs_literal = 0
				sat = "\033[91m 0\033[00m"
				sat_literal = 0
				sde = "\033[91m 0\033[00m"
				sde_literal = 0
				spe = "\033[91m 0\033[00m"
				spe_literal = 0
				nature = "None"
				nature_literal = "none"
				clearscreen()
			elif comm.lower() == 'max':
				hp = "\033[92m31\033[00m"
				hp_literal = 31
				atk = "\033[92m31\033[00m"
				atk_literal = 31
				dfs = "\033[92m31\033[00m"
				dfs_literal = 31
				sat = "\033[92m31\033[00m"
				sat_literal = 31
				sde = "\033[92m31\033[00m"
				sde_literal = 31
				spe = "\033[92m31\033[00m"
				spe_literal = 31
				clearscreen()
			elif comm.startswith("hp"):
				command = comm.split(' ')
				hp_t = int(command[1])
				if 0<=hp_t<=31:
					hp_literal = hp_t
				if hp_t == 0:
					hp = "\033[91m 0\033[00m"
				elif 1<=hp_t<=9:
					hp = " "+str(hp_t)
				elif 10<=hp_t<=30:
					hp = str(hp_t)
				elif hp_t == 31:
					hp = "\033[92m31\033[00m"
				else:
					clearscreen()
					prYellow("\nERROR! HP value was not allowed.")
					input("\033[94m\nPress Enter to return... \033[00m")
			elif comm.startswith("atk"):
				command = comm.split(' ')
				atk_t = int(command[1])
				if 0<=atk_t<=31:
					atk_literal = atk_t
				if atk_t == 0:
					atk = "\033[91m 0\033[00m"
				elif 1<=atk_t<=9:
					atk = " "+str(atk_t)
				elif 10<=atk_t<=30:
					atk = str(atk_t)
				elif atk_t == 31:
					atk = "\033[92m31\033[00m"
				else:
					clearscreen()
					prYellow("\nERROR! ATK value was not allowed.")
					input("\033[94m\nPress Enter to return... \033[00m")
			elif comm.startswith("def"):
				command = comm.split(' ')
				dfs_t = int(command[1])
				if 0<=dfs_t<=31:
					dfs_literal = dfs_t
				if dfs_t == 0:
					dfs = "\033[91m 0\033[00m"
				elif 1<=dfs_t<=9:
					dfs = " "+str(dfs_t)
				elif 10<=dfs_t<=30:
					dfs = str(dfs_t)
				elif dfs_t == 31:
					dfs = "\033[92m31\033[00m"
				else:
					clearscreen()
					prYellow("\nERROR! DEF value was not allowed.")
					input("\033[94m\nPress Enter to return... \033[00m")
			elif comm.startswith("sat"):
				command = comm.split(' ')
				sat_t = int(command[1])
				if 0<=sat_t<=31:
					sat_literal = sat_t
				if sat_t == 0:
					sat = "\033[91m 0\033[00m"
				elif 1<=sat_t<=9:
					sat = " "+str(sat_t)
				elif 10<=sat_t<=30:
					sat = str(sat_t)
				elif sat_t == 31:
					sat = "\033[92m31\033[00m"
				else:
					clearscreen()
					prYellow("\nERROR! SAT value was not allowed.")
					input("\033[94m\nPress Enter to return... \033[00m")
			elif comm.startswith("sde"):
				command = comm.split(' ')
				sde_t = int(command[1])
				if 0<=sde_t<=31:
					sde_literal = sde_t
				if sde_t == 0:
					sde = "\033[91m 0\033[00m"
				elif 1<=sde_t<=9:
					sde = " "+str(sde_t)
				elif 10<=sde_t<=30:
					sde = str(sde_t)
				elif sde_t == 31:
					sde = "\033[92m31\033[00m"
				else:
					clearscreen()
					prYellow("\nERROR! SDE value was not allowed.")
					input("\033[94m\nPress Enter to return... \033[00m")
			elif comm.startswith("spe"):
				command = comm.split(' ')
				spe_t = int(command[1])
				if 0<=spe_t<=31:
					spe_literal = spe_t
				if spe_t == 0:
					spe = "\033[91m 0\033[00m"
				elif 1<=spe_t<=9:
					spe = " "+str(spe_t)
				elif 10<=spe_t<=30:
					spe = str(spe_t)
				elif spe_t == 31:
					spe = "\033[92m31\033[00m"
				else:
					clearscreen()
					prYellow("\nERROR! SPE value was not allowed.")
					input("\033[94m\nPress Enter to return... \033[00m")
			elif comm.startswith("nature"):
				command = comm.split(' ')

				if command[1].lower() in natures:
					nature = command[1].capitalize()
					nature_literal = command[1].lower()
				else:
					clearscreen()
					prYellow("\nERROR! Nature value was not allowed.")
					input("\033[94m\nPress Enter to return... \033[00m")
			elif comm.lower() == 'save':
				sloop = 1

				while sloop>0:
					clearscreen()
					filename = input("\n\033[92mPlease type a save name for your save file, and then hit Enter (or 'exit' to go back): \033[00m") + '.breed'

					if filename.lower() == "exit.breed":
						sloop = 0
						continue
					if (os.path.isfile(filename)):
						menuheader_s = ("\n  \033[92mNOTE! This file already exists. Do you want to overwrite it?\033[00m")
						optionlist_s = ["\n  \033[0;32;47m(1) Yes\033[0m\n  \033[92m(2) No\033[00m", "\n  \033[92m(1) Yes\033[00m\n  \033[0;32;47m(2) No\033[0m"]	
						overwrite = menues(optionlist_s,menuheader_s)

						try:
							clearscreen()
							if overwrite == 0:
								os.remove(filename)
								breedfile = open(filename, "a+")
								breedfile.write("Name::"+str(pokemon["Name"]))		#0
								breedfile.write("\nHP/Attack/Defense/Sp.Atk/Sp.Def/Speed::"+str(pokemon["HP"])+"/"+str(pokemon["Attack"])+"/"+str(pokemon["Defense"])+"/"+str(pokemon["Sp.Atk"])+"/"+str(pokemon["Sp.Def"])+"/"+str(pokemon["Speed"]))
								breedfile.write("\nNature::"+str(nature_literal))	#2
								breedfile.write("\nbreeders::"+str(breeders))		#3
								breedfile.write("\nbraces::"+str(braces))			#4
								breedfile.write("\nbraces_nat::"+str(braces_nat))	#5
								breedfile.write("\neverstones::"+str(everstones))	#6
								breedfile.write("\ngender::"+str(genders))			#7
								breedfile.write("\ncost::"+str(cost))				#8
								breedfile.write("\n***")							#9
								breedfile.write("\nstage:: ")						#10
								breedfile.write("\ngen_counter:: ")					#11
								breedfile.write("\n***")							#12
								breedfile.write("\ngen1_iv:: ")						#13
								breedfile.write("\ngen1_nat:: ")					#14
								breedfile.close()
								prGreen("\nSuccessfully overwrote file '"+str(filename)+"'")
								input("\033[94m\nPress Enter to return... \033[00m")
								sloop=0

							elif overwrite == 1:
								sloop = 0
								
						except Exception as e:
							prRed("Uh oh! Something went wrong...")
							print("ERROR : "+str(e))
							input("\033[94m\nPress Enter to return... \033[00m")

					else:
						breedfile = open(filename, "a+")
						breedfile.write("Name::"+str(pokemon["Name"]))		#0
						breedfile.write("\nHP/Attack/Defense/Sp.Atk/Sp.Def/Speed::"+str(pokemon["HP"])+"/"+str(pokemon["Attack"])+"/"+str(pokemon["Defense"])+"/"+str(pokemon["Sp.Atk"])+"/"+str(pokemon["Sp.Def"])+"/"+str(pokemon["Speed"]))
						breedfile.write("\nNature::"+str(nature_literal))	#2
						breedfile.write("\nbreeders::"+str(breeders))		#3
						breedfile.write("\nbraces::"+str(braces))			#4
						breedfile.write("\nbraces_nat::"+str(braces_nat))	#5
						breedfile.write("\neverstones::"+str(everstones))	#6
						breedfile.write("\ngender::"+str(genders))			#7
						breedfile.write("\ncost::"+str(cost))				#8
						breedfile.write("\n***")							#9
						breedfile.write("\nstage:: ")						#10
						breedfile.write("\ngen_counter:: ")					#11
						breedfile.write("\n***")							#12
						breedfile.write("\ngen1_iv:: ")						#13
						breedfile.write("\ngen1_nat:: ")					#14
						breedfile.close()
						prGreen("\nSuccessfully created file '"+str(filename)+"'")
						input("\033[94m\nPress Enter to return... \033[00m")
						sloop=0
						createloop=0

			else:
					clearscreen()
					prYellow("\nYour input was an unrecognized command!")
					input("\033[94m\nPress Enter to return... \033[00m")


		except Exception as e:
				clearscreen()
				prYellow("\nERROR! User inputted incorrectly formatted command.\nRemember, you can type 'help' if you're unsure of the syntax.")
				print("ERROR : "+str(e))
				input("\033[94m\nPress Enter to return... \033[00m")


def pokepaint(gen1, gen2, gen3, gen4, gen5, gen6, stage, name, hp, atk, dfs, sat, sde, spe, nature_literal, breedstring, iv_amount, gen_counter, iv_breeder, nature_breeder, final_poke_string, braces_cost, everstone_cost, gender_cost_average):
	if stage.lower() == "iv":
		rows = len(gen1)

		prPurple("CURRENT STAGE          : "+str(stage).upper())
		print("")
		prPurple("Desired Pokémon Profile : "+str(name)+", "+str(hp)+"/"+str(atk)+"/"+str(dfs)+"/"+str(sat)+"/"+str(sde)+"/"+str(spe)+", Nature: "+str(nature_literal))
		print("")
		print(" Breeding IVs            : "+str(breedstring))
		print(" Total Required Breedings: "+str(2**(iv_amount-1)-1))
		print("\n")
		
		if gen_counter == 1:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if gen1[index][-1].lower() == "m":
					print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m")
					braces_dict[str(gen1[index][0:3].lower())]+=1
				elif gen1[index][-1].lower() == "f":
					print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m")
					braces_dict[str(gen1[index][0:3].lower())]+=1
				else:
					print(gen1[index])

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic IV profile ATTAINED.")
				prPurple("IVs have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 2:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if index%2 == 0:
					if index%4 == 0:
						gen2_string1,gen2_string2,braces_dict = gen2_func(gen2,index,braces_dict)
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1)	
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
				else:
					if gen1[index][-1].lower() == "m":
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic IV profile ATTAINED.")
				prPurple("IVs have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 3:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2            STAGE 3")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if index%4 == 0:
					braces_save = deepcopy(braces_dict)
					gen2_string1,gen2_string2,_ = gen2_func(gen2,index,braces_dict)
					braces_dict = deepcopy(braces_save)
					if index%8 == 0:
						gen3_string1,gen3_string2,braces_dict = gen3_func(gen3,index,braces_dict)
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1)
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)

				elif index%2 == 0:
					if gen1[index][-1].lower() == "m":
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
					else:
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)

				else:
					if gen1[index][-1].lower() == "m":
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic IV profile ATTAINED.")
				prPurple("IVs have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 4:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2            STAGE 3            STAGE 4")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if index%4 == 0:
					braces_save = deepcopy(braces_dict)
					gen2_string1,gen2_string2,braces_dict = gen2_func(gen2,index,braces_dict)
					braces_dict = deepcopy(braces_save)
					if index%8 == 0:
						braces_save = deepcopy(braces_dict)
						gen3_string1,gen3_string2,braces_dict = gen3_func(gen3,index,braces_dict)
						braces_dict = deepcopy(braces_save)
						if index%16 == 0:
							gen4_string1,gen4_string2,braces_dict = gen4_func(gen4,index,braces_dict)
							if gen1[index][-1].lower() == "m":
								print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1)
							else:
								print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1)
						else:
							if gen1[index][-1].lower() == "m":
								print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
							else:
								print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
				elif index%2 == 0:
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
		
				else:
					if gen1[index][-1].lower() == "m":
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic IV profile ATTAINED.")
				prPurple("IVs have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 5:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2            STAGE 3            STAGE 4            STAGE 5")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if index%4 == 0:
					braces_save = deepcopy(braces_dict)
					gen2_string1,gen2_string2,braces_dict = gen2_func(gen2,index,braces_dict)
					braces_dict = deepcopy(braces_save)
					if index%8 == 0:
						braces_save = deepcopy(braces_dict)
						gen3_string1,gen3_string2,braces_dict = gen3_func(gen3,index,braces_dict)
						braces_dict = deepcopy(braces_save)
						if index%16 == 0:
							braces_save = deepcopy(braces_dict)
							gen4_string1,gen4_string2,braces_dict = gen4_func(gen4,index,braces_dict)
							braces_dict = deepcopy(braces_save)
							if index%32 == 0:
								gen5_string1,gen5_string2,braces_dict = gen5_func(gen5,index,braces_dict)
								if gen1[index][-1].lower() == "m":
									print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1)
								else:
									print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1)
							else:
								if gen1[index][-1].lower() == "m":
									print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string2)
								else:
									print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string2)
						else:
							if gen1[index][-1].lower() == "m":
								print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
							else:
								print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
				elif index%2 == 0:
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
		
				else:
					if gen1[index][-1].lower() == "m":
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic IV profile ATTAINED.")
				prPurple("IVs have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 6:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2            STAGE 3            STAGE 4            STAGE 5              STAGE 6")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if index%4 == 0:
					braces_save = deepcopy(braces_dict)
					gen2_string1,gen2_string2,braces_dict = gen2_func(gen2,index,braces_dict)
					braces_dict = deepcopy(braces_save)
					if index%8 == 0:
						braces_save = deepcopy(braces_dict)
						gen3_string1,gen3_string2,braces_dict = gen3_func(gen3,index,braces_dict)
						braces_dict = deepcopy(braces_save)
						if index%16 == 0:
							braces_save = deepcopy(braces_dict)
							gen4_string1,gen4_string2,braces_dict = gen4_func(gen4,index,braces_dict)
							braces_dict = deepcopy(braces_save)
							if index%32 == 0:
								braces_save = deepcopy(braces_dict)
								gen5_string1,gen5_string2,braces_dict = gen5_func(gen5,index,braces_dict)
								braces_dict = deepcopy(braces_save)
								if index%64 == 0:
									gen6_string1,gen6_string2,braces_dict = gen6_func(gen6,index,braces_dict)
									if gen1[index][-1].lower() == "m":
										print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1+"  "+gen6_string1)
									else:
										print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1+"  "+gen6_string1)
								else:
									if gen1[index][-1].lower() == "m":
										print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1+"  "+gen6_string2)
									else:
										print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1+"  "+gen6_string2)
							else:
								if gen1[index][-1].lower() == "m":
									print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string2)
								else:
									print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string2)
						else:
							if gen1[index][-1].lower() == "m":
								print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
							else:
								print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
				elif index%2 == 0:
						if gen1[index][-1].lower() == "m":
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
						else:
							print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
		
				else:
					if gen1[index][-1].lower() == "m":
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(line+"\033[92m"+str(gen1[index][0:3])+"\033[00m/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic IV profile ATTAINED.")
				prPurple("IVs have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		if gen_counter != iv_amount:
			print("\n")
			prGreen("NOTE: Green = IV-brace")
			prGreen("NOTE: Gen2 and beyond assumes correct genders")
			genbrace = ""
			for keys in braces_dict:
				genbrace = genbrace + str(keys)+": "+str(braces_dict[keys])+", "
			print(" Braces needed this generation::  "+str(genbrace[:-2]))


	elif stage.lower() == "nat":
		rows = len(gen1)

		prPurple("CURRENT STAGE          : "+str(stage).upper())
		print("")
		prPurple("Desired Pokémon Profile : "+str(name)+", "+str(hp)+"/"+str(atk)+"/"+str(dfs)+"/"+str(sat)+"/"+str(sde)+"/"+str(spe)+", Nature: "+str(nature_literal))
		print("")
		print(" Breeding IVs            : "+str(breedstring))
		print(" Total Required Breedings: "+str(2**(iv_amount-1)-1))
		print("\n")
		if gen_counter == 1:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if gen1[index][0:3].lower() == "nat":
					gen1_string = "\033[93m"+str(gen1[index][0:3])+"\033[00m"
				else:
					gen1_string = "\033[92m"+str(gen1[index][0:3])+"\033[00m"


				if gen1[index][-1].lower() == "m":
					print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m")
					if gen1[index][0:3].lower() == "nat":
						pass
					else:
						braces_dict[str(gen1[index][0:3].lower())]+=1
				elif gen1[index][-1].lower() == "f":
					print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m")
					if gen1[index][0:3].lower() == "nat":
						pass
					else:
						braces_dict[str(gen1[index][0:3].lower())]+=1
				else:
					print(gen1[index])

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic nature profile ATTAINED.")
				prPurple("Desired nature have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 2:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if gen1[index][0:3].lower() == "nat":
					gen1_string = "\033[93m"+str(gen1[index][0:3])+"\033[00m"
				else:
					gen1_string = "\033[92m"+str(gen1[index][0:3])+"\033[00m"

				if index%2 == 0:
					if index%4 == 0:
						gen2_string1,gen2_string2,braces_dict = gen2_func(gen2,index,braces_dict)
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1)	
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
				else:
					if gen1[index][-1].lower() == "m":
						print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic nature profile ATTAINED.")
				prPurple("Desired nature have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 3:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2            STAGE 3")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if gen1[index][0:3].lower() == "nat":
					gen1_string = "\033[93m"+str(gen1[index][0:3])+"\033[00m"
				else:
					gen1_string = "\033[92m"+str(gen1[index][0:3])+"\033[00m"

				if index%4 == 0:
					braces_save = deepcopy(braces_dict)
					gen2_string1,gen2_string2,_ = gen2_func(gen2,index,braces_dict)
					braces_dict = deepcopy(braces_save)
					if index%8 == 0:
						gen3_string1,gen3_string2,braces_dict = gen3_func(gen3,index,braces_dict)
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1)
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)

				elif index%2 == 0:
					if gen1[index][-1].lower() == "m":
						print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
					else:
						print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)

				else:
					if gen1[index][-1].lower() == "m":
						print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic nature profile ATTAINED.")
				prPurple("Desired nature have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 4:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2            STAGE 3            STAGE 4")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if gen1[index][0:3].lower() == "nat":
					gen1_string = "\033[93m"+str(gen1[index][0:3])+"\033[00m"
				else:
					gen1_string = "\033[92m"+str(gen1[index][0:3])+"\033[00m"

				if index%4 == 0:
					braces_save = deepcopy(braces_dict)
					gen2_string1,gen2_string2,braces_dict = gen2_func(gen2,index,braces_dict)
					braces_dict = deepcopy(braces_save)
					if index%8 == 0:
						braces_save = deepcopy(braces_dict)
						gen3_string1,gen3_string2,braces_dict = gen3_func(gen3,index,braces_dict)
						braces_dict = deepcopy(braces_save)
						if index%16 == 0:
							gen4_string1,gen4_string2,braces_dict = gen4_func(gen4,index,braces_dict)
							if gen1[index][-1].lower() == "m":
								print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1)
							else:
								print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1)
						else:
							if gen1[index][-1].lower() == "m":
								print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
							else:
								print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
				elif index%2 == 0:
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
		
				else:
					if gen1[index][-1].lower() == "m":
						print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic nature profile ATTAINED.")
				prPurple("Desired nature have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 5:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2            STAGE 3            STAGE 4            STAGE 5")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if gen1[index][0:3].lower() == "nat":
					gen1_string = "\033[93m"+str(gen1[index][0:3])+"\033[00m"
				else:
					gen1_string = "\033[92m"+str(gen1[index][0:3])+"\033[00m"

				if index%4 == 0:
					braces_save = deepcopy(braces_dict)
					gen2_string1,gen2_string2,braces_dict = gen2_func(gen2,index,braces_dict)
					braces_dict = deepcopy(braces_save)
					if index%8 == 0:
						braces_save = deepcopy(braces_dict)
						gen3_string1,gen3_string2,braces_dict = gen3_func(gen3,index,braces_dict)
						braces_dict = deepcopy(braces_save)
						if index%16 == 0:
							braces_save = deepcopy(braces_dict)
							gen4_string1,gen4_string2,braces_dict = gen4_func(gen4,index,braces_dict)
							braces_dict = deepcopy(braces_save)
							if index%32 == 0:
								gen5_string1,gen5_string2,braces_dict = gen5_func(gen5,index,braces_dict)
								if gen1[index][-1].lower() == "m":
									print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1)
								else:
									print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1)
							else:
								if gen1[index][-1].lower() == "m":
									print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string2)
								else:
									print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string2)
						else:
							if gen1[index][-1].lower() == "m":
								print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
							else:
								print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
				elif index%2 == 0:
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
		
				else:
					if gen1[index][-1].lower() == "m":
						print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(lline+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic nature profile ATTAINED.")
				prPurple("Desired nature have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		elif gen_counter == 6:
			braces_dict = {"hpt":0,"atk":0,"def":0,"sat":0,"sde":0,"spe":0}
			print("    STAGE 1            STAGE 2            STAGE 3            STAGE 4            STAGE 5              STAGE 6")
			print("\n")
			for index in range(0,rows):
				if len(str(index+1)) ==1:
					line = "0" + str(index+1) + ": "
				else:
					line = str(index+1) + ": "

				if gen1[index][0:3].lower() == "nat":
					gen1_string = "\033[93m"+str(gen1[index][0:3])+"\033[00m"
				else:
					gen1_string = "\033[92m"+str(gen1[index][0:3])+"\033[00m"

				if index%4 == 0:
					braces_save = deepcopy(braces_dict)
					gen2_string1,gen2_string2,braces_dict = gen2_func(gen2,index,braces_dict)
					braces_dict = deepcopy(braces_save)
					if index%8 == 0:
						braces_save = deepcopy(braces_dict)
						gen3_string1,gen3_string2,braces_dict = gen3_func(gen3,index,braces_dict)
						braces_dict = deepcopy(braces_save)
						if index%16 == 0:
							braces_save = deepcopy(braces_dict)
							gen4_string1,gen4_string2,braces_dict = gen4_func(gen4,index,braces_dict)
							braces_dict = deepcopy(braces_save)
							if index%32 == 0:
								braces_save = deepcopy(braces_dict)
								gen5_string1,gen5_string2,braces_dict = gen5_func(gen5,index,braces_dict)
								braces_dict = deepcopy(braces_save)
								if index%64 == 0:
									gen6_string1,gen6_string2,braces_dict = gen6_func(gen6,index,braces_dict)
									if gen1[index][-1].lower() == "m":
										print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1+"  "+gen6_string1)
									else:
										print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1+"  "+gen6_string1)
								else:
									if gen1[index][-1].lower() == "m":
										print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1+"  "+gen6_string2)
									else:
										print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string1+"  "+gen6_string2)
							else:
								if gen1[index][-1].lower() == "m":
									print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string2)
								else:
									print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string1+"    "+gen5_string2)
						else:
							if gen1[index][-1].lower() == "m":
								print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
							else:
								print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string1+"        "+gen4_string2)
					else:
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string1+"            "+gen3_string2)
				elif index%2 == 0:
						if gen1[index][-1].lower() == "m":
							print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
						else:
							print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m              "+gen2_string2)
		
				else:
					if gen1[index][-1].lower() == "m":
						print(line+gen1_string+"/\033[94m"+str(gen1[index][-1])+"\033[00m")
					else:
						print(line+gen1_string+"/\033[91m"+str(gen1[index][-1])+"\033[00m")

			if gen_counter == iv_amount:
				print("\n")
				prPurple("Pokémon genetic nature profile ATTAINED.")
				prPurple("Desired nature have been reached at iteration "+str(gen_counter)+".")
				prGreen("No further breeding possible. To go to the next stage, type 'stage' and hit enter.")

		if gen_counter != iv_amount:
			print("\n")
			prGreen("NOTE: Green = IV-brace")
			prGreen("NOTE: Gen2 and beyond assumes correct genders")
			genbrace = ""
			for keys in braces_dict:
				genbrace = genbrace + str(keys)+": "+str(braces_dict[keys])+", "
			print(" Braces needed this generation::  "+str(genbrace[:-2]))

	elif stage.lower() == "final":
		prPurple("CURRENT STAGE          : "+str(stage).upper())
		print("")
		prPurple("Desired Pokémon Profile : "+str(name)+", "+str(hp)+"/"+str(atk)+"/"+str(dfs)+"/"+str(sat)+"/"+str(sde)+"/"+str(spe)+", Nature: "+str(nature_literal))
		print("")
		print(" Breeding IVs            : "+str(breedstring))
		print("\n")

		nature_string = ""
		iv_string = ""

		for each in iv_breeder:
			if each.upper() in nature_breeder:
				iv_string = iv_string + str(each).upper() + "|"
			else:
				iv_string = iv_string + "\033[92m"+str(each).upper()+"\033[00m" + "|"

		for each in nature_breeder:
			if each.lower() == "nat":
				nature_string = nature_string + "\033[93m"+str(each).upper()+"\033[00m" + "|"
			else:
				nature_string = nature_string + str(each).upper() + "|"

		iv_string = iv_string[0:-1]
		nature_string = nature_string[0:-1]

		spaces1 = round((len(iv_string)-10)/2)*" "
		spaces2 = ((len(iv_string)-10)//2)*" "+((len(nature_string)-10)//2)*" "

		print(spaces1+"IV STAT"+spaces2+"NATURED")
		print("\n")
		print("    "+iv_string+"      "+nature_string+"    ")

	elif stage.lower() == "final_present":
		value_top = round(cost*1.5)
		print("\n\n")
		prPurple("All Pokémon criteria met - the breeding process is completed!\n\n")
		print("-------- REPORT --------\n")
		prPurple("Pokémon breeding profile   : "+final_poke_string)
		prPurple("Pokémon breeding specifics : "+name+", "+str(hp)+"/"+str(atk)+"/"+str(dfs)+"/"+str(sat)+"/"+str(sde)+"/"+str(spe)+", "+nature_literal)
		print("------------------------")
		prGreen("Estimated value: $ "+str(cost))+" - $ "+str(value_top)
		print(" (Value is dependent on many factors - value above doesn't necessarily reflect actual GTL value)")

	else:
		pass

def gen2_func(gen2,index,braces_dict=None):
	if len(gen2)>1:
		check1 = gen2[index//2].split("|")
		check2 = gen2[(index//2)+1].split("|")

		gen2_string1list = []
		gen2_string2list = []

		gen2_string1list_check = []
		gen2_string2list_check = []

		for each1 in check1:
			if each1 not in gen2_string1list_check:
				if each1 in check2:
					gen2_string1list.append(each1)
					gen2_string1list_check.append(each1)
				else:
					if each1.lower() == "nat":
						gen2_string1list.append("\033[93m"+str(each1)+"\033[00m")
						gen2_string1list_check.append(each1)
					else:
						gen2_string1list.append("\033[92m"+str(each1)+"\033[00m")
						gen2_string1list_check.append(each1)
						braces_dict[str(each1).lower()]+=1
			else:
				pass

		for each2 in check2:
			if each2 not in gen2_string2list_check:
				if each2 in check1:
					gen2_string2list.append(each2)
					gen2_string2list_check.append(each2)
				else:
					if each2.lower() == "nat":
						gen2_string2list.append("\033[93m"+str(each2)+"\033[00m")
						gen2_string2list_check.append(each2)
					else:
						gen2_string2list.append("\033[92m"+str(each2)+"\033[00m")
						gen2_string2list_check.append(each2)
						braces_dict[str(each2).lower()]+=1
			else:
				pass

		gen2_string1 = "|".join(gen2_string1list)
		gen2_string2 = "|".join(gen2_string2list)
	else:
		check1 = gen2[index//2].split("|")
		check1_clean = set(check1)

		gen2_string1 = "|".join(check1_clean)
		gen2_string2 = None

	return gen2_string1,gen2_string2,braces_dict

def gen3_func(gen3,index,braces_dict=None):
	if len(gen3)>1:
		check1 = gen3[index//4].split("|") #index is from gen1
		check2 = gen3[(index//4)+1].split("|")

		gen3_string1list = []
		gen3_string2list = []

		gen3_string1list_check = []
		gen3_string2list_check = []

		for each1 in check1:
			if each1 not in gen3_string1list_check:
				if each1 in check2:
					gen3_string1list.append(each1)
					gen3_string1list_check.append(each1)
				else:
					if each1.lower() == "nat":
						gen3_string1list.append("\033[93m"+str(each1)+"\033[00m")
						gen3_string1list_check.append(each1)
					else:
						gen3_string1list.append("\033[92m"+str(each1)+"\033[00m")
						gen3_string1list_check.append(each1)
						braces_dict[str(each1).lower()]+=1
			else:
				pass

		for each2 in check2:
			if each2 not in gen3_string2list_check:
				if each2 in check1:
					gen3_string2list.append(each2)
					gen3_string2list_check.append(each2)
				else:
					if each1.lower() == "nat":
						gen3_string2list.append("\033[93m"+str(each2)+"\033[00m")
						gen3_string2list_check.append(each2)
					else:
						gen3_string2list.append("\033[92m"+str(each2)+"\033[00m")
						gen3_string2list_check.append(each2)
						braces_dict[str(each1).lower()]+=1
			else:
				pass

		gen3_string1 = "|".join(gen3_string1list)
		gen3_string2 = "|".join(gen3_string2list)
	else:
		check1 = gen3[index//4].split("|")
		check1_clean = set(check1)

		gen3_string1 = "|".join(check1_clean)
		gen3_string2 = None

	return gen3_string1,gen3_string2,braces_dict

def gen4_func(gen4,index,braces_dict=None):
	if len(gen4)>1:
		check1 = gen4[index//8].split("|")
		check2 = gen4[(index//8)+1].split("|")

		gen4_string1list = []
		gen4_string2list = []

		gen4_string1list_check = []
		gen4_string2list_check = []

		for each1 in check1:
			if each1 not in gen4_string1list_check:
				if each1 in check2:
					gen4_string1list.append(each1)
					gen4_string1list_check.append(each1)
				else:
					if each1.lower() == "nat":
						gen4_string1list.append("\033[93m"+str(each1)+"\033[00m")
						gen4_string1list_check.append(each1)
					else:
						gen4_string1list.append("\033[92m"+str(each1)+"\033[00m")
						gen4_string1list_check.append(each1)
						braces_dict[str(each1).lower()]+=1
			else:
				pass

		for each2 in check2:
			if each2 not in gen4_string2list_check:
				if each2 in check1:
					gen4_string2list.append(each2)
					gen4_string2list_check.append(each2)
				else:
					if each1.lower() == "nat":
						gen4_string2list.append("\033[93m"+str(each2)+"\033[00m")
						gen4_string2list_check.append(each2)
					else:
						gen4_string2list.append("\033[92m"+str(each2)+"\033[00m")
						gen4_string2list_check.append(each2)
						braces_dict[str(each1).lower()]+=1
			else:
				pass

		gen4_string1 = "|".join(gen4_string1list)
		gen4_string2 = "|".join(gen4_string2list)
	else:
		check1 = gen4[index//8].split("|")
		check1_clean = set(check1)

		gen4_string1 = "|".join(check1_clean)
		gen4_string2 = None

	return gen4_string1,gen4_string2,braces_dict

def gen5_func(gen5,index,braces_dict=None):
	if len(gen5)>1:
		check1 = gen5[index//16].split("|")
		check2 = gen5[(index//16)+1].split("|")

		gen5_string1list = []
		gen5_string2list = []

		gen5_string1list_check = []
		gen5_string2list_check = []

		for each1 in check1:
			if each1 not in gen5_string1list_check:
				if each1 in check2:
					gen5_string1list.append(each1)
					gen5_string1list_check.append(each1)
				else:
					if each1.lower() == "nat":
						gen5_string1list.append("\033[93m"+str(each1)+"\033[00m")
						gen5_string1list_check.append(each1)
					else:
						gen5_string1list.append("\033[92m"+str(each1)+"\033[00m")
						gen5_string1list_check.append(each1)
						braces_dict[str(each1).lower()]+=1
			else:
				pass

		for each2 in check2:
			if each2 not in gen5_string2list_check:
				if each2 in check1:
					gen5_string2list.append(each2)
					gen5_string2list_check.append(each2)
				else:
					if each1.lower() == "nat":
						gen5_string2list.append("\033[93m"+str(each2)+"\033[00m")
						gen5_string2list_check.append(each2)
					else:
						gen2_string2list.append("\033[92m"+str(each2)+"\033[00m")
						gen2_string2list_check.append(each2)
						braces_dict[str(each1).lower()]+=1
			else:
				pass

		gen5_string1 = "|".join(gen5_string1list)
		gen5_string2 = "|".join(gen5_string2list)
	else:
		check1 = gen5[index//16].split("|")
		check1_clean = set(check1)

		gen5_string1 = "|".join(check1_clean)
		gen5_string2 = None

	return gen5_string1,gen5_string2,braces_dict

def gen6_func(gen6,index,braces_dict=None):
	check1 = gen6[index//32].split("|")
	check1_clean = set(check1)

	gen6_string1 = "|".join(check1_clean)
	gen6_string2 = None

	return gen6_string1,gen6_string2,braces_dict


if __name__=='__main__':
	main()