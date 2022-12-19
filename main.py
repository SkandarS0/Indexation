from os import listdir
from pathlib import Path

from nltk import download
from nltk.stem.snowball import ArabicStemmer, EnglishStemmer, FrenchStemmer

from core.index_parser import Index
from utils.helpers import (
	COLORS,
	file_selection,
	get_input_from_choices,
	show_info,
	show_success,
	show_text,
	show_warning
)

download('stopwords')

AVAILABLE_STEMMERS = {
	"0": {
		"__": "English", "func": EnglishStemmer(True)
	},
	"1": {
		"__": "French", "func": FrenchStemmer(True)
	},
	"2": {
		"__": "Arabic", "func": ArabicStemmer(True)
	},
}


def show_intro():
	title = "Welcome to my search engine project."
	show_text('-' * len(title), COLORS.BLUE, 2, 1)
	show_text(title, COLORS.YELLOW, 0, 1)
	show_text('-' * len(title), COLORS.BLUE, 0, 3)


def configure_index():
	show_text("Let's configure our index!", COLORS.GREEN, 0, 3)
	_with_stemmer = get_input_from_choices(
		"Do you want to stem your documents?\n",
		COLORS.BLUE, {
			"0": "No", "1": "Yes"
		}
	)
	with_stemmer = _with_stemmer == "1"
	stemmer_language = None
	if with_stemmer:
		_stemmer_language = get_input_from_choices(
			"In which language the documents you are trying to index ?\n",
			COLORS.BLUE,
			AVAILABLE_STEMMERS
		)
		stemmer_language = AVAILABLE_STEMMERS[_stemmer_language]['func']
	_with_stopwords = get_input_from_choices(
		"Do you want to exclude stop words from your index?\n",
		COLORS.BLUE, {
			"0": "No", "1": "Yes"
		}
	)
	with_stopwords = _with_stopwords == "1"
	stopwords = None
	if with_stopwords:
		antidict = file_selection("antidict.txt")
		with open(antidict, mode="r") as antidict_stream:
			stopwords = antidict_stream.read().splitlines()
	show_success("Index configured.")
	return Index(stemmer=stemmer_language, stopwords=stopwords)


def build_index(index: Index, collection_file: Path):
	show_info("Building index...", 1, 1)
	index.build_index(collection_file)
	show_success(
		"Index is built. Index is exported to JSON and pickled.", 1, 1
	)


def token_search(pickled_index_path):
	index = Index(pickled_index_file=pickled_index_path)
	show_text("Enter search keyword:", COLORS.RED, 1, 2)
	__keyword = input()
	if index.lookup(__keyword):
		for document_number, document in enumerate(index.lookup(__keyword), 1):
			if document_number % 2 == 0:
				show_text(f"\n\t\t{document_number}\t{document}\n", COLORS.YELLOW)
			else:
				show_text(f"\n\t\t{document_number}\t{document}\n", COLORS.BLUE)
	else:
		show_info("Sorry the keyword doesn't exist in the index.")

def main():
	show_intro()
	while True:
		choice = get_input_from_choices(
			"Start searching or select a pickled index ?",
			COLORS.BLUE,
			{
				"0": "Build a new index.",
				"1": "Select a pickled index.",
				"2": "Exit."
			}
		)
		if choice == "0":
			index = configure_index()
			collection_file = file_selection("collection.lst")
			build_index(index, collection_file)
		elif choice == "1":
			pickled_index_path = file_selection("index.pckl")
			while True:
				choice = get_input_from_choices("", COLORS.WHITE, {
					"0": "Return to main menu.",
					"1": "Search"
				})
				if choice == "0":
					show_text("Goodbye.", COLORS.GREEN)
					exit(0)
				else:
					token_search(pickled_index_path)
		elif choice == "2":
			break


if __name__ == '__main__':
	main()