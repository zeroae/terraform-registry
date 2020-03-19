FROM python:3.7-alpine

RUN apk add curl

ARG CHALICE_VERSION
VOLUME /opt/chalice
WORKDIR /opt/chalice
EXPOSE 8000
RUN pip install chalice==$CHALICE_VERSION

ENTRYPOINT [ "chalice", "--project-dir=/opt/chalice" ]
CMD ["local", "--host=0.0.0.0", "--stage=local"]

# Candidate for ON-BUILD
COPY requirements.txt .
RUN pip install -r requirements.txt
