# zeek-dgaintel

This repository contains a [Zeek Broker](https://zeek.org/) client code for the real-time detection of domain
generation algorithms ([DGA](https://en.wikipedia.org/wiki/Domain_generation_algorithm)), which are commonly used by
malware for communicating with the command and control servers. Detection is performed by intercepting DNS requests
with Zeek and feeding the domain names to a CNN-LSTM neural network model implemented by
[dgaintel](https://github.com/sudo-rushil/dgaintel).

## Usage

The `zeek-dgaintel` service can be executed as a standalone application directly on the host or as a Docker container.

### Standalone

To run the service directly on the host, you need to install the following dependencies:
- Python 3.11
- Poetry
- [Full Zeek installation](https://docs.zeek.org/en/master/install.html) or
[Zeek Broker bindings for Python](https://github.com/zeek/broker#compilinginstalling) (the `broker` package must be
available in the Python path)

Then install the project dependencies using Poetry:

```shell
$ poetry install
```

Finally, run the service using Poetry:

```shell
$ poetry run python3 -m zeek-dgaintel
```

### Docker

To run the service as a Docker container, you need to have Docker Engine installed on the host. Then simply build and
run the image using the typical Docker commands:

```shell
$ docker build -t zeek-dgaintel .
$ docker run -it --rm zeek-dgaintel
```

Configuration for the service can be provided to the `run` command using environment variables (`-e` option). 
