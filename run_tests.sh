set -e
tox -e py37-unit
sam build
sam local start-api &
set +e
server_pid=$!
tox -e py37-integration
kill $server_pid
