import requests
import requests.cookies
import os
import pickle
import logging
import time
import hashlib
import base64
import re
import json


# Example:
# dl = xzb_api.XZBDownloader('13817130417', 'chenhy123', './xzb_cookie',
#                            verification_code_reader=verification_code.default_verification_code_reader('tesseract1', './vcode.jpg'))


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'


logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

sh = logging.StreamHandler()
sh.setLevel(logging.NOTSET)
sh.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s]: %(message)s'))
logger.addHandler(sh)


def current_timestamp():
    return int(time.time() * 1000)

def current_random():
    from random import randint
    return '%s%06d.%s' % (current_timestamp(), randint(0, 999999), randint(100000000, 9999999999))

def remove_bom(response):
    if response.startswith('\xef\xbb\xbf'):
        response = response[3:]
    return response

def get_response_info(response, jsonp):
    response = remove_bom(response)
    m = re.search(r'%s\((.+)\)' % jsonp, response)
    assert m, 'invalid jsonp response: %s' % response
    # logger.debug('get_response_info:')
    # logger.debug(response)
    parameter = m.group(1)
    # m = re.match(r"^\{process:(-?\d+),msg:'(.*)'\}$", parameter)
    # if m:
    #     return {'process': int(m.group(1)), 'msg': m.group(2)}
    return json.loads(parameter)

def str_filesize(size):
    '''
    author: limodou
    >>> print str_filesize(0)
    0
    >>> print str_filesize(1023)
    1023
    >>> print str_filesize(1024)
    1K
    >>> print str_filesize(1024*2)
    2K
    >>> print str_filesize(1024**2-1)
    1023K
    >>> print str_filesize(1024**2)
    1M
    '''
    import bisect
    d = [(1024 - 1, 'K'), (1024 ** 2 - 1, 'M'), (1024 ** 3 - 1, 'G'), (1024 ** 4 - 1, 'T')]
    s = [x[0] for x in d]
    index = bisect.bisect_left(s, size) - 1
    if index == -1:
        return str(size)
    else:
        b, u = d[index]
    return str(size / (b + 1)) + u


