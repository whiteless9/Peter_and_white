import os

from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time  # 可以忽视这个 Time 报错（运行程序还是没问题的）
import time
import glob


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

def formatTime(atime):
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(atime))

if __name__ == '__main__':
    # 需要自己配置
    # cTime = "2019-12-13 21:51:02"  # 创建时间
    # mTime = "2019-02-02 00:01:03"  # 修改时间
    # aTime = "2019-02-02 00:01:04"  # 访问时间
    cTime = "2022-06-21 "  # 创建时间
    mTime = "2022-06-21 "  # 修改时间
    aTime = "2022-06-21 "  # 访问时间

    fName = r"C:\Users\lenovo\Desktop\K19150_0072\021441839_K19150_0072_2_05.jpg"  # 文件路径，文件存在才能成功（可以写绝对路径，也可以写相对路径）
    for root, dirs, files in os.walk(r"D:\projects\ModifyFileTime\file\3"):
        for dir in dirs:
            # WSI_MASK_PATH = r"C:\Users\lenovo\Desktop\K19150_0072"
            if dir =="Thumb":
                break
            WSI_MASK_PATH = os.path.join(root,dir)
            print(WSI_MASK_PATH)

            paths = glob.glob(os.path.join(WSI_MASK_PATH, '*.jpg'))
            paths.sort()
            for fName in paths:
                print(fName)
                a = fName.split("\\")
                # print(a[7][0:2],a[7][2:4] ,a[7][4:6])

                # print("最后一次访问时间:", formatTime(os.stat(fName).st_atime))
                # print("最后一次修改时间:", formatTime(os.stat(fName).st_mtime))
                # print("最后一次状态变化的时间：", formatTime(os.stat(fName).st_ctime))
                #
                # timeStr = formatTime(os.stat(fName).st_mtime)[11:]
                # # timeStr = timeStr
                # print(timeStr)
                timeStr = str(a[7][0:2]+":"+a[7][2:4]+":"+a[7][4:6])
                cTime = cTime + timeStr
                mTime = mTime + timeStr
                aTime = aTime + timeStr

                print("修改后时间",aTime)
                offset = (0, 0, 2)  # 偏移的秒数（不知道干啥的）
                # 调用函数修改文件创建时间，并判断是否修改成功
                r = modifyFileTime(fName, cTime, mTime, aTime, offset)
                if r == 0:
                    print(fName + ' 修改完成')
                elif r == 1:
                    print('修改失败')
                cTime = "2022-06-21 "  # 创建时间
                mTime = "2022-06-21 "  # 修改时间
                aTime = "2022-06-21 "  # 访问时间