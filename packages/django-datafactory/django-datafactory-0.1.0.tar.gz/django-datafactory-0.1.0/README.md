# django-datafactory [![Build Status](https://travis-ci.org/ParticulateSolutions/django-datafactory.svg?branch=master)](https://travis-ci.org/ParticulateSolutions/django-datafactory)

`django-datafactory` is a lightweight [django](http://djangoproject.com) plugin which provides the integration of the service [datafactory](https://www.deutschepost.de/de/d/deutsche-post-direkt/datafactory.html).

## How to install django-datafactory?

There are just two steps needed to install django-datafactory:

1. Install django-paydirekt to your virtual env:

	```bash
	pip install django-datafactory
	```

2. Configure your django installation with the following lines:

	```python
    # django-datafactory
    INSTALLED_APPS += ('django_datafactory', )

    DATAFACTORY = True

    # Those are dummy test data - change to your data
    DATAFACTORY_AUTH_SETTINGS = {
        "API_USERNAME": "Your-Datafactory-Username", 
        "API_PASSWORD": "Your-Datafactory-Password"
    }
	```


## What do you need for django-datafactory?

1. An [datafactory](https://www.deutschepost.de/de/d/deutsche-post-direkt/datafactory.html) account
2. Django >= 1.8

## Usage

### Minimal typeahead example:

```python
datafactory_wrapper = DataFactoryWrapper(auth=settings.DATAFACTORY_AUTH_SETTINGS)
datafactory_response = datafactory_wrapper.typeahead(
    postal_code=56070, 
    city="Koblenz", 
    district="Metternich", 
    street="universitaetsstrasse"
)
datafactory_response
{u'Ergebnisse': {u'Ergebnis': {u'Anfragentyp': u'PlzOrtOtlStr', u'UUID': u'065C55A2B99DAAF62975505DBD409663', u'Ort': u'Koblenz', u'Plz': 56070, u'Strasse': u'Universit\xe4tsstr.', u'Adresstyp': u'A', u'Ortsteil': u'Metternich'}}}

```

## Copyright and license

Copyright 2018 Jonas Braun for Particulate Solutions GmbH, under [MIT license](https://github.com/minddust/bootstrap-progressbar/blob/master/LICENSE).
