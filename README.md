Task description
----------------

The task is to develop an application as shown on http://applicationtask.herokuapp.com.

The requirements are as follow:

- Django as web framework
- Bootstrap as front-end framework
- Keep the URL logic
- Regarding the aggregations: please implement one in Python code and the other one as database query, using Django's database API over raw SQL.


How to run application using Docker:
------------------------------------

### Build an image

```
    $ cd megawatt
    $ docker build -t megawatt/megawatt .
```

### Run container

```
    $ docker run --publish=8001:8000 --detach --name=megawatt megawatt/megawatt:latest
```

Now application can be accessed on http://localhost:8001/

### Run tests

```
    $ docker exec -it megawatt ./manage.py test -v2
```
