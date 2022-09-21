import cv2

# open camera
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

# set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# take frame
ret, frame = cap.read()
# write frame to file
cv2.imwrite('camTestImage.jpg', frame)
# release camera
cap.release()

