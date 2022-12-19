import codecs
from collections import defaultdict
import json
from pathlib import Path
from nltk.stem.snowball import _StandardStemmer


class Index:
	"""This is a python Index helper"""

	def __init__(
		self,
		stemmer: _StandardStemmer = None,
		stopwords=None,
		pickled_index_file=None
	):
		"""
		Args:
			stemmer : For example: nltk.stem.snowball.EnglishStemmer()
			stopwords : _description_. 
		"""
		if pickled_index_file:
			from pickle import load as __p_load
			with open(pickled_index_file, mode='rb') as iu:

				self.index = __p_load(iu).index
		else:
			self.stemmer = stemmer
			self.index = defaultdict(list)
			self.stopwords = set(stopwords) if stopwords else set()
		

	@staticmethod
	def get_words(document_path) -> list:
		from nltk import regexp_tokenize
		with codecs.open(document_path, mode='r',
							encoding='UTF-8') as document:
			return regexp_tokenize(document.read(), pattern=r'\w+')

	def build_index(
		self, file_points_to_docs: Path):
		with open(file_points_to_docs, mode='r') as collection_stream:
			documents = collection_stream.read().splitlines()
		for document_path in documents:
			words_list = [
				t.lower() for t in Index.
				get_words(file_points_to_docs.absolute().resolve().parent / document_path)
			]
			for word in words_list:
				word = self.stemmer.stem(word) if self.stemmer is not None else word
				if word in self.stopwords:
					continue
				if word in self.index.keys():
					self.index[word].append(document_path)
				else:
					self.index[word] = [
						document_path,
					]
		self.to_json("index.json")

	def lookup(self, word):
		"""
		Lookup a word in the index
		"""
		word = word.lower()
		if self.stemmer:
			word = self.stemmer.stem(word)

		return self.index.get(word)


	def to_pickle(self, pickle_filepath: str):
		with codecs.open(pickle_filepath, mode='wb') as pickle_filestream:
			from pickle import dump as __p_dump
			__p_dump(self, pickle_filestream)

	def to_json(self, json_filepath: str):
		with open(json_filepath, mode='w') as file_write_stream:
			json.dump(self.index, file_write_stream, indent=4, sort_keys=True)
