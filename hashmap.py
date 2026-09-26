def hash_function(id_hash, tam):
    acum = 0
    for i in range(len(id)):
        acum = acum * 31 + i + ord(id[i])

    result = acum % tam

    return result

class table:
    def constructor():