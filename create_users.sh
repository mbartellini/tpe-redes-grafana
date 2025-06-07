#!/bin/bash

echo "Creating users..."

for i in $(seq 1 1000);
do
  curl -X 'POST' \
    'http://localhost/users/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d "{
    \"username\": \"username_${i}\",
    \"password\": \"password\"
  }"
done

echo "Finished creating users"
