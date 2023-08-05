import requests
from bs4 import BeautifulSoup
import re
from ..tools import chinanumber
from .Season import Season
import json
import os
import copy
import datetime, time


def __class_is_art_img_or_page_navi__(class_):
    return class_ == "art_img_box clearfix" or class_ == "page_navi"


class TV:
    """
    定义爬到的TV的信息: 名字，URL, 最新的season, 每个season对象组成的字典,key是season的序号
    """
    tv_name = ''
    tv_url = ''  # 指向这个剧的url地址
    latest_season = 0
    season_object_dict = {}

    def __init__(self, name, url):
        self.tv_name = name
        self.tv_url = url
        latest_season = 0
        self.season_object_dict = {}

    def __generate_season_object_recursive__(self, url, season_to_generate=-1):
        next_url = None
        print("Request url in __generate_season_object_recursive__:", url)

        while True:
            try:
                r = requests.get(url)
                break
            except Exception as err:
                print(err)
                time.sleep(10)

        content = r.text

        # 分析根据名字查到的美剧列表网页
        soup = BeautifulSoup(content, 'lxml')
        div_tags = soup.find_all('div', class_=__class_is_art_img_or_page_navi__)



        for div_tag in div_tags:
            # 加入第，处理火线这个特殊情况
            if len(div_tag.find_all('a', title=re.compile(self.tv_name + "第"))) > 0:
                a_tag = div_tag.find('a', title=re.compile(self.tv_name+"第"))  # 在这个div里面找到第一个就可以了
            else:
                # 加入， 处理 达.芬奇的恶魔的情况
                a_tag = div_tag.find('a', string=re.compile(self.tv_name + "第"))  # 在这个div里面找到第一个就可以了

                if a_tag is None:
                    a_tag = div_tag.find('a', title=re.compile(self.tv_name + "全"))

            if a_tag is not None:
                a_tag_title = a_tag['title']
                tmp_result = re.findall(r'第(.*?)季', a_tag_title)
                if len(tmp_result) != 1:
                    tmp_result = re.findall(r'全', a_tag_title)
                    if len(tmp_result)==1:       # 处理碰到只有一季，文字中会用全集表示
                        tmp_result[0] = '一'
                    else:
                        print("Find some tv season with this name, but without Season Number {} times, 可能是衍生剧".format(len(tmp_result)))
                        continue


                multi_seasons = False
                if len(tmp_result[0]) > 1:
                    multi_seasons = True
                    tmp_result1 = re.findall(r'(.*)[至到](.*)', tmp_result[0])      # 处理一至九，一到八之类的情况
                    if len(tmp_result1) > 0:
                        numA = chinanumber.from_china(tmp_result1[0][0])
                        numB = chinanumber.from_china(tmp_result1[0][1])
                        tmp_result[0] = []
                        for n in range(numA, numB+1):
                            tmp_result[0].append(chinanumber.to_china(n))
                    else:
                        for i in range(0, len(tmp_result[0])-1):
                            numA = chinanumber.from_china(tmp_result[0][i])
                            numB = chinanumber.from_china(tmp_result[0][i+1])
                            if numA+1 != numB:
                                multi_seasons = False

                season_TODO = []
                if multi_seasons:
                    for i in range(0, len(tmp_result[0])):       # 存在第四五六季的情况，这样要处理三个Season
                        season_TODO.append(chinanumber.from_china(tmp_result[0][i]))  # 基本上应该只会找到一个
                else:
                    season_TODO.append(chinanumber.from_china(tmp_result[0]))

                for season in season_TODO:
                    if season_to_generate == -1 or season_to_generate == season:
                        season_object = Season(self.tv_name, season, a_tag['href'])
                        season_object.generate_episode_object_dict()
                        # key of a dict should be str, most people doing so, if NOT, read from json file will go wrong
                        self.season_object_dict[str(season)] = season_object
                        if season_to_generate == season:
                            break
            else:
                a_tag = div_tag.find('a', text=re.compile("下一页"))
                if a_tag is not None:
                    if next_url is None:
                        next_url = a_tag['href']
                    else:
                        assert next_url == a_tag['href'], "不一样的话，可能有异常"

        if season_to_generate != -1 and str(season_to_generate) in self.season_object_dict.keys():
            return

        seasons = sorted([int(n) for n in self.season_object_dict.keys()])
        if len(seasons) == 0 or seasons != [n for n in range(1, max(seasons) + 1)]:  # 没有取全
            if next_url is not None:
                if season_to_generate == -1:
                    self.__generate_season_object_recursive__(next_url)
                else:
                    self.__generate_season_object_recursive__(next_url, season_to_generate)
            else:
                print("Crawl all the searching result, only find these seasons: ", seasons)

    def generate_season_object_dict(self):
        """
        生成类成员 season_object_dict, 利用爬取到的信息填充这个season对象，注意是一对一的，每个season对应一个season对象。
        算法会一直尝试爬到第一季，如果找完所有的搜索页都没有找全，会打印一个warning，告诉找到了那些季。
        爬取过程中，会调用season的函数 generate_episode_object_dict，生成这个season对象里面的所有episode对象
        :return:
        """
        print("Generate all the season objects in dict: ", self.tv_name)
        self.__generate_season_object_recursive__(self.tv_url)
        if len(self.season_object_dict.keys()) > 0:
            self.latest_season = max([int(n) for n in self.season_object_dict.keys()])
        print("End : ", self.tv_name)

    def generate_season_object(self, season):
        print("Generate specific Season object: ", self.tv_name, " Season: ", season)
        self.__generate_season_object_recursive__(self.tv_url, season)
        self.latest_season = -1
        print("End : ", self.tv_name)

    def dump(self, season=-1):
        """
        把TV对象保存在json文件里面, 利用了类的__dict__属性，并进入Season和Episode对象，使用他们的__dict__属性
        最后，降生成的dict类型的变量使用json进行序列化
        :return:
        """
        if season == -1:
