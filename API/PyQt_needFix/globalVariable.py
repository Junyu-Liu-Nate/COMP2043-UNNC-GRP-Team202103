# 全局变量管理模块

def _init():
    '''在主模块初始化'''
    global GLOBALS_DICT
    GLOBALS_DICT = {}

def set(name, value):
    '''设置'''
    GLOBALS_DICT[name] = value
    print("set successful", name, " = ", value)


def get(name):
    '''取值'''
    try:
        return GLOBALS_DICT[name]
    except KeyError:
        return "Not Found"