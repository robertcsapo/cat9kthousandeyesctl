FROM python:3.9-slim
WORKDIR /script/
COPY ./ ./
RUN pip3 install .
ENTRYPOINT ["cat9kthousandeyesctl"]