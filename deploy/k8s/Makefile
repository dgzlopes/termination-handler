.PHONY: build
build:
	docker build -t dgzlopes/termination-handler-k8s:v0.0.1 . --no-cache

.PHONY: publish
publish:
	docker login
	docker push dgzlopes/termination-handler-k8s:v0.0.1

.PHONY: deploy
deploy:
	kubectl create -f manifests/clusterrole.yaml
	kubectl create -f manifests/serviceaccount.yaml
	kubectl create -f manifests/clusterrolebinding.yaml
	kubectl create -f manifests/daemonset.yaml
