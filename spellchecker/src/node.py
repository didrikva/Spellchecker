""" File for the node class """
class Node():
    """Class for node"""
    def __init__(self, key=None):
        """Main function"""
        self.key = key
        self.children = {}
        self.word = False
        self.frequency = 0
