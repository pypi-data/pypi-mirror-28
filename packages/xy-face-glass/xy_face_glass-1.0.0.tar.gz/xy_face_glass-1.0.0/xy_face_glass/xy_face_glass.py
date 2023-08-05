import dlib
from PIL import Image, ImageDraw, ImageFont
import argparse

from imutils import face_utils, translate, rotate, resize
from imutils.video import VideoStream
import numpy as np

import moviepy.editor as mpy

import cv2




def generate_gif(filename=''):
    '''生成GIF图，传入的图像必须有人脸'''
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-image", required=True, help="path to input image")
    # args = parser.parse_args()
    if not filename:
        return -1
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68.dat')

    # resize to a max_width to keep gif size small
    max_width = 500

    # open our image, convert to rgba
    # img = Image.open(args.image).convert('RGBA')
    img = Image.open(filename).convert('RGBA')

    # two images we'll need, glasses and deal with it text
    deal = Image.open("deals.png")
    text = Image.open('text.png')

    if img.size[0] > max_width:
        scaled_height = int(max_width * img.size[1] / img.size[0])
        img.thumbnail((max_width, scaled_height))

    img_gray = np.array(img.convert('L')) # need grayscale for dlib face detection

    rects = detector(img_gray, 0)

    if len(rects) == 0:
        print("No faces found, exiting.")
        exit()

    print("%i faces found in source image. processing into gif now." % len(rects))

    faces = []

    for rect in rects:
        face = {}
        print(rect.top(), rect.right(), rect.bottom(), rect.left())
        shades_width = rect.right() - rect.left()

        # predictor used to detect orientation in place where current face is
        shape = predictor(img_gray, rect)
        shape = face_utils.shape_to_np(shape)

        # grab the outlines of each eye from the input image
        leftEye = shape[36:42]
        rightEye = shape[42:48]

        # compute the center of mass for each eye
        leftEyeCenter = leftEye.mean(axis=0).astype("int")
        rightEyeCenter = rightEye.mean(axis=0).astype("int")

    	# compute the angle between the eye centroids
        dY = leftEyeCenter[1] - rightEyeCenter[1]
        dX = leftEyeCenter[0] - rightEyeCenter[0]
        angle = np.rad2deg(np.arctan2(dY, dX))

        # resize glasses to fit face width
        current_deal = deal.resize((shades_width, int(shades_width * deal.size[1] / deal.size[0])),
                                   resample=Image.LANCZOS)
        # rotate and flip to fit eye centers
        current_deal = current_deal.rotate(angle, expand=True)
        current_deal = current_deal.transpose(Image.FLIP_TOP_BOTTOM)

        # add the scaled image to a list, shift the final position to the
        # left of the leftmost eye
        face['glasses_image'] = current_deal
        left_eye_x = leftEye[0,0] - shades_width // 4
        left_eye_y = leftEye[0,1] - shades_width // 6
        face['final_pos'] = (left_eye_x, left_eye_y)
        faces.append(face)

    # how long our gif should be
    duration = 4

    def make_frame(t):
        draw_img = img.convert('RGBA') # returns copy of original image

        if t == 0: # no glasses first image
            return np.asarray(draw_img)

        for face in faces:
            if t <= duration - 2:
                current_x = int(face['final_pos'][0])
                current_y = int(face['final_pos'][1] * t / (duration - 2))
                draw_img.paste(face['glasses_image'], (current_x, current_y) , face['glasses_image'])
            else:
                draw_img.paste(face['glasses_image'], face['final_pos'], face['glasses_image'])
                draw_img.paste(text, (75, draw_img.height // 2 - 32), text)

        return np.asarray(draw_img)

    animation = mpy.VideoClip(make_frame, duration=duration)
    animation.write_gif(filename + ".gif", fps=4)


def video_realtime():
    '''视频实时添加效果，按字母d添加,q退出'''
    vs = VideoStream().start()

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68.dat')

    max_width = 500
    frame = vs.read()
    frame = resize(frame, width=max_width)

    fps = vs.stream.get(cv2.CAP_PROP_FPS) # need this for animating proper duration

    animation_length = fps * 5
    current_animation = 0
    glasses_on = fps * 3

    # uncomment for fullscreen, remember 'q' to quit
    # cv2.namedWindow('deal generator', cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty('deal generator', cv2.WND_PROP_FULLSCREEN,
    #                          cv2.WINDOW_FULLSCREEN)

    deal = Image.open("deals.png")
    text = Image.open('text.png')

    dealing = False

    while True:
        frame = vs.read()

        frame = resize(frame, width=max_width)

        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = []

        rects = detector(img_gray, 0)
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        for rect in rects:
            face = {}
            shades_width = rect.right() - rect.left()

            # predictor used to detect orientation in place where current face is
            shape = predictor(img_gray, rect)
            shape = face_utils.shape_to_np(shape)

            # grab the outlines of each eye from the input image
            leftEye = shape[36:42]
            rightEye = shape[42:48]

            # compute the center of mass for each eye
            leftEyeCenter = leftEye.mean(axis=0).astype("int")
            rightEyeCenter = rightEye.mean(axis=0).astype("int")

    	    # compute the angle between the eye centroids
            dY = leftEyeCenter[1] - rightEyeCenter[1]
            dX = leftEyeCenter[0] - rightEyeCenter[0]
            angle = np.rad2deg(np.arctan2(dY, dX))

            current_deal = deal.resize((shades_width, int(shades_width * deal.size[1] / deal.size[0])),
                                   resample=Image.LANCZOS)
            current_deal = current_deal.rotate(angle, expand=True)
            current_deal = current_deal.transpose(Image.FLIP_TOP_BOTTOM)

            face['glasses_image'] = current_deal
            left_eye_x = leftEye[0,0] - shades_width // 4
            left_eye_y = leftEye[0,1] - shades_width // 6
            face['final_pos'] = (left_eye_x, left_eye_y)

            # I got lazy, didn't want to bother with transparent pngs in opencv
            # this is probably slower than it should be
            if dealing:
                if current_animation < glasses_on:
                    current_y = int(current_animation / glasses_on * left_eye_y)
                    img.paste(current_deal, (left_eye_x, current_y), current_deal)
                else:
                    img.paste(current_deal, (left_eye_x, left_eye_y), current_deal)
                    img.paste(text, (75, img.height // 2 - 32), text)

        if dealing:
            current_animation += 1
            # uncomment below to save pngs for creating gifs, videos
            # img.save("images/%05d.png" % current_animation)
            if current_animation > animation_length:
                dealing = False
                current_animation = 0
            else:
                frame = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

        cv2.imshow("deal generator", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        if key == ord("d"):
            dealing = not dealing

    cv2.destroyAllWindows()
    vs.stop()

def main():
    generate_gif('1.jpg')
    video_realtime()
if __name__ == '__main__':
    main()
