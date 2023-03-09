##########
### STEP 1
##########
FROM python:3.11.2-slim-buster as base

# Setup env
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV RUNNING_AS_DOCKER=true

##########
### STEP 2
##########
FROM base AS python-env

COPY Pipfile .

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget gcc python3-dev \
    && wget http://pki.coyote.com/trust/zscaler.cer -O /usr/local/share/ca-certificates/zscaler.crt \
    && chmod 644 /usr/local/share/ca-certificates/zscaler.crt \
    && update-ca-certificates \
    && pip install pipenv \
    && PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --skip-lock

##########
### STEP 3
##########
FROM base

# Copy virtual env from python-env stage
COPY --from=python-env /.venv /.venv
COPY --from=python-env /usr/local/share/ca-certificates/zscaler.crt /usr/local/share/ca-certificates/zscaler.crt
ENV PATH=/.venv/bin:$PATH

COPY ./src /app/

WORKDIR /app
