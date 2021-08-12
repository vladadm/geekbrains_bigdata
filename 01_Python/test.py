#!python3

while True:
    f = str(input("Input text: "))
    if not f:
        print("User input empty line, saved file.")
        break
    print(f'User input: {f}')