# ======== 페이지 정보 =============================
import sys
import os
import re
import shutil
import time
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
    post_name = post_dir.split('-')[-1]
    category = path_splits.pop()

    date_split = post_dir.split('-')
    date = str.join('-', date_split[:-1])
    
    return category, post_dir, post_name, date

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

    category,  post_dir, _, _ = extract_info(file_path)
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


def move(file_path, new_category_name, new_post_name, new_date):
    category, _, post_name, date = extract_info(file_path)

    print(category, post_name, date)

    #명령인자 검사
    if new_category_name == None: new_category_name = category
    if new_post_name == None: new_post_name = post_name
    if new_date == None: new_date = date

    print('args check:',new_category_name,new_post_name,new_date)

    old_path = os.path.abspath(f'./_posts/{category}/{date}-{post_name}')
    new_path = os.path.abspath(f'./_posts/{new_category_name}/{new_date}-{new_post_name}')

    #데이터 변경
    origin_raw = read_file(file_path)

    origin_raw = origin_raw.replace(f'title: {post_name.split("-")[-1]}', f'title: {new_post_name.split("-")[-1]}', 1)    #헤더 변경
    origin_raw = origin_raw.replace(f'[{category}]', f'[{new_category_name}]', 1)

    origin_raw = origin_raw.replace(f'/{category}/', f'/{new_category_name}/')  #이름들 변경
    origin_raw = origin_raw.replace(f'/{date}-{post_name.replace(" ", "%20")}/', f'/{new_date}-{new_post_name.replace(" ", "%20")}/')

    write_file(old_path + '/' + new_date + '-' + new_post_name + '.md', origin_raw)

    #폴더 옮기기
    shutil.move(old_path, new_path)

    old_file = new_path + '/' + date + '-' + post_name + '.md'
    os.remove(old_file) #오래된 파일 지우기
    print('removed:', old_file)

    #이전 카테고리에 포스팅 없으면 카테고리 삭제
    category_dir = os.path.abspath(f'./_posts/{category}')
    if os.listdir(category_dir).__len__() == 0:
        os.rmdir(category_dir)

# -------------------메인-------------------------

def get_one(keyset, dict):
    for key in keyset:
        try:
            if dict[key] != None: return dict[key]
        except KeyError:
            pass
    return None

cmd = sys.argv[1]
args = {}

#argument 딕셔너리화
try:
    for i in range(2, len(sys.argv), 2):
        args[sys.argv[i]] = sys.argv[i + 1]
except IndexError:
    print('명령인자가 충분하지 않습니다.')
    sys.exit(1)

# try:
if cmd in ['help', '?']:
    show_help()
elif cmd in ['convert_image', 'cv']:
    convert_image(os.path.abspath(get_one(['--file', '-f'], args)))
elif cmd in ['move', 'mv']:
    move(
        os.path.abspath(get_one(['--file', '-f'], args)),
        get_one(['--category', '-c'], args),
        get_one(['--post', '-p'], args),
        get_one(['--date', '-d'], args)
    )
else:
    print(cmd + ' 은(는) 알 수 없는 명령입니다.')
    print('도움말을 보시려면 python manage.py ? 를 입력하세요.')
# except Exception as e:
#     print('오류가 발생했습니다:', e)
#     sys.exit(1)
