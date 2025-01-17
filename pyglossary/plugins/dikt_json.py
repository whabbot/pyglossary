# -*- coding: utf-8 -*-
# from https://github.com/maxim-saplin/pyglossary

import re
import typing
from typing import Generator

from pyglossary.compression import (
	# compressionOpen,
	stdCompressions,
)
from pyglossary.glossary_types import EntryType, GlossaryType
from pyglossary.option import (
	BoolOption,
	EncodingOption,
	Option,
)

enable = True
lname = "dikt_json"
format = "DiktJson"
description = "DIKT JSON (.json)"
extensions = ()
extensionCreate = ".json"
singleFile = True
kind = "text"
wiki = ""
website = "https://github.com/maxim-saplin/dikt"
optionsProp: "dict[str, Option]" = {
	"encoding": EncodingOption(),
	"enable_info": BoolOption(comment="Enable glossary info / metedata"),
	"resources": BoolOption(comment="Enable resources / data files"),
	"word_title": BoolOption(
		comment="add headwords title to beginning of definition",
	),
}


class Writer(object):
	_encoding: str = "utf-8"
	_enable_info: bool = True
	_resources: bool = True
	_word_title: bool = False

	compressions = stdCompressions

	def __init__(self: "typing.Self", glos: GlossaryType) -> None:
		self._glos = glos
		self._filename = None
		glos.preventDuplicateWords()

	def open(self: "typing.Self", filename: str) -> None:
		self._filename = filename

	def finish(self: "typing.Self") -> None:
		self._filename = None

	def write(self: "typing.Self") -> "Generator[None, EntryType, None]":
		from json import dumps

		from pyglossary.text_writer import writeTxt

		glos = self._glos
		encoding = self._encoding
		enable_info = self._enable_info
		resources = self._resources

		ascii = encoding == "ascii"

		def escape(st: str) -> str:
			# remove styling from HTML tags
			st2 = re.sub(r' style="[^"]*"', '', st)
			st2 = re.sub(r' class="[^"]*"', '', st2)
			st2 = re.sub(r'<font [^>]*>', '', st2)
			st2 = re.sub(r'</font>', '', st2)
			st2 = re.sub(r'\n', '', st2)
			st2 = re.sub(r'<div></div>', '', st2)
			st2 = re.sub(r'<span></span>', '', st2)
			# fix russian dictionary issues,
			# such as hyphenation in word (e.g. абб{[']}а{[/']}т)
			st2 = re.sub(r"\{\['\]\}", "", st2)
			st2 = re.sub(r"\{\[/'\]\}", "", st2)
			return dumps(st2, ensure_ascii=ascii)

		yield from writeTxt(
			glos,
			entryFmt="\t{word}: {defi},\n",
			filename=self._filename,
			encoding=encoding,
			writeInfo=enable_info,
			wordEscapeFunc=escape,
			defiEscapeFunc=escape,
			ext=".json",
			head="{\n",
			tail='\t"": ""\n}',
			resources=resources,
			word_title=self._word_title,
		)
