# Music-Recommendation-Using-Emotion-Detection-From-Facial-Expression
This Project uses emotion detected from facial expression to recommend music to users.

clone the repository
to install of the dependencies run 'pip install -r requirements.txt'

To access the weights download from 'https://drive.google.com/file/d/1bJG9w8Fw-eIIyh4uiQwih0G_Gtjq2z6V/view?usp=sharing'

copy the downloaded weights into this folder 'Music-Recommendation-Using-Emotion-Detection-From-Facial-Expression/trainer/weights/'

then run the following command on cmd prompt 'uvicorn app.main:app --reload' to start the uvicorn server

then copy the url into postman to get the response using a 'get' request
