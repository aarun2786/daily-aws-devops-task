FROM python

WORKDIR /app

COPY requirments.txt .

RUN pip install -r requirments.txt


COPY app.py .


CMD ["python","app.py"]
