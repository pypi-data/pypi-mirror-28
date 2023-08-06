from PIL import Image
import face_recognition

''' 找到所有图片'''
def find_all(filename=''):
    if not filename:
        return -1
    image = face_recognition.load_image_file(filename)
    face_locations = face_recognition.face_locations(image)
    print("在照片中发现{}张人脸".format(len(face_locations)))
    faces = []
    for face_location in face_locations:
        top, right, bottom, left = face_location
        # 指定人脸的位置信息，然后显示人脸图片
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        # pil_image.show()
        faces.append(pil_image)
    return faces

'''识别图像中的所有人脸,并截取出人脸显示'''
def face_recognition_all(filename=''):
    if not filename:
        return -1
    image = face_recognition.load_image_file(filename)
    face_locations = face_recognition.face_locations(image)
    print("在照片中发现{}张人脸".format(len(face_locations)))
    for face_location in face_locations:
        top, right, bottom, left = face_location
        # 指定人脸的位置信息，然后显示人脸图片
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()


def main():
    face_recognition_all('1.jpg')

if __name__ == '__main__':
    main()
