import pickle
import sys

print("Enter the pickle name")
inp = input()

with open(inp, 'rb') as f:
    loaded1 = pickle.load(f)
    loaded2 = pickle.load(f)

print("File: ", loaded1)
print("Dictionary: ", loaded2)