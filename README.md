# Running a local environment

Copy the `.env.template` to a file called `.env`.

In `frontend/src/environments` copy the `environment.template.ts` to a file called `environment.ts`.

In the root folder run

```
docker compose up
```

to start a local database and backend server.

In the `frontend` folder run

```
npm i
```

to install the required packages for the frontend, and then run

```
npm start
```

to start a local frontend server.

The local site should be accessible at `http://localhost:4200`.
All mails being sent will be caught by MailCatcher locally and can be viewed at `http://localhost:1080`.
