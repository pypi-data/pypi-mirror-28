import sys
sys.path.append('..')
import jardb.compose
from jardb.util import *

def test_check_string():
    assert check_string('import os') == 'False'
    assert check_string('from os import *') == 'False'
    assert check_string('$data == 5') == "ob.find('data') == 5"

def test_convert_set():
    _list = []
    for i in range(0,11):
        _list.append(jardb.compose.DbRecord({'data':i}))
    assert convert_set(_list,'data') == set(range(0,11))
    assert convert_set(_list,'id') == {None}

def test_check_attr():
    assert check_attr([]) == False
    assert check_attr({}) == True
    assert check_attr({'id':[]}) == True
    assert check_attr({'id':'123'}) == False
    assert check_attr({'id':['NotNull','Unique'],'data':['AutoIncrease']}) == True
    assert check_attr({'id':['NotNull','Unique'],'data':['Not In Data']}) == False


def test_cache():
    _list = []
    for i in range(0,11):
        _list.append(jardb.compose.DbRecord({'data':i}))
    cache = Cache()
    assert cache.increase('data','data',_list) == 11
    assert cache.increase('data','data',_list) == 12
    assert cache.increase('data','id',_list) == 1
    assert cache.increase('data','id',_list) == 2
    assert cache.check_unique('data','data',_list,8) == True
    assert cache.check_unique('data','data',_list,11) == False
    cache.remove_label('data','data',[1,2,3,4,5])
    cache.remove_label('data','data',6)
    assert cache.check_unique('data','data',_list,5) == False
    assert cache.check_unique('data','data',_list,6) == False

if __name__ == '__main__':
    test_check_string()
    test_convert_set()
    test_check_attr()
    test_cache()