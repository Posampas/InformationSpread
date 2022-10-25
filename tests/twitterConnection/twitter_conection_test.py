import unittest
from src.twitterConnection import Connection as con

class TwitterConncectionTest(unittest.TestCase):

    def test_should_create_Connection(self):
        twitterConection = con.Connection()
