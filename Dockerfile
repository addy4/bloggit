FROM python:3.8-slim
COPY . app/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
WORKDIR app/
CMD ["python", "run.py"]