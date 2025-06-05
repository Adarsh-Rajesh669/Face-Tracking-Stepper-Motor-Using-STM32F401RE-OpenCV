import cv2
import serial


ser = serial.Serial('COM6', 9600)  

# Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)  # Open webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip camera 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    frame_center = frame.shape[1] // 2
    face_pos = "CENTER"

    for (x, y, w, h) in faces:
        cx = x + w // 2
        if cx < frame_center - 50:
            face_pos = "LEFT"
        elif cx > frame_center + 50:
            face_pos = "RIGHT"
        else:
            face_pos = "CENTER"

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        break

    ser.write(face_pos.encode())

    cv2.putText(frame, f"Face: {face_pos}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
