backup2s3
=========

Backup files and mysql databases to Amazon S3

Requirements
------------

- mysql-client

Installation
------------
Using PIP via PyPI::

    pip install backup2s3

Using PIP via Github::

    pip install git+https://github.com/wavedocs/backup2s3#egg=backup2s3

Usage
-----

Create new IAM User

- In the IAM Management Console on Amazon, click Create New User and follow on-screen instructions.
- Click Create User Policy on the user page, then select Custom Policy, then paste the following text in the text area. Replace INSERT_YOUR_BUCKET_NAME with the bucket name you have previously created, and submit the form:


```
{
	"Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::INSERT_YOUR_BUCKET_NAME",
                "arn:aws:s3:::INSERT_YOUR_BUCKET_NAME/*"
            ]
        }
    ]
}
```

Сopy and edit the config

```
$ cp /etc/backup2s3-sample.yml /etc/backup2s3.yml
```

Run backup files and mysql databases

```
/usr/bin/backup2s3

Usage: backup2s3 [options]
    Options:
      -a, --all Backup files and mysql db
      -f, --files Backup files
      -d, --databases Backup mysql databases
      -h, --help Print man