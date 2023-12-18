start:
	docker-compose -f ./docker-compose.yml down -v; \
    docker-compose -f ./docker-compose.yml rm -fsv; \
	docker-compose -f ./docker-compose.yml up --remove-orphans;

start-gpu:
	docker-compose -f ./docker-compose-gpu.yml down -v; \
    docker-compose -f ./docker-compose-gpu.yml rm -fsv; \
	docker-compose -f ./docker-compose-gpu.yml up --remove-orphans;
stop:
	docker-compose -f ./docker-compose.yml down -v; \
	docker-compose -f ./docker-compose-gpu.yml down -v; \
    docker-compose -f ./docker-compose.yml rm -fsv; \
    docker-compose -f ./docker-compose-gpu.yml rm -fsv;