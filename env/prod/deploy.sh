[ "$(basename "$PWD")" = "publicnEUro-BD" ] || {
    echo "This script should be run from the root of the git-project"
    exit 1
}

if [ -z "$1" ]; then
    echo "Please specify your username"
    exit 1
fi

USER="$1"

read -s -p "Enter password for $USER: " PASSWORD
echo

rsync -avz --delete --filter='dir-merge,- .gitignore' --exclude '.git' --exclude 'env/local' --exclude 'env/test' --exclude 'env/prod/nginx/tls' --exclude 'env/prod/nginx/ssl' --exclude 'datalad/docker-mount' --include '*' . $USER@10.45.130.68:/tmp/syncfolder
ssh $USER@10.45.130.68 "cd /tmp/syncfolder && echo "$PASSWORD" | sudo -S rsync -avz --delete --filter='dir-merge,- .gitignore' --exclude '.git' --exclude 'env/local' --exclude 'env/test' --exclude 'env/prod/nginx/tls' --exclude 'env/prod/nginx/ssl' --exclude 'datalad/docker-mount' --include '*' . /dpnru002/shared/group/data-manager/prod"
ssh $USER@10.45.130.68 'cd /dpnru002/shared/group/data-manager/prod/env/prod && echo '$PASSWORD' | sudo -S ./restart.sh'
