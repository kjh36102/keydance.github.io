# ======== 페이지 정보 =============================
GITHUB_USER = 'kjh36102'
REPOSITORY_NAME = 'kjh36102.github.io'
BRANCH_NAME = 'master'
# ==================================================

import sys
import os
import re

def show_help():
    help_str = '''\
[command]           | [alias]  |                      [desc]                    |   [args]
--conver_image      | -c       | md 파일의 이미지url을 github url로 바꿉니다.   | 0: md파일 경로
'''
    print(help_str)


def convert_image(file_path):
   #입력받은 경로에서 정보 추출
    path_splits = file_path.split('\\')
    path_splits.pop()
    post_dir = path_splits.pop()
    category = path_splits.pop()

    URL_BASE = f'https://raw.githubusercontent.com/{GITHUB_USER}/{REPOSITORY_NAME}/{BRANCH_NAME}/_posts/{category}/{post_dir}/'

    #파일 읽기
    origin_file = open(file_path, 'r', encoding='utf-8')
    origin_raw = origin_file.read()
    origin_file.close()

    #정규식으로 이미지부분만 가져오기
    regex = '!\[.*\]\(.*\)'
    find_list = re.findall(regex, origin_raw)

    for elem in find_list:
        if 'https' in elem: continue

        tag_split = str.split(elem, '(')
        img_name = tag_split[1][:-1]
        
        print('\tTarget Image:', img_name, end='     ')

        converted_url = (URL_BASE + img_name).replace(' ', '%20')

        origin_raw = origin_raw.replace(elem, tag_split[0] + '(' + converted_url + ') <!-- CONVERTED -->')
        print('...DONE')

    #파일에 쓰기
    target_file = open(file_path, 'w', encoding='utf-8')
    target_file.writelines(origin_raw)
    target_file.close()

    print(f'* Converting All Done!')

def rename(file_path):
    pass

#-------------------메인-------------------------

args = sys.argv

try:
    if args[1] in ['--help', '-h']: show_help()
    elif args[1] in ['--convert_image', '-c']:
        convert_image(os.path.abspath(args[2]))
    elif args[1] in ['--rename', '-n']:
        rename(os.path.abspath(args[2]))
    else:
        print(args[1] + ' 은(는) 알 수 없는 명령입니다.')
        print('도움말을 보시려면 python manage.py -h 를 입력하세요.')
except Exception as e:
    print('오류 발생: ', e)
