from huffman import HuffmanEncoding

class HuffmanFile:
    '''
    A class for reading and writing Huffman encoded files.
    This class provides a bridge between the Huffman Encoding
    abstraction and the bits written to a binary file.
    '''
    def __init__(self, file_path, encoding=None):
        self.encoding = encoding
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, 'wb' if self.encoding else 'rb')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
    
    def _serialize_tree(self, node):
        """Serialize Huffman tree to string of bits"""
        if node.is_leaf():
            # Leaf node: 0 + 8-bit character
            return '0' + format(ord(node.char), '08b')
        # Internal node: 1 + left + right
        return '1' + self._serialize_tree(node.left) + self._serialize_tree(node.right)
    
    def write(self):
        """Write Huffman tree and encoded data to binary file"""
        if not self.encoding:
            raise ValueError("Encoding must be provided for writing")
        
        # Serialize tree
        tree_bits = self._serialize_tree(self.encoding.root())
        
        # Write tree size and tree
        self.file.write(len(tree_bits).to_bytes(4, byteorder='big'))
        tree_int = int(tree_bits, 2)
        tree_bytes = (len(tree_bits) + 7) // 8
        self.file.write(tree_int.to_bytes(tree_bytes, byteorder='big'))
        
        # Write encoded data
        encoded_text = self.encoding.encoding()
        self.file.write(len(encoded_text).to_bytes(4, byteorder='big'))
        data_int = int(encoded_text, 2)
        data_bytes = (len(encoded_text) + 7) // 8
        self.file.write(data_int.to_bytes(data_bytes, byteorder='big'))
    
    def _deserialize_tree(self, bits, pos=0):
        """Reconstruct Huffman tree from bits"""
        if bits[pos] == '0':
            char = chr(int(bits[pos+1:pos+9], 2))
            return HuffmanEncoding.Node(1, char=char), pos + 9
        left, new_pos = self._deserialize_tree(bits, pos=pos + 1)
        right, final_pos = self._deserialize_tree(bits, pos=new_pos)
        return HuffmanEncoding.Node(1, left=left, right=right), final_pos
    
    def read(self):
        """Read Huffman tree and encoded data from binary file"""
        if self.encoding:
            raise ValueError("Encoding should not be provided for reading")
        
        # Read and reconstruct tree
        tree_size = int.from_bytes(self.file.read(4), byteorder='big')
        tree_bytes = (tree_size + 7) // 8
        tree_int = int.from_bytes(self.file.read(tree_bytes), byteorder='big')
        tree_bits = bin(tree_int)[2:].zfill(tree_size)
        root, _ = self._deserialize_tree(tree_bits)
        
        # Read encoded data
        data_size = int.from_bytes(self.file.read(4), byteorder='big')
        data_bytes = (data_size + 7) // 8
        data_int = int.from_bytes(self.file.read(data_bytes), byteorder='big')
        encoded_text = bin(data_int)[2:].zfill(data_size)
        
        self.encoding = HuffmanEncoding(encoded_text=encoded_text, root=root)
        return self.encoding.source_text()
