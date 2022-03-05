# Library management

[Brief description of the application]

## Installation

Make sure you have python3 installed with venv. If you don't have [venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/), you can install it with:

```bash
python3 -m pip install --user virtualenv
```

Clone the repository:

```bash
git clone git@github.com:Faith-qa/uberpool.git
```

Cd on the root folder of the project, and create the virtual environment with
```bash
make create_environment
```

Then, you can activate it with:
```bash
source env-africanlibraries/bin/activate
```

And install dependencies with:
```bash
make install
```
With all dependencies installed, you can initialize the database with a sample of the library dataset from the excel files

```bash
make initialize
```

Note that from this command, you will be prompted to create a super user account (admin).

Please, check other quick make commands from the Makefile.

Last step, make a copy of the .env.dev file, and rename it to .env. Then, set values to the those environment variables.

All should be set now, you can run the develoment server and login with a demo user credential: 
    Username: Demo01
    Password: Demo
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
