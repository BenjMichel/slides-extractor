import imageio
import os
import shutil

path = './images'
reader = imageio.get_reader('./video.mp4')

# numbers of frames between detection and capture
# to avoid capturing at the beginning of a transition between slides
delayBetweenDetectAndCapture = 30

# delay between 2 frames changes (=detections)
# to avoid capture several frames during a transition between 2 slides
delayBetween2Detections = 50

def initDir():
    try:
        # os.rmdir(path)
        shutil.rmtree(path)
    except OSError as e:
        print(e);
        print("Deletion of the directory %s failed" % path)
    else:
        print("Successfully deleted the directory %s" % path)
    try:
        os.mkdir(path)
    except OSError as e:
        print(e);
        print("Creation of the directory %s failed" % path)
        raise Exception()
    else:
        print("Successfully created the directory %s " % path)


previousMean = 0
currentMean = 0
slide = 0
previousCapturedFrameIndex = 0

def shouldDetectFrame(previousMean, currentMean, previousCapturedIndex, currentIndex):
    return ((previousMean != currentMean) and
        (previousCapturedIndex == 0 or
        previousCapturedIndex < currentIndex - delayBetween2Detections))

def captureFrame(i, slide):
    name = 'images/slide' + str(slide) + '.png'
    imageio.imwrite(name, im)
    print('slide', slide)

initDir()

for i, im in enumerate(reader):
    currentMean = int(im.mean())
    # print('Mean of frame %i is %1.1f' % (i, currentMean))
    if shouldDetectFrame(previousMean, currentMean, previousCapturedFrameIndex, i):
        slide += 1
        previousCapturedFrameIndex = i
        nextFrameToCapture = i + delayBetweenDetectAndCapture
        # print('previousCapturedFrameIndex', previousCapturedFrameIndex)
    if (i == nextFrameToCapture):
        print("capture", i)
        captureFrame(i, slide)
    previousMean = currentMean
