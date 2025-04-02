

## Requirements:

- [Docker](https://www.docker.com/get-started/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Docker compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)(on linux), [WSL Ubuntu](https://ubuntu.com/desktop/wsl)(on windows)


---
## How to use(Windows):
1. #### Clone the repo:
    ```bash
   git clone https://github.com/uzineck/sep_backend.git
   cd sep_backend
   ```
2. #### Install all required packages in `Requirements` section.
3. #### Open Docker Desktop
4. #### Open WSL Ubuntu in your terminal and go to cloned application folder
5. #### Create `.env` file from `.env.example`, make changes if needed
6. #### With Make command run:
     ```bash
     make app # to build application and storage containers 
     make migrate  # to apply all migrations to database
     make collectstatic # to collect and use static files in proxy
     ```
7. #### In your browser go to `localhost:80/api/docs`
8. #### Implemented Commands

    - `make app` - up application and storages
    - `make app-logs` - follow the logs in app container
    - `make app-down` - down application and all infrastructure
    - `make storages` - up only storages. you should run your application locally for debugging/developing purposes
    - `make storages-logs` - follow the logs in storages containers
    - `make postgres` - psql into postgres container
    - `make storages-down` - down all storage infrastructure
    - `make monitoring` - up monitoring docker compose(kibana, apm, elastic)
    - `make monitoring-logs` - show monitoring logs
    - `make monitoring-down` - down monitoring docker containers
    - `make proxy-logs` - show proxy container logs
    - `make proxy-reload` - if any changes were made to nginx config, while server is on, write this command
9. #### Django Specific Commands

    - `make migrations` - make migrations to models
    - `make migrate` - apply all made migrations
    - `make collectstatic` - collect static
    - `make superuser` - create admin user
    - `make loaddata` - searches for and loads the contents of the named fixture into the database
    - `make dumpdata` - outputs to standard output all data in the database associated with the named application
    - `make run-test` - runs test with pytest
    - `make runscheduler` - runs apscheduler for background tasks
