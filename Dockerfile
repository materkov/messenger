FROM python:3.7.0-alpine3.8
RUN apk add --no-cache gcc musl-dev libffi-dev
RUN pip install pipenv
COPY . /app
WORKDIR /app
RUN pipenv install
EXPOSE 8000
CMD ["pipenv", "run", "gunicorn", "app:app"]
