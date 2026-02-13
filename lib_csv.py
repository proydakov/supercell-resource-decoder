import os
import lzma

#
# decode_file
#
def decode_file(path):
    basename = os.path.splitext(path)[0]
    decodedname = basename + ".decoded.csv"

    print("process:", path, "->", decodedname)

    with open(path, 'rb') as f:
        data = f.read()

    tempdata = bytearray()

    for i in range(0, 8):
        tempdata.append(data[i])

    for i in range(0, 4):
        tempdata.append(0)

    for i in range(8, len(data)):
        tempdata.append(data[i])

    try:
        with open(decodedname, 'wb') as f:
            decompressor = lzma.LZMADecompressor()
            unpack_data = decompressor.decompress(tempdata)
            f.write(unpack_data)
    except:
        print("invalid input:", path)

#
# Len_2_bytes
#
def len_2_bytes(datalen, max_len=4):
    data = []
    while datalen > 0:
        item = datalen % 256
        datalen = int(datalen / 256)
        data.append(item)
    while len(data) < max_len:
        data.append(0)
    return data

#
# encode_file
#
def encode_file(path, max_len=4):
    basename = os.path.splitext(path)[0]
    encodedname = basename + ".encoded.csv"

    print("process:", path, "->", encodedname)

    with open(path, 'rb') as f:
        data = f.read()

    filters = [
        {
            "id": lzma.FILTER_LZMA1,
            "dict_size": 256 * 1024,
            "lc": 3,
            "lp": 0,
            "pb": 2,
            "mode": lzma.MODE_NORMAL
        },
    ]

    pack_data = lzma.compress(data, format=lzma.FORMAT_ALONE, filters=filters)

    lzmadata = bytearray()

    for i in range(0, 5):
        lzmadata.append(pack_data[i])

    data_size = len_2_bytes(len(data), max_len)
    for size in data_size:
        lzmadata.append(size)

    for i in range(13, len(pack_data)):
        lzmadata.append(pack_data[i])

    #for i in range(0, len(lzmadata)):
    #    print("i: ", i, " val: ", lzmadata[i])

    with open(encodedname, 'wb') as f:
        f.write(lzmadata)

#
# restore_file
#
def restore_file(path):
    with open(path, 'rb') as f:
        data = f.read()

    tempdata = bytearray()

    for i in range(0, 8):
        tempdata.append(data[i])

    for i in range(0, 4):
        tempdata.append(0)

    for i in range(8, len(data)):
        tempdata.append(data[i])

    with open('real.lzma', 'wb') as f:
        f.write(tempdata)
