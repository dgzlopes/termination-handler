# termination-handler
[![PyPI](https://img.shields.io/pypi/v/cloud-detect.svg)](https://pypi.org/project/termination-handler/)
[![PyPI - License](https://img.shields.io/pypi/l/cloud-detect.svg)](https://github.com/dgzlopes/termination-handler/blob/master/LICENSE.md)
## About
`termination-handler` handles termination notices on spot/preemptible instances.

As an example, if deployed on a Kubernetes cluster and a termination notice is issued by the cloud provider, `termination-handler` drains the node it is running on before the node is taken away by the cloud provider.

Inspired by [pusher/k8s-spot-termination-handler](https://github.com/pusher/k8s-spot-termination-handler) for AWS, `termination-handler` surges from the need to operate the same tooling in various distinct environments (providers, orchestrators...)

## Features
- Supports multiple cloud providers (AWS, GCP).
- Supports multiple handlers (Kubernetes, Nomad, Slack).
- Small and extensible.

## Documentation
TBD
## Usage
### Deploy to Kubernetes

A K8s docker image is available at [`dgzlopes/termination-handler-k8s`](https://hub.docker.com/r/dgzlopes/termination-handler-k8s) and sample Kubernetes manifests are available in the [deploy/k8s](deploy/k8s) folder.

To deploy in clusters using RBAC, please apply all of the manifests (Daemonset, ClusterRole, ClusterRoleBinding and ServiceAccount) in the [deploy/k8s](deploy/k8s) folder but uncomment the `serviceAccountName` in the [Daemonset](deploy/k8s/daemonset.yaml).

#### Requirements

For `termination-handler` to schedule correctly; you will need an identifying label on your spot/preemptible instances.

We add a label `node-role.kubernetes.io/spot-worker` to our spot/preemptible instances and hence this is the default value in the node selector of the [Daemonset](deploy/k8s/daemonset.yaml).
```yaml
nodeSelector:
  "node-role.kubernetes.io/spot-worker": "true"
```
To achieve this, add the following flag to your Kubelet:
```
--node-labels="node-role.kubernetes.io/spot-worker=true"
```

#### Configuration

To define any custom parameters to the drain command you can use `DRAIN_PARAMETERS` environment property. If not defined, default parameters are `--grace-period=120 --force --ignore-daemonsets`.
```yaml
env:
  - name: DRAIN_PARAMETERS
    value: '--grace-period=120 --force --ignore-daemonsets --delete-local-data'
```
### Deploy to Nomad
A Nomad docker image is available at [`dgzlopes/termination-handler-nomad`](https://hub.docker.com/r/dgzlopes/termination-handler-nomad).

TBD

### Demo mode

The main way to use termination-handler is waiting for the termination notice from the cloud provider. However, termination-handler comes with a demo mode that is can simulate the notice. When deployed it will identify your cloud provider and run your handlers.

To activate termination-handler demo mode on Kubernetes, you can use `DEMO_TERMINATION_HANDLER` environment property.
```yaml
env:
  - name: DEMO_TERMINATION_HANDLER
    value: True
```

### Other handlers
#### Slack
Sends a notification message to a specific channel when a termination notice is issued.

## How to contribute
1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork [the repository](https://github.com/dgzlopes/termination-handler) on GitHub to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a [pull request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) and bug [me](https://github.com/dgzlopes) until it gets merged and published.

Some things that would be great to have:
- Support for Azure cloud provider.
- Support for Execution handler (certain command or task)
- Support for notifications (Datadog..)
- Option to omit selected cloud provider discovery.
