from enum import StrEnum
from functools import reduce as __reduce
from os import listdir
from time import sleep

from pathlib import Path
from termcolor import cprint as __cprint

__newline = "\n"


class COLORS(StrEnum):
	GREY = "grey"
	RED = "red"
	GREEN = "green"
	YELLOW = "yellow"
	BLUE = "blue"
	MAGENTA = "magenta"
	CYAN = "cyan"
	WHITE = "white"


def show_text(
	text,
	color,
	pre_new_line: int = 0,
	post_new_line: int = 0,
	attrs=None,
	*kwargs
):
	"""Shows a simple text."""
	__cprint(
		f'{__newline*pre_new_line}{text}{__newline*post_new_line}',
		color,
		attrs,
		end=""
	)


def show_warning(
	text, pre_new_line: int = 0, post_new_line: int = 0, attrs=None, *kwargs
):
	"""Shows a warning text."""

	__cprint(
		f'{__newline*pre_new_line}Warning: {text}\n{__newline*post_new_line}',
		COLORS.YELLOW,
		attrs,
		kwargs
	)


def show_error(
	text, pre_new_line: int = 0, post_new_line: int = 0, attrs=None, *kwargs
):
	"""Shows an error text."""
	__cprint(
		f'{__newline*pre_new_line}Error: {text}\n{__newline*post_new_line}',
		COLORS.RED,
		attrs,
		kwargs
	)
	exit(0)


def show_info(
	text, pre_new_line: int = 0, post_new_line: int = 0, attrs=None, *kwargs
):
	"""Shows an info text."""
	color = "blue"
	__cprint(f'{(len(text)+6)*"-"}', color)
	__cprint(
		f'{__newline*pre_new_line}Info: {text}\n{__newline*post_new_line}',
		color,
		attrs,
		kwargs
	)
	__cprint(f'{(len(text)+6)*"-"}', color)
	sleep(0.5)


def show_success(
	text, pre_new_line: int = 0, post_new_line: int = 0, attrs=None, *kwargs
):
	"""Shows a success text."""
	color = "green"
	__cprint(
		f'{__newline*pre_new_line}Success: {text}\n{__newline*post_new_line}',
		color,
		attrs,
		kwargs
	)


def get_input_from_choices(prompt_text: str, prompt_color: str, choices: dict):
	"""Get the provided choice from the user in order to simplify choice picking."""
	# TODO return the input_choice only as a int wrapped digit
	if prompt_text:
		show_text(prompt_text + '\n', prompt_color)
	for value, _ in choices.items():
		if isinstance(_, dict):
			print(f'\t{value} --> {list(_.values())[0]}')
		else:
			print(f'\t{value} --> {_}')
	while True:
		result = input()
		if result in choices:
			if isinstance(choices[result], dict):
				show_success(
					f"{list(choices[result].values())[0]} is selected."
				)
			return result
		show_warning(
			f"Wrong choice! (Choices are {__reduce(lambda x, y: f'{x}, {y}', list(choices.keys()))})."
		)
def file_selection(filename:str) -> Path:
	show_text(
				f"Select your {filename} file:",
				COLORS.RED,
				0,
				1
			)
	target = None
	chosen_entry = Path()
	while True:
		entry_choices = {'0': '..'}
		for entry_index, entry in enumerate(
			listdir(chosen_entry), 1
			):
			entry_choices[str(entry_index)] = entry
		entry_choice = get_input_from_choices(
			"", COLORS.BLUE, entry_choices
		)
		chosen_entry /= entry_choices[entry_choice]
		if chosen_entry.is_dir():
			continue
		elif (not chosen_entry.name.endswith(filename)):
			show_warning(
				f"The file you selected is not {filename}! --Resetting--"
			)
			chosen_entry = Path()
		elif (chosen_entry.name.endswith(filename)):
			target = chosen_entry
			show_success(f"{filename} is successfully selected.", 1)
			return target