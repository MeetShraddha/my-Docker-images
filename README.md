Step 1: Run your container with a fixed name (not a throwaway)
```
docker run -d --name my-notebook -p 8888:8888 -v "$(pwd)":/home/jovyan/work my-jupyter
```

The new part is --name my-notebook. This gives the container a stable identity you can stop and restart without losing its state — as opposed to docker run creating a brand new container every time.

Step 2: Day-to-day usage
- Stop it (when you're done for the day): docker stop my-notebook
- Start it again later (same container, same installed packages): docker start my-notebook
- Only use docker run again if you want a fresh one from scratch

This is the key mental shift: docker run = create new, docker start/docker stop = pause/resume existing.

Step 3: Ad-hoc package installs
Two ways, both fine:
A) From inside a Jupyter notebook cell (fastest, no terminal-switching):
```
!pip install seaborn
```
Works immediately in that notebook session. Since the container persists (you didn't docker run again), it stays installed next time you docker start it too.
B) From your Mac's terminal, directly into the running container:
```
docker exec my-notebook pip install seaborn
```
docker exec runs a command inside an already-running container — useful if you want to install something without opening Jupyter.

Step 4: "Promote" ad-hoc packages into your stable base
Every so often — say, when a project's dependencies settle — add the packages you've been ad-hoc installing into requirements.txt, then rebuild:
```
docker build -t my-jupyter .
```
This keeps your image (the reusable blueprint) in sync with what you've actually been using, so a future fresh container has them pre-installed instead of you re-installing by hand again.
