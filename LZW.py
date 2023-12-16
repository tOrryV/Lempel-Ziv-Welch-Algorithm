import os
import pickle
import zipfile

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

def compress_and_write_file(file_path, compressed_data):
    with open(file_path, 'wb') as file:
        pickle.dump(compressed_data, file)

def read_and_decompress_file(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def lzw_compress(data):
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256
    result = []
    current_code = data[0]

    for symbol in data[1:]:
        if current_code + symbol in dictionary:
            current_code += symbol
        else:
            result.append(dictionary[current_code])
            dictionary[current_code + symbol] = next_code
            next_code += 1
            current_code = symbol

    result.append(dictionary[current_code])

    return result

def lzw_decompress(compressed_data):
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    result = [chr(compressed_data[0])]
    current_code = compressed_data[0]

    for code in compressed_data[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = current_code + current_code[0]
        else:
            raise ValueError("Invalid compressed data")

        result.append(entry)

        dictionary[next_code] = str(current_code) + entry[0]
        next_code += 1
        current_code = entry

    return ''.join(result)

# User input for encoding or decoding
choice = input("Enter 'encode' for encoding or 'decode' for decoding: ")

if choice.lower() == 'encode':
    # Encoding
    input_file_path = 'input2.txt'
    compressed_archive_path = 'compressed_output.zip'

    original_data = read_file(input_file_path)
    compressed_data = lzw_compress(original_data)

    with zipfile.ZipFile(compressed_archive_path, 'w') as compressed_archive:
        compressed_data_bytes = pickle.dumps(compressed_data)
        compressed_archive.writestr('compressed_data.pkl', compressed_data_bytes)

    print("File encoded and compressed successfully.")

elif choice.lower() == 'decode':
    # Decoding
    compressed_archive_path = 'compressed_output.zip'
    decompressed_file_path = 'decompressed_output.txt'

    with zipfile.ZipFile(compressed_archive_path, 'r') as compressed_archive:
        compressed_data_bytes = compressed_archive.read('compressed_data.pkl')
        compressed_data = pickle.loads(compressed_data_bytes)

    decompressed_data = lzw_decompress(compressed_data)
    write_file(decompressed_file_path, decompressed_data)

    print("File decompressed and decoded successfully.")

else:
    print("Invalid choice. Please enter 'encode' or 'decode'.")




# Оригінальний файл
original_file_path = 'input2.txt'
original_size = os.path.getsize(original_file_path)
print(f"Розмір оригінального файлу: {original_size} байт")

# Стиснений файл
compressed_file_path = 'compressed_output.zip'
compressed_size = os.path.getsize(compressed_file_path)
print(f"Розмір стисненого файлу: {compressed_size} байт")

# Розрахунок відносної зменшення розміру
compression_ratio = (original_size - compressed_size) / original_size * 100
print(f"Відносне зменшення розміру: {compression_ratio:.2f}%")
