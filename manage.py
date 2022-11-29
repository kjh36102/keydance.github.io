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
[command]         | [alias]  |                      [desc]                    |   [args]
--------------------------------------------------------------------------------------------
convert_image     | cv       | md 파일의 이미지url을 github url로 바꿉니다.   | -f *파일 경로
--------------------------------------------------------------------------------------------
upload            | up       | 블로그를 github에 upload 합니다.               | 
--------------------------------------------------------------------------------------------
new_post          | new      | 새로운 포스팅을 작성합니다.                    | -c *카테고리 이름
                                                                              | -t *포스팅 이름
                                                                              | -d  날짜
--------------------------------------------------------------------------------------------
move              | mv       | 포스팅의 카테고리, 날짜, 이름을 바꿉니다.      | -f *파일 경로
                               선택적 변경이 가능합니다.                      | -c  카테고리 이름 
                                                                              | -d  날짜
                                                                              | -t  포스팅 이름
--------------------------------------------------------------------------------------------
                                                                * 별이 있는 인자는 필수항목입니다.
'''
    print(help_str)


def upload_all():
    os.system('git add *')
    os.system('git commit -m "auto committed by manage.py"')
    os.system('git push origin master')
    print('\t* Upload Completed!')

def create_new_post(category, title, date):

    #명령인자 검사
    if category == None: raise Exception('카테고리 이름이 없습니다.')
    if title == None: raise Exception('포스팅 제목이 없습니다.')
    if date == None: date = time.strftime('%Y-%m-%d', time.localtime())

    #date 형식 검사
    if bool(re.match('\d{4}-\d{2}-\d{2}', date)) == False: raise Exception('날짜 형식이 올바르지 않습니다.')

    dir = f'./_posts/{category}'
    if os.path.exists(dir) == False:
        os.mkdir(dir)

    dir += f'/{date}-{title}'
    if os.path.exists(dir) == False:
        os.mkdir(dir)

    data = f'''\
---
layout: post
title: {title}
categories: [{category}]
---

### **새로운 포스팅!!**
manage.py가 작성했습니다.
\
'''

    write_file(f'{dir}/{date}-{title}.md', data)

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

    #명령인자 검사
    if new_category_name == None: new_category_name = category
    if new_post_name == None: new_post_name = post_name
    if new_date == None: new_date = date

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

    #날짜와 이름에 변화가 있는 경우만 새롭게 생긴 파일 삭제
    if date != new_date or post_name != new_post_name:
        old_file = new_path + '/' + date + '-' + post_name + '.md'
        os.remove(old_file) #오래된 파일 지우기
        print('old_file:', old_file)

    #이전 카테고리에 포스팅 없으면 카테고리 삭제
    category_dir = os.path.abspath(f'./_posts/{category}')
    if os.listdir(category_dir).__len__() == 0:
        os.rmdir(category_dir)

    print(f'\tTarget Post: [{category}] {date}-{post_name}')
    print(f'\t\t  -> [{new_category_name}] {new_date}-{new_post_name}')
    print('\t* Moving Completed!')

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
elif cmd in ['upload', 'up']:
    upload_all()
elif cmd in ['new_post', 'new']:
    create_new_post(
        get_one(['--category', '-c'], args),
        get_one(['--title', '-t'], args),
        get_one(['--date', '-d'], args)
    )
elif cmd in ['convert_image', 'cv']:
    convert_image(os.path.abspath(get_one(['--file', '-f'], args)))
elif cmd in ['move', 'mv']:
    move(
        os.path.abspath(get_one(['--file', '-f'], args)),
        get_one(['--category', '-c'], args),
        get_one(['--title', '-t'], args),
        get_one(['--date', '-d'], args)
    )
else:
    print(cmd + ' 은(는) 알 수 없는 명령입니다.')
    print('도움말을 보시려면 python manage.py ? 를 입력하세요.')
# except Exception as e:
#     print('오류가 발생했습니다:', e)
#     sys.exit(1)
