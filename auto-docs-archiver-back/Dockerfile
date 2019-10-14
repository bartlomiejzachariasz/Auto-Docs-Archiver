FROM python:3.7
ENV PYTHONUNBUFFERED 1
COPY . /back
WORKDIR /back
RUN apt-get update && apt-get install -y tesseract-ocr
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "src.main:app", "-b", "0.0.0.0:8000"]