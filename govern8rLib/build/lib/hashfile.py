import hashlib

# get hash of a file
def  hash_file(file):
    print "hashing ..."+file

    sha = hashlib.sha256()
    with open(file, 'rb') as f:
        while True:
            block = f.read(2**10) # Magic number: one-megabyte blocks.
            if not block: break
            sha.update(block)
        return sha.hexdigest()


def main():
    hashdigest = hash_file("bootstrap.ini")
    print hashdigest
    hashdigest = hash_file("C:\Users\Bharathi\Downloads\\beast.jpg")
    print hashdigest

if __name__ == "__main__":
    main()