class XZBDownloader():

    def __init__(self, username=None, password=None, cookie_path=None, login=True, verification_code_reader=None):
        self.username = username
        self.password = password
        self.cookie_path = cookie_path
        self.session = None
        self.verification_code_reader = verification_code_reader
        self.login_time = None
        self.session = requests.Session()

        self.session.headers.update({'User-Agent':USER_AGENT})
        self.load_cookies()

        if login:
            self.id = self.get_userid_or_none()
            if not self.id:
                self.login()
            self.id = self.get_userid()

            self.init_peer()

    ################################################################################################################

    def url_content(self, url, data=None):
        try:
            logger.debug(self.session.cookies)
            if data:
                content = self.session.post(url, data=data).content
            else:
                content = self.session.get(url).content
            return content
        except Exception as e:
            logger.debug(e)

    ################################################################################################################

    def get_userid_or_none(self):
        return self.get_cookie('.xunlei.com', 'userid')

    def gen_jsonp_function_name(self):
        return 'jQuery{}_{}'.format(id(self), current_timestamp())

    def get_userid(self):
        if self.has_cookie('.xunlei.com', 'userid'):
            return self.get_cookie('.xunlei.com', 'userid')
        else:
            raise Exception('Probably login failed')

    ################################################################################################################

    def save_cookies(self):
        if not os.path.isdir(os.path.dirname(self.cookie_path)):
            return False

        with open(self.cookie_path,'wb') as f:
            f.truncate()

            pickle.dump(self.session.cookies._cookies, f)
            #pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies),f)

    def load_cookies(self):
        if not os.path.isfile(self.cookie_path):
            return False

        with open(self.cookie_path, 'rb') as f:
            cookies = pickle.load(f)

            jar = requests.cookies.RequestsCookieJar()
            jar._cookies = cookies
            self.session.cookies = jar

            #cookies = requests.utils.cookiejar_from_dict(pickle.load(f))        # RequestsCookieJar 类型
            #self.session.cookies = cookies

    def has_cookie(self, domain, k):
        return domain in self.session.cookies._cookies and k in self.session.cookies._cookies[domain]['/']

    def get_cookie(self, domain, k):
        if self.has_cookie(domain, k):
            return self.session.cookies._cookies[domain]['/'][k].value
        else:
            return None

    def set_cookie(self, domain, k, v):
        c = requests.cookies.RequestsCookieJar()
        c.set(k, v, path='/',domain=domain)
        self.session.cookies.update(c)

    def del_cookie(self, domain, k):
        if self.has_cookie(domain, k):
            self.session.cookies.clear(domain=domain, path="/", name=k)


    ################################################################################################################

    def login(self):

        logger.info('login')

        if not self.has_cookie('.xunlei.com', 'deviceid'):
            # 先拿到计算daviceid的算法
            url1 = 'https://login.xunlei.com/risk?cmd=algorithm&t='+str(current_timestamp())
            sign_fun = self.url_content(url1).decode()
            import js2py
            xl_al = js2py.eval_js(sign_fun)

            SB = USER_AGENT + "###zh-cn###24###960x1440###-540###true###true###true###undefined###undefined###x86###Win32#########"\
                    + hashlib.md5(str(int(time.time() * 1000)).encode()).hexdigest().lower()
            xl_fp_raw = base64.b64encode(SB.encode()).decode()
            xl_fp = hashlib.md5(xl_fp_raw.encode()).hexdigest().lower()
            xl_al = js2py.eval_js(sign_fun)
            xl_fp_sign = xl_al(xl_fp_raw)

            # 计算好参数的值POST过去，返回的cookie里面会带有相关信息
            device_data = {'xl_fp_raw': xl_fp_raw, 'xl_fp': xl_fp, 'xl_fp_sign':xl_fp_sign}
            url2 = 'http://login.xunlei.com/risk?cmd=report'
            self.url_content(url2, data=device_data)


            url3 = 'https://login.xunlei.com/sec2login/?csrf_token={}'.format(hashlib.md5(self.get_cookie('.xunlei.com', 'deviceid')[:32].encode()).hexdigest())
            formdata = {
                'u': self.username,
                'p': self.password,
                'cachetime': str(current_timestamp()),
                'appid': '113',     # 很奇怪这两个值是为什么？ 估计是之前的script里面做过要求， 值可以随便设置
                'v': '101',
            }
            self.url_content(url3, data=formdata)

            url4 = 'http://verify1.xunlei.com/image?t=MVA&cachetime=%s' % current_timestamp()
            image = self.url_content(url4)

            verification_code = self.verification_code_reader(image)

            url5 = 'https://login.xunlei.com/sec2login/?csrf_token={}'.format(hashlib.md5(self.get_cookie('.xunlei.com', 'deviceid')[:32].encode()).hexdigest())
            formdata.update({'verifycode':verification_code})
            self.url_content(url5, data=formdata)

            logger.info('save cookie')
            self.save_cookies()
            self.login_time = time.time()

    def logout(self):
        logger.info('logout')
        session_id = self.get_cookie('.xunlei.com', 'sessionid')
        if not session_id:
            return
        url = 'http://login.xunlei.com/unregister?sessionid={}'.format(session_id)
        self.url_content(url)
        ckeys = ["sessionid", "usrname", "nickname", "usernewno", "userid"]
        for k in ckeys:
            self.set_cookie('.xunlei.com', k, '')
        self.save_cookies()
        self.login_time = None

    def is_session_timeout(self, htmlcontent):
        logger.info('is_session_timeout?')
        logger.debug('html: {}'.format(htmlcontent))
        # timeout warning 1:
        # jQuery4444817808_1480233929775({"msg": "user not login", "rtn": 1004})
        timeout_test = r'(not login)|("rtn": 1004)'
        if re.search(timeout_test, htmlcontent):
            return True

        maybe_timeout = htmlcontent == '''rebuild({"rtcode":-1,"list":[]})'''
        if maybe_timeout:
            if self.login_time and time.time() - self.login_time > 60 * 10:  # 10 minutes
                return True

        return False

    ################################################################################################################

    def init_peer(self):
        logger.info('list_peer')

        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/listPeer?type=0&v=2&ct=0&callback={}&_={}'.format(callback, current_timestamp())
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
            logger.info(resp)
        except AssertionError as e:
            msg = 'response is not jsonp when list_peer'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        result = []
        if resp.get('rtn') == 0:
            result = resp.get('peerList')
            self.cached_peer_list = result

        peers = self.cached_peer_list
        self.selected_peer_id = peers[0].get('pid')
        self.set_cookie('config.com', 'selected_peer_id', self.selected_peer_id)
        self.save_cookies()

        # check the peer still online
        if not peers[0].get('online') in [1, '1']:
            raise Exception('The selected downloader is offline')

        self.selected_peer_name = peers[0].get('name')

        # login the peer
        drive_list = self.login_peer(self.selected_peer_id)
        if not drive_list:
            raise Exception('Error when login the downloader')
        self.peer_drives = drive_list
        logger.debug('peer drives: {!s}'.format(drive_list))

        # get the peer's settings and save its default target dir
        setting = self.get_peer_setting(self.selected_peer_id)
        if not setting:
            raise Exception('Error when retrieving the setting of the downloader')

        self.default_target_dir = setting.get('defaultPath')


    def login_peer(self, pid):
        """
        :param pid:
        :return: drive list of this peer - ["C", "D", ...]
        """
        logger.info('login_peer')

        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/login?pid={}&clientType=&v=2&ct=0&callback={}&_={}'.format(pid, callback, current_timestamp())
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
            logger.info(resp)
        except AssertionError as e:
            msg = 'response is not jsonp when login_peer'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        result = []
        if resp.get('rtn') == 0:
            result = [x[0] for x in resp.get('pathList')]

        return result

    def get_peer_setting(self, pid):
        logger.info('get_peer_setting: {}'.format(pid))

        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/settings?pid={}&v=2&ct=0&callback={}&_={}'.format(
            pid, callback, current_timestamp()
        )
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
            logger.info(resp)
        except AssertionError as e:
            msg = 'response is not jsonp when get_peer_setting'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        result = {}
        if resp.get('rtn') == 0:
            result = resp

        return result

    ################################################################################################################

    def resolve_url(self, url):
        logger.info('resolve_url')

        callback = self.gen_jsonp_function_name()
        payload = dict(url=url)
        payload = dict(json=json.dumps(payload))
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/urlResolve?pid={}&v=2&ct=0&callback={}'.format(
            self.selected_peer_id, callback
        )

        resp = self.url_content(url, data=payload).decode()
        try:
            resp = get_response_info(resp, callback)
        except AssertionError as e:
            msg = 'response is not jsonp when resolve_url'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        result = dict(url="", infohash="", size=0, name="")
        if resp.get('rtn') == 0 and 'taskInfo' in resp:
            result['infohash'] = resp.get('infohash', '')
            result['url'] = resp.get('taskInfo').get('url')
            result['size'] = resp.get('taskInfo').get('size')
            result['name'] = resp.get('taskInfo').get('name')

        return result

    def list_downloading(self, start=0, len=100):
        logger.info('list_downloading')

        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/list?pid={}&type=0&pos={}&number={}&needUrl=1&v=2&ct=0&callback={}&_={}'.format(
            self.selected_peer_id, start, len, callback, current_timestamp()
        )
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
            logger.info(resp)
        except AssertionError as e:
            msg = 'response is not jsonp when list_downloading'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        result = []
        if resp.get('rtn') == 0:
            result = resp.get('tasks')

        return result

    def list_finished(self, start=0, len=100):
        logger.info('list_finished')

        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/list?pid={}&type=1&pos={}&number={}&needUrl=1&v=2&ct=0&callback={}&_={}'.format(
            self.selected_peer_id, start, len, callback, current_timestamp()
        )
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
            logger.info(resp)
        except AssertionError as e:
            msg = 'response is not jsonp when list_finished'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        result = []
        if resp.get('rtn') == 0:
            result = resp.get('tasks')

        return result

    def list_trash(self, start=0, len=100):
        logger.info('list_trash')

        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/list?pid={}&type=2&pos={}&number={}&needUrl=1&v=2&ct=0&callback={}&_={}'.format(
            self.selected_peer_id, start, len, callback, current_timestamp()
        )
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
        except AssertionError as e:
            msg = 'response is not jsonp when list_trash'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        result = []
        if resp.get('rtn') == 0:
            result = resp.get('tasks')

        return result

    def get_free_space_of_downloader(self, pid=None):
        logger.info('get_free_space_of_downloader')

        if not pid:
            pid = self.selected_peer_id
        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/boxSpace?pid={}&v=2&ct=0&callback={}&_={}'.format(
            pid, callback, current_timestamp()
        )
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
        except AssertionError as e:
            msg = 'response is not jsonp when get_free_space_of_downloader'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        result = []
        if resp.get('rtn') == 0:
            result = resp.get('space')
            def filter(x):
                x['remain'] = str_filesize(int(x['remain']))
                return x
            result = [filter(x) for x in result]

        return result

    ################################################################################################################

    def create_task(self, url, path_index=None):
        logger.info('create_task')

        #resolve the url first
        url_info = self.resolve_url(url)
        size = url_info.get('size')
        if size == 0:
            raise Exception('Invalid URL provided')
        hash = url_info.get('infohash')
        name = url_info.get('name')
        url = url_info.get('url')

        #get the target dir
        target_path = self.default_target_dir