#            for key in self.season_object_dict.keys():
#                season_obj = self.season_object_dict.get(key)
#                season_obj.dump()

            if not os.path.exists('./'+self.tv_name):
                print("Makedir in tv:", './'+self.tv_name)
                os.mkdir('./'+self.tv_name)

            with open('./'+self.tv_name+'/'+self.tv_name + '.json', 'w', encoding='utf-8') as f:
                print("DUMP TV: {} json file".format(self.tv_name))
                json.dump(self.get_serializable_dict(), f, ensure_ascii=False, indent=4)
        else:       # 指定dump某一季的时候，TV对象不会被dump
            assert str(season) in self.season_object_dict.keys(), "Try to dump the wrong season:{}".format(season)
            season_obj = self.season_object_dict.get(str(season))
            season_obj.dump()

    def load(self, season=-1):
        """
        从json文件中读取内容，并进行实例化
        season = -1 : load all seasons
        season = 0 : load none seasons
        season = 1-n:  load specific season
        :return:
        """
        try:
            with open('./'+self.tv_name+'/'+self.tv_name+'.json', 'r', encoding='utf-8') as f:
                loaded_dict = json.load(f)
        except FileNotFoundError:
            print("No TV File, Stop load TV {}!".format(self.tv_name))
            return

        dict_todo = loaded_dict.get("season_object_dict")
        if season == -1:
            pass
        elif season == 0:
            pass
        else:
            assert str(season) in dict_todo.keys(), "Try to load wrong season:{} to tv object".format(season)
            season_obj = Season(self.tv_name, season, "")
            season_obj.load(season)
            dict_todo[str(season)] = season_obj

        print("LOAD TV json file", self.tv_name)
        self.__dict__.update(loaded_dict)

    def get_serializable_dict(self):
        return_dict = copy.deepcopy(self.__dict__)
        dict_todo = return_dict.get("season_object_dict")
        for key in dict_todo.keys():
            season_obj = dict_todo.get(key)
            dict_todo[key] = season_obj.season_url

        return return_dict

    def get_season_serializable_dict(self, season_num=-1):
        if season_num == -1:
            return_dict = copy.deepcopy(self.season_object_dict)
        else:
            return_dict = copy.deepcopy(self.season_object_dict.get(str(season_num)))

        for key in return_dict.keys():
            season_obj = return_dict.get(key)
            season_obj_dict = season_obj.get_serializable_dict()
            return_dict[key] = season_obj_dict
        return return_dict

    def backup_json(self):
        if os.path.exists('./' + self.tv_name + '/' + self.tv_name +'.json'):
            os.rename('./' + self.tv_name + '/' + self.tv_name+'.json', './' + self.tv_name+'/' + self.tv_name +
                      datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.json')
        else:
            print("OLD TV File NOT exist!!")
