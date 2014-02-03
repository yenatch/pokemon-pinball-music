
song_names = {
	 0: "Nothing",
	 1: "Blue Field",
	 2: "Catch 'Em! Red",
	 3: "Hurry Up! Red",
	 4: "Pokedex",
	 5: "Gastly in the Graveyard",
	 6: "Haunter in the Graveyard",
	 7: "Gengar in the Graveyard",
	 8: "Red Field",
	 9: "Catch 'Em! Blue",
	10: "Hurry Up! Blue",
	11: "Hi-Score",
	12: "Game Over",
	13: "Whack the Digletts!",
	14: "Whack the Dugtrio!",
	15: "Seel Stage",
	16: "Title",
	17: "Mewtwo Stage",
	18: "Options",
	19: "Field Select",
	20: "Mewoth Stage",
	21: "End Credits",
	22: "Name Entry",
}

def trim(name):
	removes = ["!", "'", "-", " "]
	name = name.title()
	for remove in removes:
		name = name.replace(remove, "")
	return name

song_labels = [trim(name) for name in song_names.values()]

