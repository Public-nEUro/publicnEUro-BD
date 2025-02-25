[ "$(basename "$PWD")" = "publicnEUro-BD" ] || {
    echo "This script should be run from the root of the git-project"
    exit 1
}

rsync -avz --delete --filter="dir-merge,- .gitignore" --exclude '.git' --exclude 'env/local' --exclude 'env/test' --exclude 'env/prod/nginx/tls' --exclude 'env/prod/nginx/ssl' --exclude 'datalad/docker-mount' --include '*' . root@10.45.130.67:/dpnru002/shared/group/data-manager/prod
ssh root@10.45.130.67 'cd /dpnru002/shared/group/data-manager/prod/env/prod && ./restart.sh'
