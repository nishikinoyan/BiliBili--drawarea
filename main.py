import requests
import json
import picture_info
import os
import re
import time
import threading

def bilibili_picture_save(file_name,picture_title,picture_format,original_page):
    with open(os.path.join(picture_dir, file_name + picture_format), 'wb') as o:
        o.write(original_page.content)
        print('下载图片:  ' + picture_title)


def bilibili_picture_download(picture_items):

    for picture_item_temp in picture_items:
        picture_title = picture_item_temp.title
        picture_link = picture_item_temp.picture_link
        picture_doc_id = picture_item_temp.doc_id
        picture_format = picture_link[-4:]

        re_str = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_picture_title = re.sub(re_str, "_", picture_title)

        file_name = new_picture_title + ' id~' + str(picture_doc_id)

        try:
            time.sleep(0.7)
            original_page = bilibili_session.get(picture_link)
            if(original_page.status_code == 200):
                picture_save_thread = threading.Thread(target=bilibili_picture_save,args=(file_name,picture_title,picture_format,original_page))
                picture_save_thread.start()




        except Exception as e:
            print('原图链接访问下载错误' + str(e))
        continue



def bilibili_json_get(json_info):

    picture_items = []

    bilibili_picture_json = json.loads(json_info)['data']

    bilibili_detail_pitcure_json = bilibili_picture_json['items']

    for bilibili_json_temp in bilibili_detail_pitcure_json:
        uid = bilibili_json_temp['user']['uid']
        author_name = bilibili_json_temp['user']['name']
        title = bilibili_json_temp['item']['title']
        picture_link = bilibili_json_temp['item']['pictures'][0]['img_src']
        doc_id = bilibili_json_temp['item']['doc_id']

        picture_items.append(picture_info.picture_item(uid,author_name,title,picture_link,doc_id))


    return  picture_items



bilibili_session = requests.session()
headers = {
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1)AppleWebKit/537.36(KHTML,likeGecko)Chrome/58.0.3029.110Safari/537.36',
        'Accept-Encoding': 'gzip,deflate'
    }

if __name__ == '__main__':


    print('输入图片储存路径')

    picture_dir = input()

    if not os.path.exists(picture_dir):
        os.mkdir(picture_dir)


    print('最新还是最热门？  1：最热门  |  2：最新')

    catch_type = input()
    max_page = 0;
    catch_type_url = ''
    if(catch_type == '1'):
        max_page = 24
        catch_type_url = 'hot'
        picture_dir = picture_dir + '/hot'
        if not os.path.exists(picture_dir):
            os.mkdir(picture_dir)

    else:
        max_page = 1000
        catch_type_url = 'new'
        picture_dir = picture_dir + '/new'
        if not os.path.exists(picture_dir):
            os.mkdir(picture_dir)


    # 最热门 'https://api.vc.bilibili.com/link_draw/v2/Doc/list?category=all&type=hot&page_num=0&page_size=20'
    # 最新   'https://api.vc.bilibili.com/link_draw/v2/Doc/list?category=all&type=new&page_num=0&page_size=20'

    p = 0
    while p <= max_page:
      print('第' + str(p) + '页###############')
      bilibili_draw_start_url = 'https://api.vc.bilibili.com/link_draw/v2/Doc/list?category=all&type='+ catch_type_url +'&page_num=' + str(p) + '&page_size=20'
      print(bilibili_draw_start_url)
      bilibili_draw_json_page = bilibili_session.get(bilibili_draw_start_url,headers=headers).content

      picture_items = bilibili_json_get(bilibili_draw_json_page)

      bilibili_picture_download(picture_items)
      p = p + 1





