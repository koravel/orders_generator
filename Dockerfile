FROM python:3.7.2
COPY . .
RUN pip install -r ./requirements.txt
RUN python3 ./Main.py
EXPOSE 3306
EXPOSE 5762
EXPOSE 15762