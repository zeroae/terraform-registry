FROM continuumio/miniconda3:4.8.2-alpine AS management

VOLUME /opt/chalice
WORKDIR /opt/chalice

COPY environment.yml .
RUN /opt/conda/bin/conda env create -n chalice && \
    /opt/conda/bin/conda clean --all --yes && \
    /opt/conda/bin/conda remove -n chalice liquidprompt && \
    sed -i 's/activate base/activate chalice/' /home/anaconda/.profile
