# explanations for member functions are provided in requirements.py
# each file that uses a skip list should import it from this file.

from typing import List

class Trie:
     
    # Trie data structure class
    def __init__(self, is_compressed: bool):
        self.is_compressed = is_compressed
        self.root = TrieNode("/")
        pass


    def _insert_uncompressed(self, key):
        temp = self.root
        for c in key:
            if c not in temp.children:
                temp.children[c] = TrieNode(c)

            temp = temp.children[c]

        temp.is_end_of_word = True
    

    def _find_longest_common_prefix(self, child_value, key_prefix):
        lcp = ""
        lcp_length = 0

        for i in range(min(len(child_value), len(key_prefix))):
            if child_value[i] == key_prefix[i]:
                lcp += child_value[i]
                lcp_length += 1
            else:
                break

        return lcp, lcp_length


    def _split_child(self, node, child, lcp, lcp_length):
        # split word, "test" will split to "te" and "st"
        split1 = lcp
        split2 = child.value[lcp_length:]

        # print(split1 + " " + split2)

        # this could be "te"
        node.children[split1] = TrieNode(split1)
        # this could be "st"
        node.children[split1].children[split2] = TrieNode(split2)
        node.children[split1].children[split2].is_end_of_word = True

        for child_node in child.children.values():
            node.children[split1].children[split2].children[child_node.value] = child_node

        del node.children[child.value]
        
        return node.children[split1]


    def _insert_compressed(self, key):
        node = self.root
        # print("insert key: " + key)
        index = 0

        while index < len(key):
            # Find the longest common prefix between the key segment and the children of the current node
            match = False
            # print(node.children)
            for child in node.children.values():
                lcp, lcp_length = self._find_longest_common_prefix(child.value, key[index:])
                if lcp_length > 0:  # If there's a match
                    match = True
                    if lcp_length < len(child.value):
                        # Need to split the child node
                        child = self._split_child(node, child, lcp, lcp_length)
                        # print("child: " + child.value)
                    index += lcp_length
                    node = child
                    break
            if not match:
                # No matching child, create a new one with the remaining key segment
                new_node = TrieNode(key[index:])
                node.children[key[index:]] = new_node
                node = new_node
                break
        node.is_end_of_word = True


    def construct_trie_from_text(self, keys: List[str]) -> None:
        for key in keys:
            if not self.is_compressed:    
                self._insert_uncompressed(key)
            else:
                self._insert_compressed(key)


    def _generate_suffixes(self, word):
        suffixes = []
        for i in range(len(word)):
            suffixes.append(word[i:])
        return suffixes


    def construct_suffix_tree_from_text(self, keys: List[str]) -> None:
        suffixes = []

        for key in keys:
            for suffix in self._generate_suffixes(key):
                suffixes.append(suffix)

        for suffix in suffixes:
            if not self.is_compressed:    
                self._insert_uncompressed(suffix)
            else:
                self._insert_compressed(suffix)

        return self
    
    def search_and_get_depth(self, key: str) -> int:
        print("searching for key: " + key)
        if not self.is_compressed:
            temp = self.root
            depth = 0

            for c in key:
                if c not in temp.children:
                    return -1

                depth += 1
                temp = temp.children[c]

            return depth if temp.is_end_of_word else -1
        else:
            temp = self.root
            depth = 0
            i = 0
            while i < len(key):
                # print(temp.children)
                found = False
                for child in temp.children.values():
                    if key.startswith(child.value, i):
                        depth += 1
                        # print("node value: " + child.value + ", end of word: " + str(child.is_end_of_word))
                        i += len(child.value)
                        temp = child
                        found = True
                        break
                if not found:
                    return -1
            return depth if temp.is_end_of_word else -1


# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define

class TrieNode:

    # Initialise
    def __init__(self, value):
        self.value = value
        self.children = {}
        self.is_end_of_word = False
