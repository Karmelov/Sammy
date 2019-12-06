set -e
tox -e py37-unit
set +e
sam build
sam local start-api &
server_pid=$!
tox -e py37-integration
kill $server_pid
