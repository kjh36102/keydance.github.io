import sys
import os
from pathlib import Path

file_path = sys.argv[1]
file_path = os.path.abspath(file_path)

print('args:', sys.argv)
print('abs_path:', file_path)

if len(sys.argv) != 2:
    print('Args length not match')
    sys.exit()


url_format = 'https://raw.githubusercontent.com/kjh36102/kjh36102.github.io/master/_posts/{{page.categories}}/{{page.date | date: "%Y-%m-%d-"}}{{page.id | remove: "/"}}'

# domain = os.getcwd()
# print('domain:',domain)

# #파일 읽기
# origin = open(file_path, 'rb')

# while True:
#     line = origin.readline()
#     if not line: break
#     print(line.decode())

# origin.close()
