FROM python:3-slim-stretch

ARG VERSION=undefined
ENV VERSION ${VERSION}
ENV NOMAD_VERSION="0.9.0"

# Install curl and certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openssl \
    ca-certificates \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install nomad client
RUN curl --silent --remote-name https://releases.hashicorp.com/nomad/${NOMAD_VERSION}/nomad_${NOMAD_VERSION}_linux_amd64.zip &&\
    unzip nomad_${NOMAD_VERSION}_linux_amd64.zip &&\
    chown root:root nomad &&\
    mv nomad /usr/local/bin/

# Install termination-handler
RUN pip install termination-handler --upgrade --no-cache-dir

ENTRYPOINT ["termination-handler", "--nomad"]
