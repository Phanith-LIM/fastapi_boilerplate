# Use a slim version of Python 3.12
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install Poetry, pin the version to ensure consistency
RUN pip install --no-cache-dir poetry==1.6.1

# Copy poetry files first to leverage Docker layer caching
COPY pyproject.toml poetry.lock /app/

# Install dependencies without dev dependencies, using --no-root for efficiency
RUN poetry install --no-dev --no-interaction --no-ansi

# Expose the application port
EXPOSE 8000

# Copy the rest of the application
COPY . /app

# Run the application using poetry to ensure it's in the virtual environment
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
