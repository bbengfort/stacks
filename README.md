# Bengfort Stacks

**Personal eBook library for the Bengfort Family**

The Bengfort Stacks are a content and media storage app to backup DRM free eBooks and magazines for personal use only.


## Project Setup

Build the docker file as follows:

```
docker build -t stacks:latest .
```

Note that the build process compiles the Go API server and Vue client separately then runs them both using nginx and an entrypoint.sh file.

### Run the Container

Run the container in detached mode:

```
docker run -d --name stacks -e "PORT=8765" -p 8007:8765 stacks:latest
```

You should now be able to access the site at [localhost:8007](http://localhost:8007/).


### Stop the Container

```
docker stop stacks && docker rm stacks
```