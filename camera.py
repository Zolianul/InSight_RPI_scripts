import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
import pyrebase
import firebase_admimn
from firebase_admin import credentials,storage

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
ds_factor = 0.6

config={
             "apiKey":"AIzaSyCwCUxOKRQIMJOsFY2PL1KYONv1wujsxoM",
             "authDomain":"insight-4b54a.firebaseapp.com",
             "databaseURL":"https://insight-4b54a-default-rtdb.firebaseio.com",
             "projectId":"insight-4b54a",
             "storageBucket":"insight-4b54a.com",
             "serviceAccount":"serviceAccountKey.json"}

firebase_admin = pyrebase.initialize_app(config)
storage = firebase_admin.storage()
database = firebase_admin.database()


known_person = []  
known_image = []  
known_face_encodings = []


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


for file in os.listdir("profiles"):
    try:
        
        known_person.append(file.replace(".jpg", ""))
        file = os.path.join("profiles", file)
        known_image = face_recognition.load_image_file(file)
        known_face_encodings.append(face_recognition.face_encodings(known_image)[0])
    
    
    except Exception as e:
        pass

class VideoCamera(object):
    def __init__(self, email, password):
       
        self.video = cv2.VideoCapture(0)
        self.email = email
        self.password = password
        self.userID = auth.sign_in_with_email_and_password(self.email, self.password)
        
    def __del__(self):
        
        self.video.release()
 
    def get_frame(self):
        global last_upload_time
        global last_update_profiles
        success, image = self.video.read()
        if not success:
            return None  
 
        try:
            small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)  
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])  
 
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
 
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
 
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_person[best_match_index]
 
                face_names.append(name)
                
                
                if (name == "Unknown") and ((datetime.now() - last_upload_time) > timedelta(seconds=30) ):
                    self.upload_to_firebase(image)
                    last_upload_time = datetime.now()
                
              
                if((datetime.now() - last_update_profiles) > timedelta(seconds = 300) ):
                    firebase_path="UserUploads/"+userID['idToken']+"/ProfilesUploaded/"
                    local_path="profiles"
                    
                   
                    for file in os.listdir(local_path):
                        file_path=os.path.join(local_path,file)
                        if os.path.isfile(file_path)
                            os.unlink(file_path)
                    
                    bucket = storage.bucket()
                    blobs= bucket.list_blobs(prefix= firebase_path)
                    for blob in blobs:
                        filename=os.path.basename(blob.name)
                        local_file_path = os.path.join(local_path,filename)
                        blob.download_to_filename(local_file_path)
                        print("Updated Profiles")
                    last_update_profiles=datetime.now()
                    
                    
                    
         
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(image, (left, top), (right, bottom), (255, 255, 255), 2)
                cv2.rectangle(image, (left, bottom - 35), (right, bottom), (255, 255, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, name, (left + 6, bottom - 6), font, 0.5, (0, 0, 0), 1)
        except Exception as e:
            print(f"Error processing frame: {e}")  
 
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    
    def take_picture(self):
        success,image= self.video.read()
        if success:
            self.upload_to_firebase(image)
    
    def upload_to_firebase(self,image):
        ret, imggg = cv.imencode(',jpg', image)
        today_date = datetime.now().strftime("%m%d%Y-%H%M%S") 
        photo_name=str(today_date + ".jpg")
        cv2.imwrite(photo_name, imggg)
        storage.child(photo_name).put(photo_name)
        uploaded_url=storage.child(photo_name).get_url(None)
        image_metadata={
            "name":photo_name,
            "url":uploaded_url}
        database.child("UserUploads/"+userID['idToken']+"/RPI").push(image_metadata)