import cv2

def capture_still():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()
    if ret:
        # Save the captured frame to disk
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured and saved as 'captured_image.jpg'")
    else:
        print("Error: Could not capture an image.")

    # Release the camera
    cap.release()

def stream_live_feed():
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # Display the resulting frame
        cv2.imshow('Live Feed', frame)

        # Break the loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# First, capture a still image
capture_still()
# Then, stream the live feed (comment out the above line if you only want the live feed)
stream_live_feed()
