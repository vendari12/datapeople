## Setting up

##### Dependencies

The following dependencies are required for running this project locally

1. [Docker compose](https://docs.docker.com/compose/install/)
2. Vs Code | Pycharm this is based on developers preference
3. ES lint (Sonarcude extension)

##### Clone the repository

```
$ https://github.com/datapeople-eng/vendari
```

##### Add Environment Variables

Create a file called `.env` that contains environment variables. Place the `.env` file in your project root
directory

**Very important: do not include the `.env` file in any
commits. This should remain private.** You will manually maintain this file locally, and keep it in sync on your host.

Variables declared in file have the following format: `ENVIRONMENT_VARIABLE=value`. You may also wrap values in double
quotes like `ENVIRONMENT_VARIABLE="value with spaces"`.

1. In order for Services to run, these variables are required:

| Variable         | Default               | Discussion                                    |
|------------------|-----------------------|-----------------------------------------------|
| `ADMIN_EMAIL`    | `Nil`  | email associated with your USA jobs org account            |
| `JOB_API_KEY` | `Nil`            | Head over to `https://developer.usajobs.gov/apirequest/` to get your API key         |
| `ELASTIC_PORT` | `9200`            | Port where elastixsearch instance is served         |
| `ELASTIC_HOST` | `elasticsearch`            |  Host address where elasticsearch is currently running on         |
| `ELASTIC_PASSWORD ` | `Nil`(Optional)            |  Provide this if your elasticsearch is protected        |
    


##### Initialize the project

Be sure you don't have anything running on port 8000

```
$ make run
```
This will start a number of containers like elasticsearch, worker, jobboard

Worker: A celery beat process responsible for periodically pulling in job updates to elasticsearch

Jobboard: User facing API interface for quering jobs

Elasticsearch: Datastore storing all available jobs

Cache: DragonflyDB (Redis) cache store for celery worker

##### Available commands

`$ make run`  starts the project <br />
`$ make test`  runs the test suite <br />
`$ make ingest`  Executes the ingest pipeline to pull in jobs

N/B: A worker process is responsible for pulling in latest job updates daily (00:00 UTC)


##### (If you're on a Mac) Make sure xcode tools are installed

```
$ xcode-select --install
```


## Formatting code

Before you submit changes to this repo, you may want to autoformat your code with `black`.


