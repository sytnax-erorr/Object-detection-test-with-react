# Object-detection-test-with-react

**Note**:
	We are hitting the apis on an avg every 5 sec, so there is little delay in the detected screen.


**Points**:
1. App URL - **https://aspiringcvengineer.xyz/**
2. Accessible from everywhere (ex: Laptop, mobile,etc ) & will ask permission to access the camera of the device.


**Folder Structure**:
	*Backend* -> Contains everything related to model training (ex: Generating more training data &
			Annotation of images, tf record generation, etc )
	*Frontend* -> React application for frontend  and all its related files
	*ssnv* -> Few screenshots and demo videos


**Model Selected  - “ssd_mobilenet_v2”**
**Reasons**: Since our primary focus was to detect the objects on real time (web cam),  so we needed higher speed with little compromise with accuracy.
*Config file* : Full model pipeline config file is present in the directory /Model/pipeline.config


**Approach For Backend:**

Step 1: Since model training requires lots of data but we had only a few hundreds So we generated more training data by augmenting the existing one.

Step 2: Generation of csv(for bounding boxes) & tf record files. Beauces model training takes data in special format (byte data which is ultimately  faster in compare to old techniques) 

Step 3: Used transfer learning and further training of model for custom object detections.
Step 4: Created flask application and used the already trained model for detection ( Goal - to create APIs)


**Approach for Frontend:**

Step 1: Create a react application and get the ssl certification to access the camera + ssl for APIs to ( Due to CORS policy)

Step 2: Capturing image from camera sending it to server and getting predictions

Step 3: Drawing the boxes on client end for detected boxes

Step 4: Also managing the number of request to send to the server at a time



**Area to improve:**
1. Since training data was too small to train, the accuracy is not too much high at this time( because most of training data was very simple and plain in background but for detecting with other objects(real data with noise) we need more data sets )
2. Front end applications can be built more in React way(more component wise) but due to time issue, i went with the easy way. 
3. We can also reduce the time delay by compressing the data before sending it to the server. Will improve the performance.
4. In mobiles when users switch the camera from front to rear, images get flipped and boxes get distorted a little bit. We can also improve that.



