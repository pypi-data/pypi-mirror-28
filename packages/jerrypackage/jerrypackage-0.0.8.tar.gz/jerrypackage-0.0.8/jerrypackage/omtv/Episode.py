
class Episode:
    """
    未定义什么成员函数，仅仅是用来保存一下有关这个episode的信息，如：
    episode_num： 第几集
    episode_name: 爬到的链接是用什么名字来保存这一集的
    episode_size: 文件大小（str类型)
    episode_download_url：   下载链接，注意这是一个列表，就算是同一个文件，有不同的下载链接，例如ed2k, magnet, 网盘链接等等
    """
    episode_num = ''
    episode_name = ''
    episode_size = ''
    episode_download_url = []

    def __init__(self, name, num, size, url):
        self.episode_name = name
        self.episode_num = num
        self.episode_size = size
        self.episode_download_url = url
