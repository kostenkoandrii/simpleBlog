
### To run project you need to clone repository - simpleBlog
### install docker from official website
```
https://docs.docker.com/get-docker/
```

### go to the simpleBlog repository to build and run docker at port:5000
```
docker build -t nameimage ./
docker run -p5000:5000 nameimage
```

### go to the simpleBlogFront repository to build and run second docker at port:8080
```
docker build -t nameimage ./
docker run -p8080:8080 nameimage
```

