def WriteBitSequence(sequence, len_for_write=None):
    if len_for_write:
        sequence = sequence[:len_for_write]

    parts = [sequence[i:i + 8] for i in range(0, len(sequence), 8)]
    for i, part in enumerate(parts):
        if len(part) < 8:
            part = part[::-1]
            parts[i] = part.rjust(8, '0')
        else:
            parts[i] = part[::-1]
    return parts


def ReadBitSequence(sequence, len_for_read=None):
    sequence = sequence.replace(' ', '')
    sequence_list = [sequence[i:i + 8][::-1] for i in range(0, len(sequence), 8)]
    sequence = ''.join(sequence_list)

    if len_for_read:
        sequence = sequence[:len_for_read]

    parts = [sequence[i:i + 8] for i in range(0, len(sequence), 8)]
    for i, part in enumerate(parts):
        if len(part) < 8:
            part = part[::-1]
            parts[i] = part.rjust(8, '0')
        else:
            parts[i] = part[::-1]
    return parts


# input_file = input('Input file: ')
# output_file = input('Output file: ')
# write_file = open(output_file, 'w', encoding='UTF-8')

# with open(input_file, 'r', encoding='UTF-8') as read_file:
#     bit_sequence = read_file.read().replace(' ', '')

# print(bit_sequence)


first_array = '100001111'
second_array = '011101110'
total_array = first_array + '' + second_array

res = ' '.join(map(str, WriteBitSequence(total_array)))
# write_file.write(res)
print(res)

read = ' '.join(map(str, ReadBitSequence(res)))
print(read)
