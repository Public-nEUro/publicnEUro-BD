# publicnEUro-BD

This repository exposes the database behind PublicnEUro.eu. You can reuse it for free under MIT licence.
This work was funded by [Novo Nordisk Foundation](https://novonordiskfonden.dk/en/) (NNF20OC0063277).  

## Running a local environment

Install docker.

In the `env/local` folder run

```
docker compose up
```

to start a local environment.

DataLad is available at `https://localhost:8443`.

The management site is at `https://localhost:8443/manage`.

All emails being sent will be caught by MailCatcher locally and can be viewed at `https://localhost:8443/email`.

## Calling the API

User registration and DUA signing (and SSC if outside EU and adequate countries) happens via browser since in most cases, it requires admin interaction.  

Once you have registered, and requested a dataset and signed the DUA, you can obtain the download URL at any time via command line entering the PublicnEUro (PN) ID:  

`curl -w "\n" -u email:password -L https://datacatalog.publicneuro.eu/api/get_share_link/PNXXXXXX`
