# Use build layer
FROM python:3.10-alpine as builder
ENV POETRY_HOME=/opt/poetry

RUN if [ -z "${PYTHON_DOCKER_IMAGE##*alpine*}" ]; then \
  echo "Installing required packages for alpine image"; \
  apk update; \
  apk add gcc musl-dev python3-dev libffi-dev openssl-dev curl; \
  else \
  echo "Skipping installation of required packages for alpine image"; \
  fi

# Install poetry
RUN pip3 install --no-cache-dir --upgrade pip 
RUN curl -sSL https://install.python-poetry.org | python3 -

# Use runtime layer
FROM python:3.10-alpine

# Disable creation of virtual environments to reduce image size
ENV POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME=/opt/poetry \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on 

# Copy poetry into image
COPY --from=builder /opt/poetry /opt/poetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN pip3 install --no-cache-dir --upgrade pip
RUN poetry install

COPY ./cefies /app/cefies
CMD ["fastapi", "run", "cefies/app.py", "--port", "80"]