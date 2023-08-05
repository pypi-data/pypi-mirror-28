from .TV import TV
from .Season import Season
import operator


base_url = 'http://www.msj1.com/'




def crawl_tv(name, season=-1):
    """
    爬取所有的Season对应的每一集的下载链接
    :param name: 电视剧名字
    :param season: 电视剧第几季，如果不指定，就crawl所有的Season
    :return:
    """
    tv_obj = TV(name, base_url+r'?s='+name)
    if season == -1:
        tv_obj.generate_season_object_dict()
    else:
        tv_obj.generate_season_object(season)

    return tv_obj


def load_tv(name, season=-1):
    """
    从文件中载入一个电视剧的所有Season,或者是指定的Season(此时TV对象的season_object_dict只包含一个Season)
    :param name: 电视剧名字
    :param season:  电视剧第几季，如果不指定，就载入所有的Season
    :return:
    """
    tv_obj = TV(name, base_url + r'?s=' + name)
    tv_obj.load(season)

    dict_todo = tv_obj.season_object_dict
    for key in dict_todo.keys():
        season_obj = Season(tv_obj.tv_name, 0, "")
        season_obj.load(int(key))
        dict_todo[key] = season_obj

    return tv_obj


def dump_tv(name, season=-1):
    """
    dump电视剧所有Season，或者指定Season到json文件中
    :param name: 电视剧名字
    :param season:  电视剧第几季，如果不指定，就crawl所有的Season，然后dump
    :return:
    """
    tv_obj = crawl_tv(name, season)
    tv_obj.dump(season)

    for season in tv_obj.season_object_dict.values():
        season.dump()


def crawldump_tv(name, season=-1):
    """
    爬取TV的Season,并且和本地硬盘上读取创建的tv object对比，如果发现有不同，将crawl到的数据更新dump到本地，原本的文件重命名保存
    :param name: 电视剧名称
    :param season: 电视剧第几季，不指定(-1)的话，crawl所有的Season,load所有的Season，然后对比
    :return:
    """
    tv_obj_crawled = crawl_tv(name, season)
    tv_obj_loaded = load_tv(name, season)

    if season == -1:    # 只有在爬取整个tv信息的时候才需要考虑更新TV object的事情，只爬取某个season，TV Object不会改变
        if not operator.eq(tv_obj_crawled.get_serializable_dict(), tv_obj_loaded.get_serializable_dict()):
            print("TV {}'s content updated, dump it!!!".format(name))
            tv_obj_crawled.backup_json()
            tv_obj_crawled.dump(season)
        else:
            print("TV {}'s content is not changed, No dump!!!".format(name))

    if season == -1:
        for key in tv_obj_crawled.season_object_dict.keys():
            if tv_obj_loaded.season_object_dict.get(key) is None or\
               not operator.eq(tv_obj_crawled.season_object_dict.get(key).get_serializable_dict(),
                                    tv_obj_loaded.season_object_dict.get(key).get_serializable_dict()):
                print("TV {}'s Season {} updated, dump it!!!".format(name, key))
                tv_obj_crawled.season_object_dict.get(key).backup_json()
                tv_obj_crawled.season_object_dict.get(key).dump()
            else:
                print("TV {}'s Season {} is not changed, No dump!!!".format(name, key))
    else:
        if tv_obj_loaded.season_object_dict.get(str(season)) is None or \
                not operator.eq(tv_obj_crawled.season_object_dict.get(str(season)).get_serializable_dict(),
                           tv_obj_loaded.season_object_dict.get(str(season)).get_serializable_dict()):
            print("TV {}'s Season {} updated, dump it!!!".format(name, season))
            tv_obj_crawled.season_object_dict.get(str(season)).backup_json()
            tv_obj_crawled.season_object_dict.get(str(season)).dump()
        else:
            print("TV {}'s Season {} is not changed, No dump!!!".format(name, season))

def checkdump_tv(name, season=-1):
    """
    如果本地存在该TV目录，则跳过。如果没有，将它爬取并dump到本地
    :param name: 电视剧名称
    :param season: 电视剧第几季，不指定(-1)的话，check所有的Season,load所有的Season，然后对比
    :return:
    """
    tv_obj_loaded = load_tv(name, season)
    if len(tv_obj_loaded.season_object_dict) > 0:
        print("TV File exist, do NOT crawl, return")
    else:
        print("NO TV File exist, crawl&dump it")
        dump_tv(name, season)


def crawldump_tv_latest_season(name):
    tv_obj_loaded = load_tv(name, 0)        # not init season object
    crawldump_tv(name, int(tv_obj_loaded.latest_season))


if __name__ == "__main__":
#    dump_all_tv_in_list()
#    crawldump_all_tv_in_list()
#    checkdump_all_tv_in_list()
#    crawldump_tv('罪案终结', -1)
#    crawldump_all_tv_latest_season_in_list()
#    print_all_todo_episode()
    pass
