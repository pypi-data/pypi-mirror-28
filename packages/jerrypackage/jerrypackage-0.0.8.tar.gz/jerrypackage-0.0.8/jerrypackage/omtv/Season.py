import requests
import re
from bs4 import BeautifulSoup
import bs4
from .Episode import Episode
import json
import os
import copy
import datetime
from ..tools import chinanumber
import time

class Season:
    season_url = ""         # 指向这个season的url地址
    season_num = 0
    tv_name = ""
    last_update = ""
    broadcast_time = ""
    episode_object_list = []

    def __init__(self, name, num, url):
        self.tv_name = name
        self.season_url = url
        self.season_num = num
        self.last_update = ""
        self.broadcast_time = ""
        self.episode_object_list = []
        self.last_episode = 0

    def generate_episode_object_dict(self):
        """
        Season类最重要的函数，初始化好Season类之后，我们就知道了它指向的一个URL，这个网页上有这个Season的所有剧集的
        下载链接，这个函数就是去爬取这些信息，并把每一集生成一个Episode对象，把所有的Episode对象组成了episode_object_list。
        注意这个地方为什么用List,而不是用dict，按道理一集对应一个Episode对象很合理。
        但是爬网页过程中发现，一集经常是对应着好几种不同的分辨率文件可供下载，就算是跳过无字幕的，也存在mp4, rmvb, mkv等不同
        的格式和大小。因此为简单起见，使用列表，但是列表中的每一项是个dict {episode_number: episode_obj}
        需要的话可以再处理，将列表分成几个不同的列表，每个列表对应一种类型的文件。

        注意：每个episode目前就相当于一个数据集合，只定义了一个初始化函数，就是用来保存一下数据而已。
        :return:
        """
        print("Request url in Season {} for episode, url:{}".format(self.season_num, self.season_url))
        while True:
            try:
                r = requests.get(self.season_url)
                break
            except Exception as err:
                print(err)
                time.sleep(10)

        content = r.text
        soup = BeautifulSoup(content, 'lxml')
        article_content_tags = soup.find_all('div', class_="article_content")
        assert len(article_content_tags) == 1, "目前有{}个，不是一个，可能存在问题".format(len(article_content_tags))

        # 获取最后更新时间, 奇怪，find_all("span", text=re.compile('.*'))查不到最后一个span的字符串，只能不加条件，自己来查找
        span_tags = article_content_tags[0].find_all("span")
        next_is_broadcast_time = False
        if span_tags:
            for span_tag in span_tags:
                if next_is_broadcast_time:
                    self.broadcast_time = span_tag.text
                    next_is_broadcast_time = False
                if re.search('首播', span_tag.text):
                    # print(span_tag.next_sibling.string)
                    if re.search('\d+[年-]\d+[月-]\d+', span_tag.next_sibling.string):
                        self.broadcast_time = re.findall('(\d+[年-]\d+[月-]\d+.*$)', span_tag.next_sibling.string)[0]
                    else:
                        next_is_broadcast_time = True
                if re.search('更新', span_tag.text):      # 还不能是string属性，必须是text属性
                    self.last_update = re.findall('(\d+年\d+月\d+日)', span_tag.text)[0]

        table_tags = article_content_tags[0].find_all('table')
        if len(table_tags) == 0:      # 一页中包含多个season的时候，通常不是用table，而是用<ul>包含某一季
            ul_tags = article_content_tags[0].find_all('ul')
            for ul_tag in ul_tags:
                previous = ul_tag.previous_sibling
                while previous is not None:
                    if isinstance(previous, bs4.element.Tag) and previous.name == "h2":
                        if re.search(r'字幕', previous.text) and re.search(r'中', previous.text):
                            li_tags = ul_tag.find_all('li')

                            for li_tag in li_tags:
                                tmp_result = re.findall(r'第(.*?)季第(.*?)集', li_tag.text)
                                if len(tmp_result) == 0:    # 如果为空，表示找到的很可能是全部剧集打包下载的链接
                                    tmp_result = re.findall(r'合集', li_tag.text)
                                    if len(tmp_result) > 0:
                                        a_tags = li_tag.find_all('a')
                                        download_link_list = []
                                        episode_name = li_tag.text
                                        episode_size = None
                                        download_link_list.append(a_tags[0]['href'])
                                        episode_obj = Episode(episode_name, 'ALL', episode_size,
                                                              download_link_list)

                                        self.episode_object_list.append(['ALL', episode_obj])
                                        return
                                else:
                                    assert len(tmp_result) == 1, '找到的字符串个数：{}'.format(len(tmp_result))

                                    tmp_result1 = tmp_result[0][0]
                                    tmp_result2 = tmp_result[0][1]

                                # 这个ul tag里面的 li tag 都是对应 创建的这个season 的
                                if chinanumber.from_china(tmp_result1) == self.season_num:
                                    a_tags = li_tag.find_all('a')
                                    download_link_list = []
                                    episode_name = None
                                    episode_size = None

                                    download_link_list.append(a_tags[0]['href'])
                                    episode_name = re.findall('(第.*?季第.*?集)', li_tag.text)
                                    episode_obj = Episode(episode_name[0], tmp_result2, episode_size,
                                                          download_link_list)

                                    self.episode_object_list.append([tmp_result2, episode_obj])

                                    tmp_index = tmp_result2.find('-')
                                    if tmp_index != -1:
                                        tmp_result2 = tmp_result2[(tmp_index+1):]
                                    tmp_index = tmp_result2.rfind('&')
                                    if tmp_index != -1:
                                        tmp_result2 = tmp_result2[(tmp_index+1):]

                                    episode_number = int(tmp_result2)
                                    if episode_number > self.last_episode:
                                        self.last_episode = episode_number
                            break
                        break
                    previous = previous.previous_sibling

            return

        for table_tag in table_tags:
            previous = table_tag.previous_sibling
            while previous is not None:
                if isinstance(previous, bs4.element.Tag) and previous.name == "h2":
                    # 第一个table, 双语字幕的我们要记录链接。
                    if re.search(r'字幕', previous.text) and re.search(r'中英', previous.text):
                        td_tags = table_tag.find_all('td')

                        for td in td_tags:
                            a_tags = td.find_all('a')
                            download_link_list = []
                            episode_name = None
                            episode_size = None

                            # a_tags不为空，代表这个td项里面存在某一集的有效链接，可能是2个（ed2k, magnet），或者更多
                            if len(a_tags) > 0:
                                for a_tag in a_tags:
                                    if episode_name is None:
                                        episode_name = a_tag.text
                                    download_link_list.append(a_tag['href'])

                                aa = re.findall(r'[Ss]?(\d*)[Ee](\d+)', episode_name)
                                if len(aa) == 0:
                                    aa = re.findall(r'第(\d+)季(\d+).*\.', episode_name)
                                    if len(aa) == 0:
                                        aa = re.findall(r'第(.*?)季(\d+)\.', episode_name)
                                        if len(aa) == 0:        # 还是不行，就给一个缺省的值
                                            aa.append([str(self.season_num), str(-1)])
                                        else:
                                            aa[0] = list(aa[0])
                                            aa[0][0] = str(chinanumber.from_china(aa[0][0]))

                                episode_number = ''

                                if len(aa) > 0:
                                    # 有时候多个season的page也使用table的方式，这时候如果不是期望的season就return
                                    if aa[0][0] != '' and int(aa[0][0]) != self.season_num:
                                        return
                                    # some time episode do not give season number
                                    assert aa[0][0] == '' or int(aa[0][0]) == self.season_num, "Season number is {} by name, but {} by \
                                        class init".format(int(aa[0][0]), self.season_num)
                                    episode_number = aa[0][1]
                                else:
                                    assert "Need check again, 增加新的容错方式"

