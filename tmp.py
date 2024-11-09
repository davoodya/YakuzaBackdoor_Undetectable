import os, sys

filename = os.path.basename(sys.argv[0])
filepath =os.path.realpath(sys.argv[0])
print(f"File Name is: {filename}\nFile Path is: {filepath}")


try:
    print(f"[+] First Argument is: {sys.argv[1]}")

except IndexError: print("First Argument Not Enter.")

try:
    print(f"[+] Second Argument is: {sys.argv[2]}")

except IndexError: print("Second Argument Not Enter.")