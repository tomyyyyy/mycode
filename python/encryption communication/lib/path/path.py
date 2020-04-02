import sys,os

class path():
    """
        用来定位文件项目，
    """
    def __init__(self):
        pass

    path1 = sys.path[0]
    path2 = os.getcwd()
    path3 = os.path.abspath('.')
    path4 = os.path.dirname(os.path.abspath('.')) ## 获取相对目录



print(path().path1)
print(path().path2)
print(path().path3)
print(path().path4)
