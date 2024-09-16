## FastAPI Boilerplate

A FastAPI boilerplate project designed to help you kickstart your API development with best practices and essential features.

### Features

- **Database Integration**: Configured with SQLAlchemy for ORM and database management.
- **Authentication and Authorization**: Basic setup for user management and access control.
- **Environment Configuration**: Uses `.env` files for easy management of sensitive settings.
- **Modular Architecture**: Well-organized structure for easy extension and maintenance.

### Pre-requisites
- Poetry
- Python 3.8
- Docker


### Getting Started

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Phanith-LIM/fastapi_boilerplate.git
    cd fastapi_boilerplate
    ```

2. **Set Up Environment:**

    - Copy `.env.example` to `.env`:

      ```bash
      cp .env.example .env
      ```

    - Update the `.env` file with your actual configuration values.

3. **Install Dependencies:**

    ```bash
    poetry install
    ```

4. **Run the Application:**

    ```bash
    poetry run uvicorn app.main:app --reload
    ```
   OR
   ```shell
    poetry run dev
    ```

### Docker
Integrate with Docker for easy deployment and development.
```shell
docker-compose up --build
```