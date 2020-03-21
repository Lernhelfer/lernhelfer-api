sudo docker run -d \
--env-file ./credentials.env \
-p 5000:5000 \
--name lernhelfer_container lernhelfer:latest