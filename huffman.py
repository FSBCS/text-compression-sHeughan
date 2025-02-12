from friendsbalt.acs import MinPQ


class HuffmanEncoding:
    def __init__(self, src=None, encoded_text=None, root=None):
        """
        Initializes a new Huffman Encoding. Either source text or encoded text and root must be provided.
        If source text is provided, it builds the Huffman tree and dictionary, and encodes the text.
        If encoded text and root are provided, it decodes the text.
        Args:
            src (str, optional): The source text to be encoded.
            encoded_text (str, optional): The encoded text to be decoded.
            root (Node, optional): The root node of the Huffman tree for decoding.
        """
        self.src = src
        self.root = root
        self.e_text = encoded_text

        frequency = {}

        for x in src:
            if x not in frequency:
                frequency[x] = 1
            
            else:
                frequency.update({x: frequency[x] + 1})

        print(frequency)

        items = []
        keys = []
        for x, y in frequency.items():
            items.append((x, y))
            keys.append(x)

        items.sort(key=lambda x: x[1], reverse = True)

        print(items)

        nodes = MinPQ()
        for x in items:
            nodes.insert(x[1], self.Node(x[1], x[0]))
        
        self.nodes = nodes

        self.build_tree(nodes)

    class Node:
        def __init__(self, freq, char=None, left=None, right=None):
            self.char = char
            self.freq = freq
            self.left = left
            self.right = right
        
        def is_leaf(self):
            return self.char is not None

    def encoding(self):
        """
        Returns the encoded text.
        Returns:
            str: The encoded text as a string of 0s and 1s.
        """
        if self.e_text != None: return self.e_text

        e_text = ""
        for x in self.src:
            e_text += self.dictionary[x] 

        self.e_text = e_text
        return self.e_text


    def source_text(self):
        return self.src

    def root(self):
        """
        Returns the root node of the Huffman tree.
        Returns:
            Node: The root node of the Huffman tree.
        """
        return self.root

    def build_tree(self, nodes):

        while nodes.size() > 1:
            node_a = self.nodes.del_min()
            node_b = self.nodes.del_min()
            new_frequency = node_a.freq + node_b.freq
            self.nodes.insert(new_frequency, self.Node(new_frequency, None, node_a, node_b))
            print("Done")
        
        self.nodes = nodes.del_min()
        self.dictionary = self._build_dictionary(self.nodes)
        print(self.dictionary)
    
    def _build_dictionary(self, node=None, prefix=''):
        """
        Recursively builds a dictionary that maps characters to their corresponding
        Huffman codes based on the Huffman tree.
        Args:
            node (Node, optional): The current node in the Huffman tree. Defaults to None,
                                   which means the function will start from the root node.
            prefix (str, optional): The current Huffman code prefix. Defaults to an empty string.
        Returns:
            dict: A dictionary where keys are characters and values are their corresponding
                  Huffman codes.
        """

        if node is None:
            node = self.root
        
        if node.char is not None:
            return {node.char: prefix}
        
        dictionary = {}
        dictionary.update(self._build_dictionary(node.left, prefix + '0'))
        dictionary.update(self._build_dictionary(node.right, prefix + '1'))
        return dictionary
    
Huff = HuffmanEncoding("Hello World")
print(Huff.encoding())
print(Huff.source_text())

