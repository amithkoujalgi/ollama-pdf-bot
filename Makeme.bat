@echo off
if "%1" == "start" goto start
if "%1" == "start-gpu" goto start-gpu
if "%1" == "stop" goto stop
echo Invalid argument. Use "start", "start-gpu", or "stop".
goto end

:start
	docker-compose -f ./docker-compose.yml down -v
	docker-compose -f ./docker-compose.yml rm -fsv
	docker-compose -f ./docker-compose.yml up --remove-orphans
	goto end

:start-gpu
	docker-compose -f ./docker-compose-gpu.yml down -v
	docker-compose -f ./docker-compose-gpu.yml rm -fsv
	docker-compose -f ./docker-compose-gpu.yml up --remove-orphans
	goto end

:stop
	docker-compose -f ./docker-compose.yml down -v
	docker-compose -f ./docker-compose-gpu.yml down -v
	docker-compose -f ./docker-compose.yml rm -fsv
	docker-compose -f ./docker-compose-gpu.yml rm -fsv
	goto end

:end