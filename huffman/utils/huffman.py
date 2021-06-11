"""
Using Graph and Binary Heap to implement Huffman Encoding
Binary Tree is in the form of
e.g.
{
    'a': {
        'value': 3,
        'left': b,
        'right': c,
        }
    'b': {
        'value': 4,
        'left': e,
        'right': f,
        }
}
"""
import copy


class BinaryMinHeap:
    """
    easy binary heap for nodes with values
    """

    def __init__(self, graph):
        self.size = 0
        self.heap = []
        self.graph = {}
        self.build_heap(graph)

    def extract_min(self):
        self.size -= 1
        result = self.heap.pop(0)
        if not self.is_empty():
            last = self.heap.pop(-1)
            self.heap.insert(0, last)
            self._sift_down(0)
        return result

    def insert(self, key, value):
        """
        Insert key value pair to graph and insert to heap
        """
        self.size += 1
        self.graph[key] = {
            'value': value
        }
        self.heap.append(key)
        self._bubble_up(self.size - 1)

    def is_empty(self):
        return True if self.size == 0 else False

    def build_heap(self, graph):
        """
        O(n)
        """
        self.size = 0
        self.graph = copy.deepcopy(graph)
        for key in graph.keys():
            self.heap.append(key)
            self.size += 1
        if not self.is_empty():
            for i in range(int((len(self.heap) - 1) / 2), -1, -1):
                self._sift_down(i)

    def _bubble_up(self, index):
        if index > 0:
            parent_index = int((index - 1) / 2)
            if self.graph[self.heap[index]].get('value') < self.graph[self.heap[parent_index]].get('value'):
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                self._bubble_up(parent_index)

    def _sift_down(self, index):
        if index < int(self.size / 2):
            child_1_index = (index + 1) * 2 - 1
            child_2_index = (index + 1) * 2
            try:
                if self.graph[self.heap[index]].get('value') > self.graph[self.heap[child_1_index]].get('value') or \
                        self.graph[self.heap[index]].get('value') > self.graph[self.heap[child_2_index]].get('value'):
                    if self.graph[self.heap[child_1_index]].get('value') > \
                            self.graph[self.heap[child_2_index]].get('value'):
                        self.heap[index], self.heap[child_2_index] = self.heap[child_2_index], self.heap[index]
                        self._sift_down(child_2_index)
                    else:
                        self.heap[index], self.heap[child_1_index] = self.heap[child_1_index], self.heap[index]
                        self._sift_down(child_1_index)
            except IndexError:
                if self.graph[self.heap[index]].get('value') > self.graph[self.heap[child_1_index]].get('value'):
                    self.heap[index], self.heap[child_1_index] = self.heap[child_1_index], self.heap[index]
                    self._sift_down(child_1_index)


def huffman_encoding(input_string):
    """
    Huffman Encoding to generated encoded string
    @param input_string: targeted string
    @return: <string> encoded string
             <dict> frequency dictionary
    """
    freq_dict = _get_freq(input_string)
    binary_tree = copy.deepcopy(freq_dict)
    result_string = ''

    if len(binary_tree) == 1:
        for char in input_string:
            result_string += '0'
        return result_string

    binary_tree, root = _construct_huffman_tree(binary_tree)

    for char in input_string:
        result_string += binary_tree_dfs(binary_tree, char, root, '')

    return _bit_string_to_byte_string(result_string), freq_dict


def huffman_decoding(input_string, freq_dict):
    """
    Decoder of Huffman encoded string.
    @param input_string: Huffman encoded string
    @param freq_dict: dictionary of char to frequency
    @return: <str> decoded string
    """
    binary_tree, root = _construct_huffman_tree(freq_dict)
    result_string = ''
    i = 0
    input_string = _byte_string_to_bit_string(input_string)
    while i < len(input_string):
        node = root
        while binary_tree[node].get('left') or binary_tree[node].get('right'):
            node = binary_tree[node]['left'] if input_string[i] == '0' else binary_tree[node]['right']
            i += 1
        result_string += str(node)
    return result_string


