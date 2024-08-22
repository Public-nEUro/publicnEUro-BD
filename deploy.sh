rsync -avz --delete --filter="dir-merge,- .gitignore" --exclude '.git' --exclude '.env' --exclude 'frontend/src/environments/environment.ts' --exclude '.gitignore' --exclude '.deploy.sh' --exclude '.docker-compose.yml' --include '*' . root@10.45.130.67:/dpnru002/shared/group/data-manager
ssh root@10.45.130.67 'cd /dpnru002/shared/group/data-manager && ./restart-test.sh'