#                                td_next = td.next_sibling
#                                while td_next is not None:
#                                    if isinstance(td_next, bs4.element.Tag) and td_next.name == 'td':
#                                        if td_next.has_attr('class'):
#                                            if td_next.get('class')[0] == 'right':
#                                                episode_size = td_next.text
#                                        break
#                                    td_next = td_next.next_sibling

                                size_td = td.find_next_sibling('td', class_='right')
                                if size_td:
                                    episode_size = size_td.text
                                else:
                                    size_td = td.find_next_sibling('td', align='right')
                                    if size_td:
                                        episode_size = size_td.text

                                episode_obj = Episode(episode_name, episode_number, episode_size, download_link_list)
                                if int(episode_number) > self.last_episode:
                                    self.last_episode = int(episode_number)
                                self.episode_object_list.append([episode_number, episode_obj])
                            # a_tag是空的时候，表示无有效链接，但是如果该td.text包含tv_name，代表还没有播出，今后会播出
                            else:
                                if td.text.find(self.tv_name) != -1:
                                    episode_name = td.text
                                    download_link_list.append(None)

                                    aa = re.findall(r'[Ss](\d+)[Ee](\d+)', episode_name)
                                    assert int(aa[0][0]) == self.season_num, "Season number is {} by name, but {} by \
                                        class init".format(int(aa[0][0]), self.season_num)

                                    episode_obj = Episode(episode_name, aa[0][1], episode_size, download_link_list)
                                    self.episode_object_list.append([aa[0][1], episode_obj])
                        break
                    # 第二个table的内容，一般都是高清无字幕的，目前暂时不处理，直接跳出循环，继续。
                    else:
                        break
                previous = previous.previous_sibling

    def load(self, season_num):
        try:
            with open('./'+self.tv_name+'/'+self.tv_name+' S{:02d}'.format(season_num)+'.json', 'r', encoding='utf-8') as f:
                loaded_season_dict = json.load(f)
        except FileNotFoundError:
            print("No Season File, Stop load TV: {}, Season {}!".format(self.tv_name, season_num))
            return

        list_todo = loaded_season_dict.get("episode_object_list")
        for index in range(0, len(list_todo)):
            episode_obj = Episode('', '', '', [])
            episode_obj.__dict__.update(list_todo[index][1])
            list_todo[index][1] = episode_obj

        self.__dict__.update(loaded_season_dict)
        print("LOAD Season {} json file".format(self.season_num))

    def dump(self):
        if not os.path.exists('./' + self.tv_name):
            print("Makedir in season:", './' + self.tv_name)
            os.mkdir('./' + self.tv_name)

        with open('./'+self.tv_name+'/'+self.tv_name+' S{:02d}'.format(self.season_num)+'.json', 'w', encoding='utf-8') as f:
            print("DUMP Season {} json file".format(self.season_num))
            json.dump(self.get_serializable_dict(), f, ensure_ascii=False, indent=4)

    def get_serializable_dict(self):
        return_dict = copy.deepcopy(self.__dict__)
        list_todo = return_dict.get("episode_object_list")
        for index in range(0, len(list_todo)):
            list_todo[index][1] = list_todo[index][1].__dict__

        return return_dict

    def backup_json(self):
        if os.path.exists('./' + self.tv_name + '/' + self.tv_name+' S{:02d}'.format(self.season_num)+'.json'):
            os.rename('./' + self.tv_name + '/' + self.tv_name + ' S{:02d}'.format(self.season_num)+'.json',
                      './' + self.tv_name+'/' + self.tv_name + ' S{:02d} '.format(self.season_num) + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.json')
        else:
            print("OLD TV File NOT exist!!")
