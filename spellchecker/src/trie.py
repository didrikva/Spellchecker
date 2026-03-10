"""Main file for creating the trie"""
try:
    from src.node import Node
    from src.error import SearchMiss
except ImportError:
    from node import Node
    from error import SearchMiss


class Trie:
    """Class for trie """
    def __init__(self):
        """Main function"""
        self.root = Node()

    def add_word(self, word, frequency=1):
        """Function to add word to the trie"""
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                node.children[char] = Node(char)
            node = node.children[char]
        node.word = True
        node.frequency = float(frequency)

    def search(self, word):
        """Function to search a word in the trie"""
        node = self.root
        word = word.lower()
        for char in word:
            if char not in node.children:
                raise SearchMiss(f"Word '{word}' not found")
            node = node.children[char]
        if not node.word:
            raise SearchMiss(f"Word '{word}' not found")
        return True

    @classmethod
    def create_from_file(cls, filename="frequency.txt"):
        """Classmethod for creating a trie from a file"""
        new_trie = cls()
        new_trie.open_file(filename)
        return new_trie

    def open_file(self, filename):
        """Function to open a file and add words to the trie"""
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                word, freq = line.strip().split()
                frequency = float(freq)
                self.add_word(word, frequency)

    def remove(self, word):
        """Function to remove a word from the trie"""
        node = self.root
        word = word.lower()
        path = []
        for char in word:
            if char not in node.children:
                raise SearchMiss(f"Word '{word}' not found")
            path.append((node, char))
            node = node.children[char]
        if not node.word:
            raise SearchMiss(f"Word '{word}' not found")
        node.word = False

        reverse_path = path[::-1]
        for parent, char in reversed(reverse_path):
            child = parent.children[char]

            if not child.word:
                if not child.children:
                    parent.children.pop(char)
                    continue
            break


    def count(self):
        """Function to count the number of words in the trie"""
        total = 0
        items = [self.root]
        index = 0
        while index < len(items):
            node = items[index]
            index += 1
            if node.word:
                total += 1
            for child in node.children.values():
                items.append(child)
        return total

    def all_words(self):
        """Function that returns all words in the trie"""
        result = []
        items = [(self.root, "")]
        index = 0
        while index < len(items):
            node, prefix = items[index]
            index += 1
            if node.word:
                result.append(prefix)
            for child in node.children.values():
                items.append((child, prefix + child.key))

        return result

    def prefix_search(self, prefix):
        """Function to search for words with a given prefix"""
        node = self.root
        prefix = prefix.lower()
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        result = []
        items = [(node, prefix)]
        index = 0

        while index < len(items):
            current, current_prefix = items[index]
            index += 1

            if current.word:
                result.append((current_prefix, current.frequency))
            for child in current.children.values():
                items.append((child, current_prefix + child.key))
        for i, _ in enumerate(result):
            for j in range(i + 1, len(result)):
                if result[j][1] > result[i][1]:
                    result[i], result[j] = result[j], result[i]
        result = result[:10]
        return result


    def suffix_search(self, suffix):
        """Function to search for words with a given suffix"""
        result = []
        self._suffix(self.root, "", suffix, result)
        return sorted(result)


    def _suffix(self, node, current_word, suffix, result):
        """Function to search for words with a given suffix"""
        for child in node.children.values():
            self._suffix(child, current_word + child.key, suffix, result)

        suf_len = len(suffix)
        word_len = len(current_word)
        if current_word[word_len - suf_len:] == suffix:
            result.append(current_word)



if __name__ == "__main__":
    trie = Trie()
    trie.open_file("./spellchecker/tiny_frequency.txt")

    # print(trie.add_word("the"))
    # print(trie.add_word("be"))
    # print(trie.count())
    # print(trie.search("the"))
    # print(trie.all_words())
