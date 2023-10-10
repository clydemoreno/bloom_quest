docker build -t my-python-app:latest . 
docker run -p 8080:8080 my-python-app:latest -d 

curl http://localhost:8080