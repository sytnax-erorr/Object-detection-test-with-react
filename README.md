# Object-detection-test-with-react

**URLs**:

1. App URL - **https://aspiringcvengineer.xyz:8000** **(Tensorflow.js + React.js - Custmized the code only to detect 3 Classes)**

2. APP URL - **https://aspiringcvengineer.xyz/** **(React app + used APIs for detection (full development))**
 
3. API URL - **https://api.aspiringcvengineer.xyz:5000** **( Falsk + custom trained model for prediction (full development))**

	*In 2nd React App we are hitting the apis on an avg every 4-7 sec, so there is little delay in the detected screen.*

	*All URLs will require permission to access the Camera*


**Folder Structure**:

*Backend* -> Contains everything related to model training (ex: Generating more training data &
		Annotation of images, tf record generation, etc )

*Frontend* -> React application for frontend  and  its all related files

*ssnv* -> Few screenshots and demo videos ( *Both* Mobile & Laptop)



**Model Selected  - “ssd_mobilenet_v2”**

**Reasons**: Since our primary focus was to detect the objects on real time (web cam), so we needed higher speed then accuracy.

**Config file** : Full model pipeline config file is present in the directory /Model/pipeline.config



**Approach For Backend:**

Step 1: Since model training requires lots of data but we had only a few hundreds So we generated more training data by augmenting the existing one.

Step 2: Generation of csv(for bounding boxes) & tf record files. Beauces model training takes data in special format (byte data which is ultimately  faster in compare to old techniques) 

Step 3: Used transfer learning and trained the model further with custom training data for custom object detections.

Step 4: Created a flask application and used the already trained model (Step 3) for detection ( Goal - to create APIs)



**Approach for Frontend:**

Step 1: Create a react application and get the ssl certification to access the camera + ssl for the APIs(Backend) ( Due to CORS policy)

Step 2: Capturing image from camera sending it to server and getting predictions (in JSON form)

Step 3: Drawing the boxes on clients end for detected boxes

Step 4: Also manage the number of requests, sends to the server at a time, to prevent app cracking. 



**Area to improve:**

1. Since training data was too small to train, the accuracy is not too much high at this time( because most of training data was very simple and plain in background but for detecting with other objects (ex: real data with noise) we need more data sets )

3. Front end applications can be built more in React way(more component wise) but due to time issue, i went with more general way. 

4. We can also reduce the time delay by compressing the data before sending it to the server. Will improve the performance.

5. In mobiles when users switch the camera from front to rear, images get flipped and boxes get distorted a little bit. We can also improve that.



**Reason for low accuracy:**

1. Accuracy was much higher in Jupyter notebook(for given test images - (not exactly overfitting)), reason for low here is, Here input images having lots of noise in background as compared to the training images. 

2. Size variation in image & canvas, when drawing boxes at clients end.

3. Few training images.

