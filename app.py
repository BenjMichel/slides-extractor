import imageio
import os

path = './images'

def initDir():
    try:
        os.rmdir(path)
    except OSError:
        print ("Deletion of the directory %s failed" % path)
    else:
        print ("Successfully deleted the directory %s" % path)
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

reader = imageio.get_reader('./video.mp4')
previousMean = 0
currentMean = 0
slide = 0
previousCapturedFrameIndex = 0

def shouldCaptureFrame(previousMean, currentMean, previousCapturedIndex, currentIndex):
    return (previousMean != currentMean) and (previousCapturedIndex == 0 or previousCapturedIndex < currentIndex - 10)

def captureFrame(i, slide):
    name = 'images/slide' + str(slide) + '.png'
    imageio.imwrite(name, im)
    print('slide')

initDir()

for i, im in enumerate(reader):
    currentMean = int(im.mean())
    print('Mean of frame %i is %1.1f' % (i, currentMean))
    # print(previousMean, currentMean, previousMean != currentMean)
    if shouldCaptureFrame(previousMean, currentMean, previousCapturedFrameIndex, i):
        captureFrame(i, slide)
        slide += 1
        previousCapturedFrameIndex = i
        print('previousCapturedFrameIndex', previousCapturedFrameIndex)
    previousMean = currentMean
