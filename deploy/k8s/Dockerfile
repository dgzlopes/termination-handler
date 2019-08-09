FROM python:3-slim-stretch

ARG VERSION=undefined
ENV VERSION ${VERSION}

# Install curl and certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openssl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

# Install termination-handler
RUN pip install termination-handler --upgrade --no-cache-dir

ENTRYPOINT ["termination-handler", "--k8s"]