# coding: utf-8

"""
A script to dump music from Pokemon Pinball (U) for use with pokecrystal.
"""

import os

from extras.pokemontools.audio import Sound
from song_names import song_labels

from extras.pokemontools.configuration import Config
conf = Config()

rom = bytearray(open('baserom.gbc').read())


def dump_pinball_music():
	"""
	Dump all songs and put them in music/.
	"""
	export_sounds(song_labels, os.path.join(conf.path, 'music'), 'Music_')


def dump_pinball_sfx():
	"""
	Maybe later.
	"""
	#export_sound_clump(sfx_labels, os.path.join(conf.path, 'sfx.asm'), 'Sfx_', sfx=True)
	pass


def read_address_pointer(address, bank=None):
	"""
	Read a little-endian address.
	"""
	if bank is None:
		bank = address / 0x4000
	parsed_address = rom[address] + rom[address + 1] * 0x100
	return parsed_address + bank * 0x4000 - 0x4000 * bool(bank)


def get_song_bank(song_id):
	"""
	Pokemon Pinball's sound engine only reads music from
	the same bank (a relic of the MBC1 days).

	Since there are too many songs and sound effects to fit
	in one bank, the sound engine is pasted in five times.

	Which bank a song is in and its index are determined by
	a lookup table in bank 3.
	"""
	song_pointers_address = 0xc77e
	address = song_pointers_address + song_id * 2
	song_index, bank = rom[address], rom[address + 1]
	return song_index, bank


def dump_sounds(names, base_label='Sound_'):
	"""
	Dump music data from each sound bank.

	Return a filename with its associated output.
	"""
	pointer_length = 2
	pointer_address = 0x4ca2
	# sfx: pointer_address = 0x63ce

	addresses = []
	for i, name in enumerate(names):
		song_index, bank = get_song_bank(i)
		address = read_address_pointer(
			(bank - 1) * 0x4000 +
			pointer_address +
			song_index * pointer_length
		)
		addresses += [address]

	# Do an extra pass to grab labels from each song.
	# There's no getting around this since the
	# Graveyard themes share labels.

	sounds = {}
	all_labels = []
	for name, address in zip(names, addresses):
		sound = Sound(address, base_label + name)
		sounds[name] = sound
		all_labels += sound.labels

	outputs = []
	for name, address in zip(names, addresses):
		sound = sounds[name]
		output = sound.to_asm(all_labels) + '\n'
		filename = name.lower() + '.asm'
		outputs += [(filename, output)]

	return outputs


def export_sounds(names, path, base_label='Sound_'):
	"""
	Write sound dumps to .asm files in a given directory.
	"""
	for filename, output in dump_sounds(names, base_label):
		with open(os.path.join(path, filename), 'w') as out:
			out.write(output)


if __name__ == "__main__":
	dump_pinball_music()

