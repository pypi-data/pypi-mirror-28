"""
@Author: Nan Huijuan
@Date:   2017-11-16T14:13:19+08:00
"""
import json


class Error:
    def __init__(self, code, msg, status_code=400):
        self.code = code
        self.msg = msg
        self.status_code = status_code

    def get(self):
        return {
            'errCode': self.code,
            'msg': self.msg
        }

    def to_string(self):
        return json.dumps(self.get(), ensure_ascii=False, indent=4)


unauthorized = Error('1000', 'user unauthorized', 401)
invalid_parameter = Error('1001', 'parameter invalid')
not_found = Error('1002', 'resource not found', 404)
database_error = Error('1003', 'database error')
json_parse_error = Error('1004', 'invalid json value')
retry_later_error = Error('1005', 'retry later', 417)

unknown_error = Error('9999', 'unknown error')


def system_error_maker(msg, status_code):
    return Error('9000', msg, status_code)
