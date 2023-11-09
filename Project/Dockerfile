FROM python:3.10

WORKDIR /appfolder

COPY . .

RUN python3 -mpip install -r/appfolder/requirements.txt

EXPOSE 5000

CMD ["python","/appfolder/app.py"]