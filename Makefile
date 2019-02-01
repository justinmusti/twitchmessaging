secrets :
	bash set_secrets.sh

verify:
	echo "Verifying necessary programs exist."
	command -v docker >/dev/null 2>&1 || { echo >&2 "docker is not installed.  Aborting."; exit 1; }
	command -v docker-compose >/dev/null 2>&1 || { echo >&2 "docker-compose is not installed.  Aborting."; exit 1; }
	command -v npm >/dev/null 2>&1 || { echo >&2 "node/npm is not installed.  Aborting."; exit 1; }

up:
	make verify
	docker-compose up -d
	docker ps -a

down:
	make verify
	docker-compose down --rmi all

redo:
	make down
	make up

bundle:
	cd jmsg/frontend; npm install;	npm install -g webpack;	webpack --debug --progress

