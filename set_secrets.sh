#!/usr/bin/env bash

if [ -e .env ]
	then
		echo "File already exists"
	else
		echo "Creating new .env file."
		touch .env
		echo "APP_STAGE=staging" >> .env
		echo "POSTGRES_DB=twitchmmessaging" >> .env
		echo "POSTGRES_USER=twicth_user" >> .env
		echo "POSTGRES_PASSWORD=root" >> .env
		echo "POSTGRES_HOST=db" >> .env
		echo "POSTGRES_PORT=5432" >> .env
		echo "REDIS_HOST=redis" >> .env
		echo "REDIS_PORT=6379" >> .env
		echo "New .env file has been created."
fi
