import cv2
import datetime

cap = cv2.VideoCapture("piduan1.mp4")
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(3, 1920)
cap.set(4, 1440)

# 构建视频保存的对象
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')  # 为保存视频做准备，构建了一个对象，其中10为帧率，自己可按照需要修改
out = cv2.VideoWriter("outpianduan1.avi", fourcc, 24, (1920, 1440-80))

# print(cap.get(3))
# print(cap.get(4))
n = 0
min = 23
second = 55
while cap.isOpened():
    ret, frame = cap.read()
    n += 1
    if ret == True:
        frame = frame[80:1440, 0:1920]
        print(frame.shape)
        font = cv2.FONT_HERSHEY_SIMPLEX
        datet = str("06-21-2022  00:")
        if n % 24 == 0:
            if second <= 59:
                second += 1
            if second == 60:
                min += 1
                second = 0
        if second >= 10:
            datet = datet + str(min) + ":" + str(second)
        else:
            datet = datet + str(min) + ":" + "0" + str(second)
        frame = cv2.putText(frame, datet, (40, 60), font, 1.2,
                            (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)  # 显示视频
        out.write(frame)  # 保存视频
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
