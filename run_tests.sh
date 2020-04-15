set -e
tox -e py37-unit
set +e
export SAMMY_HOST=http://localhost:3000/
tox -e py37-integration
