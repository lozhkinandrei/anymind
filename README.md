# Anymind asignment

### Quickstart

1. Please install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) if not installed yet.
2. Clone this repository `git clone https://github.com/lozhkinandrei/anymind.git`
3. From the root project folder `anymind`, run `docker-compose up` to build images, create and start containers.
4. Visit http://localhost in your browser to make sure the server is running. You should see `{"Hello":"World"}`.
5. Check [API documentation](http://localhost/docs).

### Docker-compose service / Docker container names

| Docker-Compose Service | Docker Container                   |    Port    |
| ---------------------- | ---------------------------------- | ---------- |
| anymind                | anymind                            | 80         |


e.g. `docker-compose restart anymind` and `docker restart anymind` gives the same result, both will restart `anymind` service/container. It's just a matter of preference.

### Useful commands
- Show logs: `docker-compose logs -f anymind`
- Run tests: `docker-compose exec anymind pytest`
- Attach to container for interactive debugging with `pdb`: `docker attach anymind` (to exit press `ctrl + p`, then `ctrl + q`)


### Assignment Checklist:
- The deadline is within 5 days from 17 September 2021 <= `21 September 2021` ✔️
- Push your code to your public repository on GitHub == [repo](https://github.com/lozhkinandrei/anymind) ✔️
- You can choose any tool you like for this project but the programming language should be Python 3.7, 3.8, or 3.9 == `Python 3.9` ✔️
- You can use any Python web framework (Django, Flask, Tornado, ...etc) you prefer == `FastAPI` ✔️
- The repository should have a readme file with clear instructions on how to deploy/install locally ✔️
- Include unit tests ✔️
- DON’T use public available Twitter SDK instead please implement your own ✔️
