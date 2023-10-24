# Good morning! 🌞

Find out where the morning birds are tweeting easily with a single HTTP GET request.

## Set up

You'll (sadly) need to host this yourself. You can either host directly on your machine, or use docker.

### Bare metal

Make sure to install all dependencies, preferably in a virtual environement.

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then you can run the server with `uvicorn app.main:morning`. You can test that everything works with a simple `curl localhost:8000`.

### Docker

Given that you can build and run Docker images on your system, you can choose to host the server this way instead.

```sh
docker build -t good-morning-api .
docker run --rm -itd -e TZ=[Your/Timezone] -p [Port]:80 good-morning-api
```

Where you will need to provide

- `[Your/Timezone]`, optionally set to your timezone. If left out, Docker will default to UTC which may not be what you want.
- `[Port]`, set to the host port you want to use for communicating with the API.

