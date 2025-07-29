In this project I am  going to make a school mangement sytem which will run on local host computer as well as in other devices connected to LAN.

you must have **Python 3.9+** make virtual env in backend folder

```cd backend
python -m venv venv
pip install -r req.txt
```
activate the enviroment (In windows) using this 
``` ./venv/Scripts/activate
``` 
or 
```
source ./venv/Scripts/activate
```

Now run the server

```
uvicorn main:app --reload
```
In browser go to
```
http://127.0.0.1/docs
```
it will use the Swagger UI for fast api you can test you api through here
