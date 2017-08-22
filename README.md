# Raccoon
A library for executing heavy deferred tasks

## User Guide
### How to use?
Before starting the application, make sure you have all requitements installed.
```bash
pip install -r requirements.txt
```
Tasks need to be defined in `client.py` file. You can write your own tasks or use already created ones.

The command pattern for starting the application is
```bash
python run.py [options]
```
`[options]` - is used to constrain the max number of running jobs. You can specify the limit for the particular task,
or restrict the total amount of running jobs.

Examples:
```bash
python run.py  # no limitations
python run.py --total=3 # max 3 running jobs
python run.py --make_report=2 # max 2 running jobs of type `make_report`
```
That's it! Your server is running. Dashboard is available on [http://0.0.0.0:8080/ ](http://0.0.0.0:8080/ )

**Note**: dashboard does not get updated automatically. You need to refresh the page in order to get new resutls.

You can submit a new job by sending a POST request to `/api/tasks/` endpoint with a payload like
```bash
{
	"type": "make_report",
	"params": {
		"num": 10
	},
	"email": "example@example.com"
}
```

## Developer Guide
### Vocabulary
**Task** - a user-defined class or function, which need to be executed with some parameters in order to get the result

**Job** - a process with a running task

**Broker** - a process responsible for creating new jobs, handling results, setting status to jobs

### Pipeline
1. User sends a POST request to an API in order to start a new job
2. Server validates the user's request, adds new task to `TASK_QUEUES`, sends a response bask to the user
3. Broker constantly checking the `TASK_QUEUES` and creates a new process for running the task
4. When task is finished, it pushes the result to the `RESULTS_QUEUE`
5. Broker constantly checking the `RESULTS_QUEUE` and sends an email to user with the result if needed

Broker is running in a separate process. This way Flask never gets blocked and can respond to requests instantly.

## Things to improve
* add tests
* make it start like `raccoon <user_tasks_file> [--<limits>]`
* make the dashboard get updates automatically
* add a possibility to attach files to sent messages
