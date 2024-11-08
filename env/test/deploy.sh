[ "$(basename "$PWD")" = "data-manager" ] || {
    echo "This script should be run from the root of the git-project"
    exit 1
}

rsync -avz --delete --filter="dir-merge,- .gitignore" --exclude '.git' --exclude 'env/local' --exclude 'env/prod' --exclude 'datalad/docker-mount' --include '*' . root@10.45.130.67:/dpnru002/shared/group/data-manager/test
ssh root@10.45.130.67 'cd /dpnru002/shared/group/data-manager/test/env/test && ./restart.sh'
