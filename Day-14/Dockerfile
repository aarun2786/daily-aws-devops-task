FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app-pvc.py .

CMD ["python","app-pvc.py"]
