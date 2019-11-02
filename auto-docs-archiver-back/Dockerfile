FROM python:3.7
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /back/requirements.txt
WORKDIR /back
RUN pip install -r requirements.txt
COPY . /back
WORKDIR /back
RUN apt-get update && apt-get install -y tesseract-ocr
EXPOSE 8000
CMD ["gunicorn", "src.main:app", "-b", "0.0.0.0:8000"]