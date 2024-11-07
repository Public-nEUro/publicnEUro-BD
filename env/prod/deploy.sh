rsync -avz --delete --filter="dir-merge,- .gitignore" --exclude '.git' --exclude 'env/local' --exclude 'env/test' --exclude '.gitignore' --include '*' . root@10.45.130.67:/dpnru002/shared/group/data-manager/prod
ssh root@10.45.130.67 'cd /dpnru002/shared/group/data-manager/prod/env/prod && ./restart.sh'
