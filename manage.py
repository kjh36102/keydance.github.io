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

    date_split = post_dir.split('-')
    date = str.join('-', date_split[:-1])
    

    return category, post_dir, date

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

    category,  post_dir, _ = extract_info(file_path)
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
    category,  post_name, date = extract_info(file_path)

    new_post_name = date + '-' + new_post_name

    old_path = os.path.abspath(f'./_posts/{category}/{post_name}')
    new_path = os.path.abspath(f'./_posts/{new_category_name}/{new_post_name}')

    #데이터 변경
    origin_raw = read_file(file_path)

    origin_raw = origin_raw.replace(f'title: {post_name.split("-")[-1]}', f'title: {new_post_name.split("-")[-1]}', 1)    #헤더 변경
    origin_raw = origin_raw.replace(f'[{category}]', f'[{new_category_name}]', 1)

    origin_raw = origin_raw.replace(f'/{category}/', f'/{new_category_name}/')  #이름들 변경
    origin_raw = origin_raw.replace(f'/{post_name.replace(" ", "%20")}/', f'/{new_post_name.replace(" ", "%20")}/')

    write_file(old_path + '/' + new_post_name + '.md', origin_raw)
    os.remove(file_path) #원본폴더 파일 지우기

    #폴더 옮기기
    shutil.move(old_path, new_path)

    #이전 카테고리에 포스팅 없으면 카테고리 삭제
    category_dir = os.path.abspath(f'./_posts/{category}')
    if os.listdir(category_dir).__len__() == 0:
        os.rmdir(category_dir)

# -------------------메인-------------------------

args = sys.argv

# try:
if args[1] in ['--help', '-h']:
    show_help()
elif args[1] in ['--convert_image', '-c']:
    convert_image(os.path.abspath(args[2]))
elif args[1] in ['--rename', '-n']:
    moveto(os.path.abspath(args[2]), args[3], args[4])
else:
    print(args[1] + ' 은(는) 알 수 없는 명령입니다.')
    print('도움말을 보시려면 python manage.py -h 를 입력하세요.')
# except Exception:
#     pass
