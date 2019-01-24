FROM mcr.microsoft.com/aiforearth/base-py:latest

RUN apt-get update && apt-get -y install sudo \
    && apt-get install -y cifs-utils \
    && apt-get install -y azcopy

RUN echo "source activate ai4e_py_api" >> ~/.bashrc \
    && conda install -c conda-forge -n ai4e_py_api numpy pandas xarray netCDF4

# Note: supervisor.conf reflects the location and name of your api code.
# If the default (./my_api/runserver.py) is renamed, you must change supervisor.conf
# Copy your API code
COPY ./GSP_API /app/GSP_API/
COPY ./supervisord.conf /etc/supervisord.conf
# startup.sh is a helper script
COPY ./startup.sh /
RUN chmod +x /startup.sh

# Copy file connection information
COPY ./file_mount.json /app/fuse/file_mount.json

COPY ./file_mounter.py /app/fuse/file_mounter.py
RUN chmod +x /app/fuse/file_mounter.py

COPY ./LocalForwarder.config /lf/

#RUN mkdir -p /mnt/output

#RUN mount -t cifs //globalfloodsdiag360.file.core.windows.net/output /mnt/output -o vers=3.0,username=globalfloodsdiag360,password=+c7Ecmc7QVJxnuFUshZJg9YZZfBl8CBa8Qi6dMmTGPQgDh9K0ptGtZ69CkeU1rbnBFzXzWNJa+RVqwHUIc9XQg==,dir_mode=0777,file_mode=0777,sec=ntlmssp

# Application Insights keys and trace configuration
ENV APPINSIGHTS_INSTRUMENTATIONKEY= \
    APPINSIGHTS_LIVEMETRICSSTREAMAUTHENTICATIONAPIKEY= \
    LOCALAPPDATA=/app_insights_data \
    OCAGENT_TRACE_EXPORTER_ENDPOINT=localhost:55678

# The following variables will allow you to filter logs in AppInsights
ENV SERVICE_OWNER=AI4E_GSP_Example \
    SERVICE_CLUSTER=Local\ Docker \
    SERVICE_MODEL_NAME=GSP-sample \
    SERVICE_MODEL_FRAMEWORK=Python \
    SERVICE_MODEL_FRAMEOWRK_VERSION=3.6.6 \
    SERVICE_MODEL_VERSION=1.0

ENV API_PREFIX=/v1/global_streamflow_prediction/get_streamflow

ENV CUSTOM_VISION_PREDICTION_KEY= \
    CUSTOM_VISION_PROJECT_ID= \
    CUSTOM_VISION_ITERATION_ID=

# Expose the port that is to be used when calling your API
EXPOSE 80
HEALTHCHECK --interval=1m --timeout=3s --start-period=20s \
  CMD curl -f http://localhost/ || exit 1
ENTRYPOINT [ "/startup.sh" ]
