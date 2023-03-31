# server-image-manipulation

## Install dependencies
Python packages needed are included in the requirements.txt file

## To Run: 
` python3 app.py `

## Endpoints

### Crop 
  http://127.0.0.1:5000/crop
  
  Parameters: 
    imageName : image from the folder || url : url to an image
    height : int (amount to crop from top and bottom; >=0)
    width : int (amount to crop from left and right; >=0)
  
  Can include parameters in URL : http://127.0.0.1:5000/crop?imageName=water.png&height=250&width=250
  
  Or as form data : http://127.0.0.1:5000/crop && {imageName: 'dog.jpg', height: 10, width: 20}
  
  Or : http://127.0.0.1:5000/hash && {url: http://www.myimagestorage.png, height: 10, width: 20}
  
### Hash
  http://127.0.0.1:5000/hash
  
  Parameters: 
    imageName : image from the folder || url : url to an image
    
  Can include parameters in URL : http://127.0.0.1:5000/hash?imageName=dog.jpg
  
  Or as form data : http://127.0.0.1:5000/hash && {imageName: 'dog.jpg'}
  
  Or : http://127.0.0.1:5000/hash && {url: http://www.myimagestorage.png}
  
  *url image input must be in form data
  
### Dif
  http://127.0.0.1:5000/dif
  
  Parameters: 
    imageName1 : image from the folder || url1 : url to an image
    imageName2 : image from the folder || url2 : url to an image
  
  Can include parameters in URL : http://127.0.0.1:5000/dif?imageName1=cat.jpg&imageName2=dog.jpg
  
  Or as form data : http://127.0.0.1:5000/dif && {imageName1: 'dog.jpg', imageName2: 'cat.jpg'}
  
  Or : http://127.0.0.1:5000/dif && {url1: http://www.myimagestorage.png, url2: http://www.myimagestorage2.png ;  }
  
  *url image input must be in form data
