gunicorn -w 3 -t 120 --bind 0.0.0.0:9020 equiback:app
