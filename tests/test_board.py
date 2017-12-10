#!/usr/bin/env python
# encoding: utf-8
import unittest
from qwirkle.game import Board

class TestBoard(unittest.TestCase):
    def test_init(self):
        board = Board()

if __name__ == '__main__':
    unittest.main()

