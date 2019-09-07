.PHONY: build
build:
	docker build -t dgzlopes/termination-handler-nomad:v0.0.4 -t dgzlopes/termination-handler-nomad:latest . --no-cache

.PHONY: publish
publish:
	docker login
	docker push dgzlopes/termination-handler-nomad:v0.0.4
	docker push dgzlopes/termination-handler-nomad:latest
