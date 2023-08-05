import cv2
import sys


def face_detect(filename=''):
    if not filename:
        return -1
    # Get user supplied values
    # imagePath = sys.argv[1]
    imagePath = filename
    cascPath = "../data/haarcascade_frontalface_default.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Faces found", image)
    cv2.waitKey(0)

def living_detect():
    cap = cv2.VideoCapture(0)

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    while(True):
    	# Capture frame-by-frame
    	ret, frame = cap.read()

    	# Our operations on the frame come here
    	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    	# Detect faces in the image
    	faces = faceCascade.detectMultiScale(
    		gray,
    		scaleFactor=1.1,
    		minNeighbors=5,
    		minSize=(30, 30),
    	)

    	print("Found {0} faces!".format(len(faces)))

    	# Draw a rectangle around the faces
    	for (x, y, w, h) in faces:
    		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


    	# Display the resulting frame
    	cv2.imshow('frame', frame)
    	if cv2.waitKey(1) & 0xFF == ord('q'):
    		break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def main():
    # face_detect('../1.jpg')
    living_detect()

if __name__ == '__main__':
    main()
