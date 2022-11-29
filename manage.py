# ======== 페이지 정보 =============================
import sys
import os
import re
import shutil
GITHUB_USER = 'kjh36102'
REPOSITORY_NAME = 'kjh36102.github.io'
BRANCH_NAME = 'master'
# ==================================================


URL_BASE = 'https://raw.githubusercontent.com/'+GITHUB_USER+'/' + \
    REPOSITORY_NAME+'/'+BRANCH_NAME+'/_posts/{category}/{post_dir}/'


def read_file(file_path):
    # 파일 읽기
    origin_file = open(file_path, 'r', encoding='utf-8')
    origin_raw = origin_file.read()
    origin_file.close()

    return origin_raw


def write_file(file_path, text):
    # 파일에 쓰기
    target_file = open(file_path, 'w', encoding='utf-8')
    target_file.writelines(text)
    target_file.close()


def extract_info(file_path):
    # 입력받은 경로에서 정보 추출
    path_splits = file_path.split('\\')
    path_splits.pop()
    post_dir = path_splits.pop()
    category = path_splits.pop()

    return category, post_dir

# --------------------------------------------------------


def show_help():
    help_str = '''\
[command]           | [alias]  |                      [desc]                    |   [args]
--convert_image     | -c       | md 파일의 이미지url을 github url로 바꿉니다.   | 0: md파일 경로
'''
    print(help_str)


def convert_image(file_path):
    origin_raw = read_file(file_path)

    regex = '!\[.*\]\(.*\)'
    find_list = re.findall(regex, origin_raw)

    category,  post_dir = extract_info(file_path)
    url = URL_BASE.format(category=category, post_dir=post_dir)

    for elem in find_list:
        if 'https' in elem:
            continue

        tag_split = str.split(elem, '(')
        img_name = tag_split[1][:-1]

        print('\tTarget Image:', img_name, end='     ')
        
        converted_url = (url + img_name).replace(' ', '%20')

        origin_raw = origin_raw.replace(
            elem, tag_split[0] + '(' + converted_url + ') <!-- CONVERTED -->')

        print('...DONE')

    write_file(file_path, origin_raw)

    print(f'* Converting All Done!')


def moveto(file_path, new_category_name, new_post_name):
    category,  post_name = extract_info(file_path)

    old_path = os.path.abspath(f'./_posts/{category}/{post_name}')
    new_path = os.path.abspath(f'./_posts/{new_category_name}/{new_post_name}')

    origin_raw = read_file(file_path)

    origin_raw = origin_raw.replace(f'[{category}]', f'[{new_category_name}]', 1)
    origin_raw = origin_raw.replace(f'/{category}/', f'/{new_category_name}/')
    origin_raw = origin_raw.replace(f'/{post_name}/', f'/{new_post_name}/')

    write_file(old_path + '/' + new_post_name + '.md', origin_raw)

    os.remove(file_path)

    #폴더 옮기기
    shutil.move(old_path, new_path)

# -------------------메인-------------------------

args = sys.argv

try:
    if args[1] in ['--help', '-h']:
        show_help()
    elif args[1] in ['--convert_image', '-c']:
        convert_image(os.path.abspath(args[2]))
    elif args[1] in ['--rename', '-n']:
        moveto(os.path.abspath(args[2]), args[3], args[4])
    else:
        print(args[1] + ' 은(는) 알 수 없는 명령입니다.')
        print('도움말을 보시려면 python manage.py -h 를 입력하세요.')
except Exception as e:
    print('오류 발생: ', e)
