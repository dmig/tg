FROM python:3.9.4-slim-buster
RUN --mount=source=dist,target=/dist PYTHONDONTWRITEBYTECODE=1 pip install --disable-pip-version-check --no-cache-dir /dist/*.whl
CMD [ "python", "-m", "tg" ]
