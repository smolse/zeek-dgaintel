FROM python:3.11-slim as base

ARG ZEEK_VERSION=v5.2.2

# Install necessary deb packages
RUN  apt-get update && apt-get install -y \
  build-essential \
  cmake \
  git \
  libssl-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Python bindings for Zeek Broker from source code
RUN git clone https://github.com/zeek/zeek.git && \
  cd zeek && \
  git checkout ${ZEEK_VERSION} && \
  git submodule update --init --recursive auxil/broker && \
  cd auxil/broker && \
  ./configure && \
  make && \
  make install && \
  cd ../../.. && \
  rm -r zeek

WORKDIR /app

FROM base as build

ARG POETRY_VERSION=1.5.1

ENV PYTHONDONTWRITEBYTECODE 1 \
  PYTHONUNBUFFERED 1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_CACHE_DIR=1

RUN pip install poetry==${POETRY_VERSION}

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
  poetry install --only=main --no-root

COPY zeek_dgaintel ./zeek_dgaintel

FROM build as test

COPY mypy.ini .pylintrc .coveragerc ./
COPY tests ./tests

ENV PYTHONPATH="$PYTHONPATH:/usr/local/lib/python3.11/site-packages"
RUN . .venv/bin/activate && \
  poetry install --with=dev && \
  poetry run mypy zeek_dgaintel && \
  poetry run pylint zeek_dgaintel && \
  poetry run coverage run -m pytest && poetry run coverage report -m

FROM base as final

COPY --from=build /app/.venv .venv
COPY --from=build /app/zeek_dgaintel ./zeek_dgaintel
COPY docker-entrypoint.sh ./
RUN chmod +x ./docker-entrypoint.sh

# Disable debug messages from TensorFlow
ENV TF_CPP_MIN_LOG_LEVEL=2

ENTRYPOINT [ "./docker-entrypoint.sh" ]
