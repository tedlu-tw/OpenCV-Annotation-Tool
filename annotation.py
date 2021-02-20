import cv2
import sys
import glob

debug = 1
obj_list = []
obj_count = 0
click_count = 0
x1 = 0
y1 = 0
h = 0
w = 0
key = None
frame = None

def obj_marker(event, x, y, flags, param):
    global click_count
    global debug
    global obj_list
    global obj_count
    global x1
    global y1
    global w
    global h
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:
        click_count += 1
        if click_count % 2 == 1:
            x1 = x
            y1 = y
        else:
            w = abs(x1 - x)
            h = abs(y1 - y)
            obj_count += 1
            if x1 > x:
                x1 = x
            if y1 > y:
                y1 = y
            obj_list.append("%d %d %d %d " %(x1, y1, w, h))
            if debug > 0:
                print(obj_list)
            cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (255, 0, 0), 1)
            cv2.imshow("frame", frame)


if len(sys.argv) != 3:
    print('Usage: python marker.py /path/to/location output_filename.txt')
else:
    if debug > 0:
        print("Arguments are ok")
        print("Path: %s" %sys.argv[1])
        print("Output file: %s" %sys.argv[2])
        print("Click on edges you want to mark as an object")
        print("Press q to quit")
        print("Press c to cancel markings")
        print("Press n to load next image")
    list = glob.glob("%s/*.bmp" %sys.argv[1])
    if debug > 0:
        print(list)
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("frame", obj_marker)
    file_name = open(sys.argv[2], "w")
    for i in list:
        frame = cv2.imread(i)
        cv2.imshow("frame", frame)
        obj_count = 0
        key = cv2.waitKey(0)
        while (key & 0xFF != ord("q")) and (key & 0xFF != ord("n")):
            key = cv2.waitKey(0)
            if key & 0xFF == ord("c"):
                obj_count = 0
                obj_list = []
                frame = cv2.imread(i)
                cv2.imshow("frame", frame)
        if key & 0xFF == ord("q"):
            break
        elif key & 0xFF == ord("n"):
            if obj_count > 0:
                str1 = "%s %d " %(i, obj_count)
                file_name.write(str1)
                for j in obj_list:
                    file_name.write(j)
                file_name.write("\n")
                obj_count = 0
                obj_list = []
    file_name.close()
cv2.destroyAllWindows()
