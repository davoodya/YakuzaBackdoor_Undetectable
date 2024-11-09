import os, sys


print(os.path.realpath(sys.argv[0]))

print(sys.argv[1])

try:
    if not sys.argv[2]:
        print("Enter Second argument")
except IndexError:
    print("Second argument Not Enter")