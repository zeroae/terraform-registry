FROM python:3.7

VOLUME /opt/chalice

ARG CHALICE_VERSION
RUN pip install chalice==$CHALICE_VERSION

EXPOSE 8000
ENTRYPOINT ["chalice", "--project-dir=/opt/chalice"]
CMD ["local", "--host=0.0.0.0", "--port=8000", "--stage=local"]

COPY requirements.txt .
RUN pip install -r requirements.txt


