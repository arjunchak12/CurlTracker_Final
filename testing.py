import os

path, dirs, files = next(os.walk("Plots/"))
file_count = len(files)
print(file_count)