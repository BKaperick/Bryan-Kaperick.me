# Bryan-Kaperick.me
My personal website:
https://www.bryan-kaperick.me/

# Organization
- `./content/` contains all the html, php, and data files needed to build the site.  Additionally, within sub-directories pertaining to a specified project (e.g. ./content/poetry) there are additional python scripts which map json data into formatted html.
- `./public/` is the folder published by Netlify, so contains exactly the html files that comprise the website, in the desired heirarchy.  See Building section for more details.
- `./resources/` contains the data and scripts for the data refresh steps.

# Scripts
The site has various automated widgets that are handled by a collection of bash and python scripts.

## Building
`pre_build.sh` executes all the data ingestion scripts.  Most often, it consists of reading json data or image files, and formatting the extracted data into html and php files.

`build.sh` is responsible for generating the static html files from the html and php files in ./content. We use `php -S` to deploy onto a local webserver.  Then, we `wget` the produced html files, and write it to `./public`.  Lastly, we pass over `./public` with `cleanup.sh` which cleans up some file paths and unneeded files.

## Deployment and hosting
We build the code via Github Actions and deploy the changes onto the head of the master branch.  Netlify.app deploys the head of master.

`./.github/workflows/main.yml` 
1. Checks out the virtual environment (`uv`)
2. Ingests any new data (`pre_build.sh`)
2. Builds the website (`build.sh`)
3. Pushes the changes onto master branch.

## Local
`./deploy_site.sh` exists to simply deploy the state of `./public/` to a local php webserver at localhost:8000. It assumes the code has already been built with `./build.sh`.

A typical local workflow would be the following:
1. Make changes to the `./content/` directory
2. Execute `pre_build.sh draft` to apply the changes 
3. Execute `build.sh` to apply the changes to `./public/`
4. Execute `deploy_site.sh` to inspect changes in a web browser at `localhost:8000`


# Upcoming topics
- [x] ~Dark mode~
- [ ] Dedicated photo album pages
- [ ] Optimizing main photo page to load faster
