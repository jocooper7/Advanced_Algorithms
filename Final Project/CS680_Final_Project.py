# CS680 Advanced Algorithms
# Huffman Coding Compression Project
# Author: Jo Cooper

# imports
import csv
from hashlib import sha256
import os
import time

# Huffman Tree
class HuffInternal:
    def __init__(self, freq):
        self.freq = freq
        self.left = None
        self.right = None
 
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

class HuffLeaf:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
 
    def is_leaf(self) -> bool:
        return True


# scan input file for frequencies
def scan_freq(filename) -> dict:
    try:
        # newline = "" so characters are counted exactly as the encoder reads them
        with open(filename, newline = "") as f:
            freqs = {}
            for line in f:
                for char in line:
                    freqs[char] = freqs.get(char, 0) + 1
            return freqs
    except:
        return {}


# builds the header bytes from the code dictionary
def build_header(codes) -> bytes:
    header = bytearray(len(codes).to_bytes(4, "big"))
    for char, code in codes.items():
        char_bytes = char.encode("utf-8")
        code_len = len(code)
        n_bytes = (code_len + 7) // 8
        packed = int(code + "0" * (n_bytes * 8 - code_len), 2).to_bytes(n_bytes, "big")
 
        header.append(len(char_bytes))
        header.extend(char_bytes)
        header.append(code_len)
        header.extend(packed)
    return bytes(header)

# parses the header from raw file bytes
# returns reverse dictionary {code string: character} and the offset where the encoded data begins
def parse_header(raw, offset) -> tuple[dict, int]:
    count = int.from_bytes(raw[offset:offset + 4], "big")
    offset += 4

    decode_dict = {}
    for _ in range(count):
        char_len = raw[offset]
        offset += 1
        char = raw[offset:offset + char_len].decode("utf-8")
        offset += char_len
 
        code_len = raw[offset]
        offset += 1
        n_bytes = (code_len + 7) // 8
        packed = raw[offset:offset + n_bytes]
        offset += n_bytes

        code = bin(int.from_bytes(packed, "big"))[2:].zfill(n_bytes * 8)[:code_len]
        decode_dict[code] = char
    return decode_dict, offset

