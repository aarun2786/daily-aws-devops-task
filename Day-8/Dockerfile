FROM python

WORKDIR /app

COPY requirement.txt .

RUN pip install -r  requirement.txt

COPY app.py .

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]
