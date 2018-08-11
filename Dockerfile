FROM python:3.7.0-alpine3.8
EXPOSE 8000
WORKDIR /app
COPY . /app
RUN apk add --no-cache gcc musl-dev libffi-dev && \
  pip install pipenv && \
  pipenv install
CMD ["pipenv", "run", "gunicorn", "app:app"]
