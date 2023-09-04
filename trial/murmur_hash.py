def murmur_hash(input_string, seed, desired_length=32):
    m = 0x5bd1e995
    r = 24
    length = len(input_string)

    # Pad the input bytes with null bytes if it's shorter than the desired length
    if length < desired_length:
        input_string += b'\x00' * (desired_length - length)

    seed = int(seed)  # Convert seed to an integer

    h = seed ^ length

    for i in range(0, length, 4):
        k = (
            input_string[i]
            | (input_string[i + 1] << 8)
            | (input_string[i + 2] << 16)
            | (input_string[i + 3] << 24)
        )
        k = (k * m) & 0xffffffff
        k ^= (k >> r)
        k = (k * m) & 0xffffffff

        h = (h * m) & 0xffffffff
        h ^= k

    h ^= h >> 13
    h = (h * m) & 0xffffffff
    h ^= h >> 15

    return h
