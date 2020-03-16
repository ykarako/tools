import cv2

cap = cv2.VideoCapture(4)

dictionary_name = cv2.aruco.DICT_4X4_50
dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)

while True:
    ret, frame = cap.read()

    # スクリーンショットを撮りたい関係で1/3サイズに縮小
    # frame = cv2.resize(frame, (int(frame.shape[1]/3), int(frame.shape[0]/3)))

    # ArUcoの処理
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary)
    frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # 加工済の画像を表示する
    cv2.imshow('Edited Frame', frame)

    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
