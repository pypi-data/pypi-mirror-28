This is the MasterCard OpenAPI Python Core SDK


# Dependency Install

`brew install python`
`brew link --overwrite python`
`pip install --upgrade pip setuptools`

# Run Tests
need to run these commands before runnig the test
`pip install --user nose`
`pip install --user mock`
`pip install --user urllib3`

### Normal Tests

`python -m unittest discover tests`
or
`nosetests`

### With coverage

`nosetests --with-coverage --cover-package=mastercardapicore`
