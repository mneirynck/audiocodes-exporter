
ARG APP_NAME=audiocodes_exporter
ARG APP_PATH=/opt/${APP_NAME}
ARG POETRY_VERSION=1.1.13
ARG USER_NAME=prom
ARG GROUP_NAME=prom
ARG UID=1000
ARG GID=1000

FROM python:alpine as builder
ARG APP_PATH
ARG APP_NAME
ARG POETRY_VERSION
ARG USER_NAME
ARG GROUP_NAME
ARG UID
ARG GID



ENV \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME='/opt/poetry'

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN apk --no-cache add curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python
ENV PATH="${POETRY_HOME}/bin:$PATH"


WORKDIR ${APP_PATH}

COPY  ./poetry.lock ./pyproject.toml ./README.md ./
COPY  ./src/${APP_NAME} ./${APP_NAME}
RUN poetry build --format wheel

#
# Runtime
#
FROM builder as runtime
ARG APP_PATH
ARG APP_NAME
ARG USER_NAME
ARG GROUP_NAME
ARG UID
ARG GID

RUN addgroup -g ${UID} ${GROUP_NAME} && \
    adduser --shell /sbin/nologin --disabled-password \
    --no-create-home --uid ${UID} --ingroup ${GROUP_NAME} ${USER_NAME}


ENV \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 

# Get build artifact wheel and install it
WORKDIR ${APP_PATH}
RUN chown 1000:1000 $(pwd)
COPY --chown=${USER_NAME}:${GROUP_NAME} --from=builder ${APP_PATH}/dist/*.whl ./

USER ${USER_NAME}
RUN pip install ./${APP_NAME}*.whl

ENV API_URL ""
ENV API_USERNAME ""
ENV API_PASSWORD ""

EXPOSE 9954

ENTRYPOINT ["audiocodes-exporter"]