def _construct_huffman_tree(binary_tree):
    """
    Constructs a huffman tree by a frequency table
    @return: <dict> huffman tree, <int> or <string> root node
    """
    binary_heap = BinaryMinHeap(binary_tree)
    i = 0
    while not len(binary_heap.heap) < 2:
        # setting i as key
        i += 1
        # extract first two min nodes
        left_node_key = binary_heap.extract_min()
        right_node_key = binary_heap.extract_min()
        # make a new node with two nodes above as children
        binary_tree[i] = {}
        binary_tree[i]['left'] = left_node_key
        binary_tree[i]['right'] = right_node_key
        binary_tree[i]['value'] = binary_tree[left_node_key].get('value') + binary_tree[right_node_key].get('value')
        # add new node to binary heap
        binary_heap.insert(i, binary_tree[i]['value'])

    return binary_tree, i


def binary_tree_dfs(tree, char, tree_node_key, search_string):
    """
    Assuming binary tree to be complete
    @param tree: tree to search
    @param char: char to search
    @param tree_node_key: binary tree node
    @param search_string: current search string, e.g. '010'
    @return: a string of e.g. '0101101' as 0 being left and 1 being right
    """
    if not tree[tree_node_key].get('left') and not tree[tree_node_key].get('right'):
        return search_string if char == tree_node_key else None
    left_node_key = tree[tree_node_key].get('left')
    left_string = binary_tree_dfs(tree, char, left_node_key, search_string + '0')
    right_node_key = tree[tree_node_key].get('right')
    right_string = binary_tree_dfs(tree, char, right_node_key, search_string + '1')

    return left_string if not right_string else right_string


def _get_freq(input_string):
    """
    @param input_string: string of different chars
    @return: a dict list {'char':
                                'value': freq
                         }
    """
    result_dict = {}
    for char in input_string:
        if not result_dict.get(char):
            result_dict[char] = {'value': 1}
        else:
            result_dict[char]['value'] += 1
    return result_dict


def _bit_string_to_byte_string(input_string):
    """
    Converts 0's and 1's to an ascii byte-string
    @param input_string: any type of string which consists of only 0's and 1's
    @return: <str> ascii byte-string
    """
    result_string = ''
    for i in range(0, len(input_string), 8):
        current_len = 8 if i + 8 < len(input_string) else len(input_string) - i
        current_byte = input_string[i: i + current_len]
        # convert to int first
        byte_int = int(current_byte, 2)
        # convert the int to a ascii chr
        byte_chr = chr(byte_int)
        result_string += byte_chr

    return result_string.encode('UTF-8')


def _byte_string_to_bit_string(byte_string):
    """
    Converts byte_string (b_string) to a string of 0's and 1's
    @param byte_string: <b_string> byte-string
    @return: <str> bit-string but just a a string of 0's and 1's
    """
    result_string = ''
    byte_string = byte_string.decode('UTF-8')
    for ch in byte_string:
        binary = bin(ord(ch))[2:]
        # convert binary into 8-digit binary
        if len(bin(ord(ch))[2:]) <= 8:
            binary = '0' * (8 - len(binary)) + binary
        result_string += binary
    # for last 8 characters, convert 8-digit binary to original binary, b/c of the design of encoding
    i = len(result_string) - 8
    while i < len(result_string):
        if result_string[i] == '0':
            result_string = result_string[:i] + result_string[i + 1:]
        else:
            break
    return result_string


def write_binary_to_file(byte_string, file_name):
    with open(file_name, 'wb') as f:
        f.write(byte_string)


def read_binary_file(file_name):
    result_string = b''
    with open(file_name, "rb") as f:
        byte = f.read(1)
        result_string += byte
        while byte:
            byte = f.read(1)
            result_string += byte
    return result_string
