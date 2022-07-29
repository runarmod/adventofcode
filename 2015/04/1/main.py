import hashlib


with open("../input.txt", "r") as f:
    inputt = f.read()

leadingZeros = 5
i = 0
while True:
    thingToHash = inputt + str(i)

    hash = hashlib.md5(thingToHash.encode()).hexdigest()
    if hash[:leadingZeros] == "0" * leadingZeros:
        print("i:", str(i))
        print("thingToHash:", thingToHash)
        print("hash:", hash)
        break

    i += 1