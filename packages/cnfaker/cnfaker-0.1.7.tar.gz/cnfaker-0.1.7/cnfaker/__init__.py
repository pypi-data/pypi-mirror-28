import linecache
import random
from os import path
# from distutils.sysconfig import get_python_lib
#
#
# _resource_path = get_python_lib() + '/cnfaker/'
# _name_file = _resource_path + 'resource/name.txt'
# _email_file = _resource_path + 'resource/email.txt'
# _IDcard_file = _resource_path + 'resource/IDcard.txt'
# _phone_file = _resource_path + 'resource/phone.txt'
# _username_file = _resource_path + 'resource/username.txt'
# _address_file = _resource_path + 'resource/address.txt'
# _sentence_file = 'resource/sentence.txt'
DATA_DIR = path.abspath(path.join(path.dirname(__file__), 'resource'))

_name_file = path.join(DATA_DIR, 'name.txt')
_email_file = path.join(DATA_DIR, 'email.txt')
_IDcard_file = path.join(DATA_DIR, 'IDcard.txt')
_phone_file = path.join(DATA_DIR, 'phone.txt')
_username_file = path.join(DATA_DIR, 'username.txt')
_address_file = path.join(DATA_DIR, 'address.txt')
_sentence_file = path.join(DATA_DIR, 'sentence.txt')


def _make_gen(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024*1024)


def _rawpycount(filename):
    f = open(filename, 'rb')
    f_gen = _make_gen(f.raw.read)
    return sum( buf.count(b'\n') for buf in f_gen )


def _getfile(filename, num=1):
    linenum = _rawpycount(filename)
    result = set()
    while len(result)<num:
        tmp = linecache.getline(filename, random.randrange(1, linenum, 1)).strip()
        result.add(tmp)
    return result


def name(num=1):
    return _getfile(_name_file, num=num)


def email(num=1):
    return _getfile(_email_file, num=num)


def ID(num=1):
    return _getfile(_IDcard_file, num=num)


def phone(num=1):
    return _getfile(_phone_file, num=num)


def username(num=1):
    return _getfile(_username_file, num=num)


def address(num=1):
    return _getfile(_address_file, num=num)


def sentence(num=1):
    return _getfile(_sentence_file, num=num)


def pargraph(num=1):
    result = set()
    while len(result) < num:
        tmp = sentence(random.randint(2,10))
        tmp = ''.join(list(tmp))
        result.add(tmp)
    return result



