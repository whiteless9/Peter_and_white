import glob
import os
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time  # 可以忽视这个 Time 报错（运行程序还是没问题的）
import time


def modifyFileTime(filePath, createTime, modifyTime, accessTime, offset):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param createTime: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    try:
        format = "%Y-%m-%d %H:%M:%S"  # 时间格式
        cTime_t = timeOffsetAndStruct(createTime, format, offset[0])
        mTime_t = timeOffsetAndStruct(modifyTime, format, offset[1])
        aTime_t = timeOffsetAndStruct(accessTime, format, offset[2])

        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)

        createTimes = Time(time.mktime(cTime_t))
        accessTimes = Time(time.mktime(aTime_t))
        modifyTimes = Time(time.mktime(mTime_t))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)
        return 0
    except:
        return 1


def timeOffsetAndStruct(times, format, offset):
    return time.localtime(time.mktime(time.strptime(times, format)) + offset)


if __name__ == '__main__':
    # 需要自己配置
    cTime = "2022-06-21 01:25:07"  # 创建时间
    # mTime = "2022-06-21 00:23:54"  # 修改时间
    # aTime = "2022-06-21 00:23:54"  # 访问时间
    aTime = mTime = cTime
    fName = r"D:\projects\ModifyFileTime\file\4\几何参数数据,人工测量数据\202203122250_海南环岛高铁西段_下行_海口_东方.hhgk"
    # 文件路径，文件存在才能成功（可以写绝对路径，也可以写相对路径）
    # fName = r"D:\projects\ModifyFileTime\file\2\4C图片分析软件截图.jpg"  # 文件路径，文件存在才能成功（可以写绝对路径，也可以写相对路径）
    # for root, dirs, files in os.walk(r"D:\projects\ModifyFileTime\file\2"):
    #     for fName in files:
    #         fName = os.path.join(root, fName)
    print(fName)
    offset = (0, 1, 2)  # 修改时间访问时间与创建时间偏移的秒数
    # 调用函数修改文件创建时间，并判断是否修改成功
    r = modifyFileTime(fName, cTime, mTime, aTime, offset)
    if r == 0:
        print('修改完成')
    elif r == 1:
        print('修改失败')