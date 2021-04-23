sudo docker run -u root --restart on-failure -p 8080:8080 -p 50000:50000 -v jenkins_data:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -v $(which docker):/usr/bin/docker -v "$HOME":/home jenkins/jenkins:lts


