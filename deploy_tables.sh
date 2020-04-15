STACK_NAME=Sammy-local
set -e
sam validate
sam build
sam deploy --stack-name $STACK_NAME
set +e
export USERS_TABLE_NAME=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].Outputs[?OutputKey=='UsersTable'].OutputValue" --output text)
python3 ./config/init_local_variables.py
