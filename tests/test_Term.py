#!/usr/bin/env python
from unittest import TestCase
from evHID.Types.term.terminal import Term


class Test(TestCase):
	def test_Term(__s):
		term=Term()
		print(term.color.fg.RGB)
		print(term.color.bg.G)


	def test_size(__S):
		term = Term()
		print(term.size.rc)

	
