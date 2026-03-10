#!/usr/bin/env python3
#pylint: disable=protected-access
""" Module for testing the class Die """

import unittest
import random
from src.trie import Trie
from src.error import SearchMiss

class TestTrie(unittest.TestCase):
    """ Submodule for unittests, derives from unittest.TestCase """
    def setUp(self):
        """ Setup that runs before every testcase """
        random.seed("Trie")
    def test_count(self):
        """ Test if count is correct """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("hi")
        trie.add_word("hey")
        trie.add_word("hola")
        trie.add_word("hallo")
        trie.add_word("hash")
        trie.add_word("happy")
        trie.add_word("house")
        self.assertEqual(trie.count(), 8, "Should be 8")
    def test_remove(self):
        """ Test if remove works """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("hi")
        trie.add_word("hey")
        trie.add_word("hola")
        trie.add_word("hallo")
        trie.add_word("hash")
        trie.add_word("happy")
        trie.add_word("house")
        trie.remove("hash")
        trie.remove("hi")
        self.assertEqual(trie.count(), 6, "Should be 6")
        with self.assertRaises(SearchMiss):
            trie.search("HASH")
        with self.assertRaises(SearchMiss):
            trie.search("hE")
    def test_all_words(self):
        """ Test if list of all words is correct """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("hi")
        trie.add_word("hey")
        trie.add_word("hola")
        trie.add_word("hallo")
        trie.add_word("hash")
        trie.add_word("happy")
        trie.add_word("house")
        self.assertCountEqual(trie.all_words(),
        ["hello", "hi", "hey", "hola", "hallo", "hash", "happy", "house"],
        "Should be equal")
    def test_prefix_search(self):
        """ Test if prefix search is correct """
        trie = Trie()
        trie.add_word("hello", 2)
        trie.add_word("hi", 5)
        trie.add_word("hey", 3)
        trie.add_word("hola", 4)
        trie.add_word("hallo", 1)
        trie.add_word("hash", 1)
        trie.add_word("happy", 8)
        trie.add_word("house", 5)
        before = trie.all_words()
        trie.remove("hAsh")
        trie.remove("hi")
        after = trie.all_words()

        self.assertNotEqual(before, after, "Lists should not be equal")
        self.assertEqual(trie.prefix_search("ha"),
        [("happy", 8), ("hallo", 1)],
        "Should be return list with hallo and happy in the right order")
        self.assertCountEqual(trie.prefix_search("h"),
        [("hallo", 1), ("hello", 2), ("house", 5),
        ("hey", 3), ("hola", 4), ("happy", 8)],
        "Should be equal list with all words starting with h")
        self.assertEqual(trie.prefix_search("hahaa"), [], "Should be empty list")
        self.assertEqual(trie.suffix_search("hello"), ["hello"], "Should be return list with hello")
    def test_suffix_search(self):
        """ Test if suffix search is correct """
        trie = Trie()
        trie.add_word("hello", 2)
        trie.add_word("hi", 5)
        trie.add_word("hey", 3)
        trie.add_word("hola", 4)
        trie.add_word("hallo", 1)
        trie.add_word("holo", 5)
        trie.add_word("pallo", 3)
        trie.add_word("hash", 1)
        trie.add_word("happy", 8)
        trie.add_word("house", 5)

        self.assertEqual(trie.suffix_search("lo"),
        ["hallo", "hello", "holo", "pallo"],
        "Should be return list with words ending with lo in the right order")
        self.assertEqual(trie.suffix_search("hahaa"), [], "Should be empty list")
        self.assertEqual(trie.suffix_search("hello"), ["hello"], "Should be return list with hello")
    def test_remove_searchmiss(self):
        """ Test if SearchMiss is raised when removing a non existsing word"""
        trie = Trie()
        trie.add_word("hello", 2)
        trie.add_word("hi", 5)
        trie.add_word("hey", 3)
        trie.add_word("hola", 4)
        trie.add_word("hallo", 1)
        trie.add_word("holo", 5)
        trie.add_word("pallo", 3)
        trie.add_word("hash", 1)
        trie.add_word("happy", 8)
        trie.add_word("house", 5)
        with self.assertRaises(SearchMiss):
            trie.remove("hejej")
    def test_empty_trie(self):
        """ Test if trie is empty """
        trie = Trie()
        self.assertEqual(trie.count(), 0)
        self.assertEqual(trie.all_words(), [])
        self.assertEqual(trie.prefix_search("a"), [])
        self.assertEqual(trie.suffix_search("a"), [])
