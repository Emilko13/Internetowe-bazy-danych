FROM python:3.14-slim
RUN mkdir /app
WORKDIR /app
COPY app/requirements.txt /app
RUN python3 -m pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python","simulator.py"]
