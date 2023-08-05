# encoding=utf8

import HttpUtils


class YibaiApiError(Exception):
    def __init__(self, code, message):
        super(YibaiApiError, self).__init__(message)
        self.code = code


class YibaiClient(object):
    def __init__(self, server_url, apikey):
        self.serverUrl = server_url
        self.apikey = apikey

    def sms_batch_submit(self, submits):
        return self.__execute({'submits': submits}, '/sms/batchSubmit')

    def sms_pull_status_report(self):
        return self.__execute({}, '/sms/pullStatusReport')

    def sms_pull_reply_message(self):
        return self.__execute({}, '/sms/pullReply')

    def user_info(self):
        return self.__execute({}, '/user/info')

    def __execute(self, request, url_path):
        request['apikey'] = self.apikey
        req_url = self.serverUrl + url_path
        res = HttpUtils.post_json(req_url, request)
        if res['code'] == 200:
            return res['response']
        raise YibaiApiError(res['code'], res['message'])
