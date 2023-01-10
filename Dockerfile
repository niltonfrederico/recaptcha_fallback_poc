FROM python:3.10-slim-bullseye

WORKDIR /app

# Creates an appuser and change the ownership of the application's folder
RUN useradd appuser \
    && chown appuser /app

COPY --chown=appuser . /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY --chown=appuser . /app

EXPOSE 3000