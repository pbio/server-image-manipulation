from flask import Flask, request, Response, send_from_directory
import numpy as np
from PIL import Image
import hashlib, os, urllib.request

errors = [
    {"message": "No Error", 'status': 200}, #0
    {"message": "Error: Must Provide an imageName or url in parameters", "status":400}, #1
    {"message": "Error: Image name can not be empty", "status":400}, #2
    {"message": "Error: File does not exist", "status":400}, #3
    {"message": "Error: Attempting to crop an area larger than the image", "status": 400}, #4
    {"message": "Error: Crop value must be a positive number or 0", "status": 400}, #5
    {"message": "Error: Crop value must be an integer value", "status": 400}, #6
]


app = Flask(__name__)

def getImage(request, index=''):
    error = 0
    imageName = None
    if not request.form.get("imageName"+index) and not request.args.get("imageName"+index) and not request.form.get('url'+index):
        img = None
        error = 1
    
    elif request.form.get('url'+index):
        imageUrl = request.form.get('url'+index)
        urllib.request.urlretrieve(imageUrl, "new.png")
        img = Image.open("new.png")
        
    elif request.form.get("imageName"+index) or request.args.get("imageName"+index):
        imageName = request.form.get("imageName"+index) or request.args.get("imageName"+index)
        imageUrl = "images/" + imageName
        if not imageName: 
            error = 2
            return None, imageName, error

        if not os.path.isfile(imageUrl): 
            error = 3
            return None, imageName, error
        
        img = Image.open(imageUrl)

    return img, imageName, error



@app.route("/crop", methods=["POST", "GET"])
def crop():
    # input is one image and a height and width to crop from the edges of the image
    # create a new array with the desired dimensions
    # copy all the pixel values from original image to the new array
    # convert array to image and return
    cropHeight = request.form.get("height") or request.args.get("height")
    cropWidth = request.form.get("width") or request.args.get("width")
    if not cropHeight.isdigit() or not cropWidth.isdigit(): return Response(errors[6]["message"], status=errors[6]["status"])
    cropHeight = int(cropHeight)
    cropWidth = int(cropWidth)
    if cropHeight < 0 or cropWidth < 0: return Response(errors[5]["message"], status=errors[5]["status"])

    originalImage, imageName, errorIndex = getImage(request)
    if errorIndex: return Response(errors[errorIndex]["message"], status=errors[errorIndex]["status"])

    originalImage = np.array(originalImage)
    depth = originalImage.shape[2]
    height = originalImage.shape[0]
    width = originalImage.shape[1]
    if height < cropHeight*2 or width < cropWidth*2: return Response(errors[4]["message"], status=errors[4]["status"])
    newImage = np.zeros([height-2*cropHeight, width-2*cropWidth, depth], dtype=np.uint8)
    for i in range(cropHeight, height-cropHeight):
        for j in range(cropWidth, width-cropWidth):
            newImage[i-cropHeight,j-cropWidth] = originalImage[i,j]   
    outputImage = Image.fromarray(newImage)
    outputImage.save("images/cropped/" + imageName)

    return send_from_directory('images/cropped', imageName, as_attachment=False)

@app.route("/hash", methods=["POST", "GET"])
def calc_hash():
    # input is one image
    # convert to array with numpy, then flatten
    # calculate hash 
    # return hash

    originalImage, imageName, errorIndex = getImage(request)
    if errorIndex: return Response(errors[errorIndex]["message"], status=errors[errorIndex]["status"])
    newImage = np.array(originalImage)
    newImage = newImage.flatten()
    newImage = newImage.tobytes() 
    hash = hashlib.sha256(newImage).hexdigest()
    return hash

@app.route("/dif", methods=["POST", "GET"])
def calc_dif():
    # input will be 2 images of the same size
    # check that the size is equal; return an error if not equal
    # convert to array
    # subtract arrays
    # convert result back to an image
    # return image

    img1, imageName1, errorIndex1 = getImage(request, "1")
    img2, imageName2, errorIndex2 = getImage(request, "2")
    if errorIndex1 or errorIndex2: return Response(errors[errorIndex1 or errorIndex2]["message"], status=errors[errorIndex1 or errorIndex2]["status"])

    if img1.format != img2.format: return Response("The images are not the same formats: "+ img1.format + " and "+ img2.format , status=200)
    img1 = np.array(img1)
    img2 = np.array(img2)
    outputShape = img1.shape

    #Are the images the same size?
    if img1.shape[0] != img2.shape[0] or img1.shape[1] != img2.shape[1]: return Response("The images are not the same size", status=200)

    #Do they have the same number of channels? 
    if img1.shape[2]:
        if img1.shape[2] != img2.shape[2]: return Response("The images do not have the same number of channels", status=200)
    img1 = img1.flatten()
    img2 = img2.flatten()
    outputImage = img1 - img2

    #Are the images identical? could check hash as well
    imgAreIdentical = True
    for i in outputImage: 
        if i!=0: imgAreIdentical = False
        break
    if imgAreIdentical: return Response("The images are identical", status=200)

    #Return score
    sum = 0
    for i in outputImage: 
        if i<26 and i>-26: sum += 1
    score = sum/len(outputImage)*100
    print(len(outputImage))
    print(sum)
    return Response("Similarity score: " + str(round(score)) + "%", status=200)

    #Images are not identical, return the dif of the images
    # outputImage = outputImage.reshape(outputShape) # get the shape from image1
    # outputImage = Image.fromarray(outputImage)
    # outputImageDir = "images/dif/" 
    # outputImageName = imageName1.rsplit('.')[0] + '_' + imageName2
    # outputImage.save(outputImageDir + outputImageName)
    # return send_from_directory(outputImageDir, outputImageName, as_attachment=False)



if __name__ == '__main__':
    app.run(debug=True)