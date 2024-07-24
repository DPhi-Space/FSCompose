FROM python:3.9-slim

WORKDIR /app

COPY ./serial-test.py /app/

RUN pip install pyserial

CMD ["python3","-u", "serial-test.py"]