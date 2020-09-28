FROM python:3.8-buster

# Create working directory
RUN mkdir app
WORKDIR /app

# Install poetry and dependencies
RUN pip install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app

# Add source to path
ENV PYTHONPATH="${PYTHONPATH}:/app/cli_api"

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
