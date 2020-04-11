set -e
sam validate
tox -e py37-unit
sam build
sam deploy
set +e
export SAMMY_HOST=$(aws cloudformation describe-stacks --stack-name Sammy-stage --query "Stacks[0].Outputs[?OutputKey=='SammyApi'].OutputValue" --output text)
tox -e py37-integration
