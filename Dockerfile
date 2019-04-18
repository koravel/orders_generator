FROM python:3.7.2
COPY . .
RUN pip install -r ./requirements.txt
CMD "python3" "./Main.py"