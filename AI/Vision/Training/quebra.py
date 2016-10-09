import cv2

name = 1
cont = 0

cap = cv2.VideoCapture('/home/fei/Videos/teste.webm')

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    if cont%25 == 0:
        cv2.imwrite('frame%03d.png'%name,frame)
        name += 1
    
    frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
    cv2.imshow('Video', frame)
    cont += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
