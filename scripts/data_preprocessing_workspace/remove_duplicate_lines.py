"""
Script taken from https://www.codevscolor.com/python-remove-duplicate-lines-text-file/
"""
import hashlib
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

start_time = time.time()
input_file_path = sys.argv[1]
output_file_path = input_file_path + ".no-duplicates"

completed_lines_hash = set()
output_file = open(output_file_path, "a")


for line in open(input_file_path, "r"):

    hashValue = hashlib.md5(line.rstrip().encode(encoding="utf8")).hexdigest()
    if hashValue not in completed_lines_hash:
        output_file.write(line)
        completed_lines_hash.add(hashValue)

output_file.close()
print("--- %s seconds ---" % (time.time() - start_time))
