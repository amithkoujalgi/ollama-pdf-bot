start:
	docker-compose -f ./docker-compose.yaml down -v; \
    docker-compose -f ./docker-compose.yaml rm -fsv; \
	docker-compose -f ./docker-compose.yaml up --remove-orphans;

start-gpu:
	docker-compose -f ./docker-compose-gpu.yaml down -v; \
    docker-compose -f ./docker-compose-gpu.yaml rm -fsv; \
	docker-compose -f ./docker-compose-gpu.yaml up --remove-orphans;

stop:
	docker-compose -f ./docker-compose.yaml down -v; \
    docker-compose -f ./docker-compose.yaml rm -fsv;