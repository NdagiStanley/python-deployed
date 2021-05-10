FROM python:3-onbuild

EXPOSE 5000

CMD gunicorn hello:app --log-file - --bind 0.0.0.0:5000
