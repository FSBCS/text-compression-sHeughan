import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from huffman import HuffmanEncoding
from huffmanFile import HuffmanFile

def test_file_compression():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'totc.txt')
    with open(file_path, 'r') as file:
        contents = file.read()
    
    encoding = HuffmanEncoding(contents)
    
    assert len(contents) * 8 > len(encoding.encoded_text)
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'test.huff')
    file = HuffmanFile(output_path, encoding)
    with file:
        file.write()
    
    file = HuffmanFile(output_path)
    with file:
        text = file.read()
    
    assert os.path.getsize(file_path) > os.path.getsize(output_path)

def test_decoding():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'test_data', 'totc.txt')
    with open(file_path, 'r') as file:
        contents = file.read()
    
    encoding = HuffmanEncoding(contents)
    
    assert len(contents) * 8 > len(encoding.encoded_text)
    
    output_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'test.huff')
    file = HuffmanFile(output_path, encoding)
    with file:
        file.write()
    
    file = HuffmanFile(output_path)
    with file:
        text = file.read()
    
    assert contents == text