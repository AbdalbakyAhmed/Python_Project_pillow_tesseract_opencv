import zipfile as zp
import math
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np
# from IPython.display import display

def display(image_to_show):
    image_to_show.show()

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

images = dict()
img_names = list()

def unzip (zip_file):
    with zp.ZipFile(str(zip_file),'r') as myzip:
        zip_objects = myzip.infolist()
        for x in zip_objects:
            images[x.filename] = [Image.open(myzip.open(x.filename))]
            img_names.append(x.filename)

# unzip('readonly/small_img.zip')
# print(images)
# print(img_names)
# display(images['a-0.png'])        

def main():
    unzip('small_img.zip')
    # unzip('readonly/images.zip')
    for name in img_names:
        img = images[name][0]
        # txt = pytesseract.image_to_string(images[name][0])
        txt = pytesseract.image_to_string(img)
        images[name].append(txt)
        
        # print(images['a-0.png'][1])
        print("Results found in file ",name)

        if "Christopher" in images[name][1]:
        # if "Mark" in images[name][1]:            
            img_cv = np.array(img)
            faces = face_cascade.detectMultiScale(img_cv,1.35)
            # faces = face_cascade.detectMultiScale(img_cv,1.25)
            print("Len of faces = "+str(len(faces)))
            if len(faces) > 0:
                boundings = faces.tolist()
                images[name].append(boundings) 
                #images {'img_name':[image_object][pytesseract_string][bounding_boxes]}

                face_img_boxes = list()
                for x,y,w,h in boundings:
                    face_img_boxes.append(img.crop((x, y, x+w, y+h)))

                h = math.ceil(len(face_img_boxes)/5)
                # print ("ceil height= "+str(h))
                contact_sheet = Image.new( img.mode, (500 ,100*h) )

                x = 0
                y = 0
                for face in face_img_boxes:
                    # Make this image into a thumbnail. This method modifies the image to contain 
                    # a thumbnail version of itself
                    # https://www.geeksforgeeks.org/python-pil-image-thumbnail-method/
                    # face.thumbnail((100,100))
                    face = face.resize((100,100))
                    contact_sheet.paste(face,(x,y))

                    if x + 100 == contact_sheet.width:
                        x = 0
                        y = y + 100
                    else:
                        x = x + 100

                display(contact_sheet)
            else :
                print('But there were no faces in that file!')  
        else:
            print('But there were no faces in that file!')  

if __name__ == '__main__':
  main()