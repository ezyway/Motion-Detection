# Motion Detection Project

2 Seperate Codes are there for this Project. "Motion Detection/motion_detect.py" will ping on telegram and shows a GUI for the Cam feed with the motion rectangles. "Motion Detection and Stream/web_stream.py" is the main script. Running it will ping a link on telegram which will point to the flask server running on localhost.


#### Before you run

##### For "Motion Detection" code
- download and configure [telegram_send](https://pypi.org/project/telegram-send/)

##### For "Motion Detection and Stream" code
- download and configure [telegram_send](https://pypi.org/project/telegram-send/)
- download pyngrok {pip install pyngrok} and add auth token {ngrok authtoken token-from-the-ngrok-dashboard}
