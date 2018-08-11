#!/usr/bin/env bash

SCHEMA=$(cat schema.sql)
docker exec -it messenger_db_1 mysql -uroot -proot -e "$SCHEMA"
docker exec -it messenger_db_1 mysql -uroot -proot -e 'SELECT * FROM messenger.conversations;'