#        if path_index != None:
#            if path_index >= len(self.user_define_target_dirs):
#                raise Exception('path_index out of range')
#            target_path = self.user_define_target_dirs[path_index]

        callback = self.gen_jsonp_function_name()
        if hash:
            payload = dict(path=target_path, infohash=hash, name=name, btSub=[1])
            payload = dict(json=json.dumps(payload))
            url = 'http://homecloud.remote.xiazaibao.xunlei.com/createBtTask?pid={}&v=2&ct=0&callback={}'.format(
                self.selected_peer_id, callback
            )
            resp = self.url_content(url, data=payload).decode()
            try:
                resp = get_response_info(resp, callback)
            except AssertionError as e:
                msg = 'response is not jsonp when create_task'
                logger.warning(msg)
                logger.debug(resp)
                raise Exception(msg)

            if resp.get('rtn') == 202:
                raise Exception('Already downloading/downloaded')

            return resp.get('rtn') == 0
        else:
            task = dict(url=url, name=name, gcid="", cid="", filesize=size, ext_json={"autoname":1})
            payload = dict(path=target_path, tasks=[task])
            payload = dict(json=json.dumps(payload))
            url = 'http://homecloud.remote.xiazaibao.xunlei.com/createTask?pid={}&v=2&ct=0&callback={}'.format(
                self.selected_peer_id, callback
            )
            resp = self.url_content(url, data=payload).decode()
            try:
                resp = get_response_info(resp, callback)
            except AssertionError as e:
                msg = 'response is not jsonp when create_task'
                logger.warning(msg)
                logger.debug(resp)
                raise Exception(msg)

            if resp.get('tasks')[0].get('result') == 202:
                raise Exception('Already downloading/downloaded')

            if resp.get('rtn') == 0 and resp.get('tasks')[0].get('result') == 0:
                return resp.get('tasks')[0].get('name')
            else:
                return None

    def trash_task(self, task_id, task_state, permanently_del=False):
        """
        delete the task, but still in the trash, and the file is not deleted too, you can restore it with web gui.
        if permanently_del=True, the task can not be restored with any chance.
        :param task_id:
        :param task_state:
        :return:
        """
        logger.info('trash_task')

        param_task = '{}_{}'.format(task_id, task_state)
        recycle = 1
        delete_file = 'false'
        if permanently_del:
            recycle = 0
            delete_file = 'true'
        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/del?pid={}&tasks={}&recycleTask={}&deleteFile={}&v=2&ct=0&callback={}&_={}'.format(
            self.selected_peer_id, param_task, recycle, delete_file, callback, current_timestamp()
        )
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
        except AssertionError as e:
            msg = 'response is not jsonp when trash_task'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        return resp.get('rtn') == 0


    def pause_task(self, task_id, task_state):
        logger.info('pause_task')

        param_task = '{}_{}'.format(task_id, task_state)
        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/pause?pid={}&tasks={}&v=2&ct=0&callback={}&_={}'.format(
            self.selected_peer_id, param_task, callback, current_timestamp()
        )
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
        except AssertionError as e:
            msg = 'response is not jsonp when pause_task'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        return resp.get('rtn') == 0 and resp.get('tasks')[0].get('result') == 0


    def resume_task(self, task_id, task_state):
        logger.info('resume_task')

        param_task = '{}_{}'.format(task_id, task_state)
        callback = self.gen_jsonp_function_name()
        url = 'http://homecloud.remote.xiazaibao.xunlei.com/start?pid={}&tasks={}&v=2&ct=0&callback={}&_={}'.format(
            self.selected_peer_id, param_task, callback, current_timestamp()
        )
        resp = self.url_content(url).decode()
        try:
            resp = get_response_info(resp, callback)
        except AssertionError as e:
            msg = 'response is not jsonp when start_task'
            logger.warning(msg)
            logger.debug(resp)
            raise Exception(msg)

        return resp.get('rtn') == 0 and resp.get('tasks')[0].get('result') == 0

    ################################################################################################################

