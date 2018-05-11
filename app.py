import imageio
import os
import shutil
import img2pdf
import sys

path = './images'

# numbers of frames between detection and capture
# to avoid capturing at the beginning of a transition between slides
delayBetweenDetectAndCapture = 30

# delay between 2 frames changes (=detections)
# to avoid capture several frames during a transition between 2 slides
delayBetween2Detections = 50

def initDir():
    try:
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

def shouldDetectFrame(previousMean, currentMean, previousCapturedIndex, currentIndex):
    return ((previousMean != currentMean) and
        (previousCapturedIndex == 0 or
        previousCapturedIndex < currentIndex - delayBetween2Detections))

def captureFrame(im, slide, imageList):
    name = 'images/slide' + str(slide) + '.png'
    imageio.imwrite(name, im)
    imageList.append(name)

def saveAsPdf(imageList):
    outputPath = sys.argv[2] if (len(sys.argv) > 2 and len(sys.argv[2]) > 0) else "output.pdf"
    with open(outputPath, "wb") as f:
        f.write(img2pdf.convert(imageList))
    print('Output written to ', outputPath)



def main():
    previousMean = 0
    currentMean = 0
    slide = 0
    previousCapturedFrameIndex = 0
    imageList = []

    initDir()

    try:
        reader = imageio.get_reader(sys.argv[1])
    except:
        print("Could not read video from argument. Please specify the video path as first argument")
        sys.exit(1)

    for i, im in enumerate(reader):
        currentMean = int(im.mean())
        if shouldDetectFrame(previousMean, currentMean, previousCapturedFrameIndex, i):
            slide += 1
            previousCapturedFrameIndex = i
            nextFrameToCapture = i + delayBetweenDetectAndCapture
        if (i == nextFrameToCapture):
            captureFrame(im, slide, imageList)
            print("capture frame n°", i, " for slide n°", slide)
        previousMean = currentMean

    saveAsPdf(imageList)


if __name__ == "__main__":
    main()