# encodes file with Huffman codes
def encode_file(input_path, output_path, codes) -> None:
    lookup = codes.__getitem__

    try:
        with open(input_path, "r", newline = "") as f_in, open(output_path, "wb") as f_out:
            f_out.write(b"\x00") # placeholder for the padding count
            f_out.write(build_header(codes)) # code dictionary
            leftover = "" # bits that didn't fill a whole byte
            mem_limit = 500000

            while True:
                data = f_in.read(mem_limit)
                if not data:
                    break

                bits = leftover + "".join(map(lookup, data)) # returns string of binaries mapped by dictionary
                usable = len(bits) - (len(bits) % 8) # ensures length of data to full bytes

                if usable:
                    f_out.write(int(bits[:usable], 2).to_bytes(usable // 8, "big"))
                leftover = bits[usable:]

            # final partial byte
            padding = 0
            if leftover:
                padding = 8 - len(leftover)
                f_out.write(int(leftover + "0" * padding, 2).to_bytes(1, "big")) # pad last byte

            f_out.seek(0) # takes pointer to start of file
            f_out.write(bytes([padding])) # writes padding count
    except:
        print("Error encoding file")

# Decodes Huffman encoded file using only the dictionary stored in the file header
def decode_file(input_path, output_path) -> None:

    try:
        with open(input_path, "rb") as f:
            raw = f.read()

        padding = raw[0] # padding count from first byte
        decode_dict, offset = parse_header(raw, 1)
        data = raw[offset:]

        total_bits = len(data) * 8 - padding # drops padding bits
        bits = bin(int.from_bytes(data, "big"))[2:].zfill(len(data) * 8)[:total_bits]

        # Huffman codes are prefix-free, so the first dictionary match is always correct
        out = []
        code = ""
        for bit in bits:
            code += bit
            char = decode_dict.get(code)
            if char is not None:
                out.append(char)
                code = ""

        with open(output_path, "w", newline = "") as f:
            f.write("".join(out))

    except:
        print("Error decoding file")


## basic functions

# insertion sort used during tree build with max n of roughly 55 depending on characters in data
# most calls will be on nearly sorted lists so O(n) is expected
def insert_sort(list) -> None:
    for i in range(1, len(list)):
        key = list[i]
        j = i - 1
        while j >= 0 and key[0] < list[j][0]: # [frequency, character]
            list[j + 1] = list[j]
            j -= 1
        list[j + 1] = key

# builds Huffman tree from node list by analyzing sorted frequencies
def build_tree(node_list) -> None:
    insert_sort(node_list)
    while len(node_list) > 1:
        x = node_list.pop(0)
        y = node_list.pop(0)
        new_node = HuffInternal(x[0] + y[0])
        new_node.left = x[1]
        new_node.right = y[1]
        node_list.append([new_node.freq, new_node])
        insert_sort(node_list)

# builds Huffman code dict from tree
# a file with a single unique character gives a lone leaf, which still needs a 1 bit code
def build_dict(node, code="") -> None:
    if node.is_leaf():
        huff_dict[node.char] = code or "0"
    else:
        build_dict(node.left, code + "0")
        build_dict(node.right, code + "1")


## testing functions

# validate memory usage across file versions
def memory_check() -> None:
        orig_size = os.path.getsize(file)
        deco_size = os.path.getsize(decod)
        comp_size = os.path.getsize(comp)

        print(f"\nOriginal file size: {orig_size} bytes")
        print(f"Decoded size: {deco_size} bytes")        

        valid = os.path.getsize(decod) == os.path.getsize(file)
        if valid:
            print("Original and Decoded file sizes match.")
        else:
            print("Original and Decoded file sizes differ.")

        print(f"\nCompressed size: {comp_size} bytes (includes header)")
        print(f"Compression Ratio: {comp_size/orig_size:.5f}")

# imports SHA256 validation codes from CSV for verification
def imp_valids(filename) -> set:
    try:
        with open(filename) as f:
            reader = csv.reader(f, delimiter='|')
            valids = set()
            for row in reader:
                valids.add(row[-1])
            return valids
    except:
        return set()

# validates lines against original and decoded hashes
def cross_validate(file, sha_set) -> tuple[bool, int]:
    inv = 0
    valid = True
    inv_list = []

    try:
        with open(file, newline = '') as f:
            reader = csv.reader(f, delimiter='|')
            header = next(reader)
            for line in reader:
                # validating against original hash and encoded hash
                stored_sha = line[-1].strip()
                data = line[:-1]
                computed = sha256("|".join(data).encode()).hexdigest()

                # new hash must match the stored hash, and the old hash must be known
                if computed != stored_sha or computed not in sha_set:
                    inv += 1
                    valid = False
                    inv_list.append(line)

    except csv.Error as e:
        print(e)
        valid = False
    return valid, inv, inv_list


# main execution
if __name__ == "__main__":
    file = "CS_680_Project_Data_Set-3.csv" # change # in "Set-#" to validate program with different file
    comp = "compressed_file.bin"
    decod = "decoded_file.csv"
    invalid_file = "invalid.csv"

    test = False # set flag to True to run tests

    print("\nScanning character frequencies in file...")
    start = time.perf_counter()
    freq_dict = scan_freq(file)
    end = time.perf_counter()
    if test:
        print(f"Scan time: {end-start:.5f} seconds")

    print("\nBuilding Huffman tree...")
    start = time.perf_counter()
    node_list = []
    for char, freq in freq_dict.items():
        node_list.append([freq, HuffLeaf(char, freq)])
    build_tree(node_list)
    huff_tree = node_list[0][1]

    huff_dict = {}
    build_dict(huff_tree)
    end = time.perf_counter()
    if test:
        print(f"Tree build time: {end-start:.5f} seconds")

    print("\nEncoding file...")
    start = time.perf_counter()
    encode_file(file, comp, huff_dict)
    end = time.perf_counter()
    if test:
        print(f"Encode time: {end-start:.5f} seconds")

    print("\nDecoding file...")
    start = time.perf_counter()
    # decoder rebuilds everything from the file header, no tree is passed in
    decode_file(comp, decod)
    end = time.perf_counter()
    if test:
        print(f"Decode time: {end-start:.5f} seconds")

    if test:
        print('\n"test" variable set to True.\nRunning tests...')
        # compare memory of original, compressed, and decoded files
        memory_check()

        # get valid hashes for verification
        valids = imp_valids(file)
        val, inv, inv_list = cross_validate(decod, valids)
        if val:
            print("\nAll lines validated")
        else:
            print(f"\nNumber of Invalid lines: {inv}")
            for line in inv_list:
                print(line)

        # validation run against modified file to verify functionality 
        # invalid verification check functions as intended with specified file
        if file == "CS_680_Project_Data_Set-3.csv":
            val, inv, inv_list = cross_validate(invalid_file, valids)
            if val:
                print("\nAll lines validated")
            else:
                print(f"\nNumber of Invalid lines: {inv}")
                for line in inv_list:
                    print(line)
