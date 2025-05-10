# code-judge-backend

```bash
git clone https://github.com/Naman-0206/code-judge-backend
cd code-judge-backend
cd setup
```
```powershell On Windows
.\run_backend_dev.bat
```
```bash On Linux
.\run_backend_dev.sh
```

in /setup/

docker build -t heatcode_backend ../server
docker tag heatcode_backend naman0206/heatcode_backend:latest
docker push naman0206/heatcode_backend:latest


docker build -t submission-worker ../workers/submission_worker
docker tag submission-worker naman0206/submission-worker:latest
docker push naman0206/submission-worker:latest


docker build -t execution-worker ../workers/execution_worker
docker tag execution-worker naman0206/execution-worker:latest
docker push naman0206/execution-worker:latest


docker run -d --name submission-worker --env-file .env naman0206/submission-worker:latest
docker run -d --name execution-worker --env-file .env naman0206/execution-worker:latest
