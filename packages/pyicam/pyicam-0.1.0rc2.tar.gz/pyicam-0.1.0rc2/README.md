# PyICAM

![](https://img.shields.io/badge/license-CC0-green.png "License: Creative Commons Zero v1.0 Universal")

Python Identity, Credential, and Access Management.

## Install
```
pip install pyicam
```

## Supported Python Versions
 - Python 3.3+

## Overview

PyICAM is a simple, SAML authentication library to help Python software developers use the [NOAA Identity, Credential, Access and Federation Management (ICAM)](https://noaaonline.noaa.gov/contact_us.html) login provider in a consistent fashion.

It consists of a minimal, easy to use interface around the open-source [python3-saml](https://pypi.python.org/pypi/python3-saml) toolkit from Onelogin, Inc.

Online documentation is at https://github.com/nwfsc-data/PyICAM

## Disclaimer
<sub>This repository is a scientific product and is not official communication of the National Oceanic and
Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is
provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of
Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed
by all applicable Federal law. Any reference to specific commercial products, processes, or services by service
mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or
favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a
DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by
DOC or the United States Government.</sub>

## Quick Start
Add SSO authentication to your existing Python webserver:

- [Generate signed certificate](#generate-signed-certificate)
- [Define your application attributes](#define-your-application-attributes)
- [Obtain SSO Authority attributes](#obtain-sso-authority-attributes)
- [Create settings file](#create-settings-file)
- [Submit Metadata](#submit-metadata)
- [Add your metadata URL](#add-your-metadata-url)
- [Add your login URL](#add-your-login-url)
- [Add your logout URL](#add-your-logout-url) - TBD

### Generate signed certificate
1). Generate a secret key & certificate request for signature, which will be used to identify your webserver to the SSO authority. Complete certificate details, as required by the Certificate Authority from whom you obtain a signed HTTPS certificate.

* Send your Certificate Authority the contents of: `CERT_REQUEST.csr`
* keep your `secrets/server.key` file secure. If anyone, at any time, can read this file - they can copy the key and impersonate your Python webserver.

```
openssl req -new -newkey rsa:2048 -nodes -keyout secrets/server.key -out CERT_REQUEST.csr
```

### Define your application attributes
2). Define a unique name, id, description & three URLs for your webserver. The URLs will be used to identify your webserver, and accept SSO and Single-Log-Out (SLO) transmissions from the remote SSO authority:

* serviceName: ___________________________
* serviceId: _______________________ (short, no spaces)
* serviceDescription: _______________________________________
* custom URLs:
    - entityIdURL: ____________________________________ (E.g.: `https://my.sample_domain/great_service/saml/metadata/`)
    - assertionConsumerServiceURL: _______________________________________ (E.g.: `https://my.sample_domain/great_service/saml/?acs`)
    - singleLogoutServiceURL: ___________________________________ (E.g.: `https://my.sample_domain/great_service/saml/?sls`)

### Obtain SSO Authority attributes
3). Obtain the id, url & identifying certificate of your SSO authority:

* id: ______________ (typically short, no spaces. Often at the end of the authority URLs)
* certificateText: ________________________________________ (base64 encoded text)
* remote SSO authority URLs:
    - singleSignOnServiceURL: ____________________________________
    - singleLogoutServiceURL: ____________________________________

### Create settings file
4). Create a file called `settings.json` and populate it with the details from Step 2. & 3.:

```
{
    "strict": true,

    "debug": true,

    "sp": {
        "entityId": "__Enter_step2_entityIdURL__",
        "assertionConsumerService": {
            "url": "__Enter_step2_assertionConsumerServiceURL__",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        },
        "singleLogoutService": {
            "url": "__Enter_step2_singleLogoutServiceURL__",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "attributeConsumingService": {
                "serviceName": "__Enter_step2_name__",
                "serviceDescription": "__Enter_step2_description__",
                "requestedAttributes": [
                    {
                        "name": "__Enter_step2_id__",
                        "isRequired": false,
                        "nameFormat": "",
                        "friendlyName": "",
                        "attributeValue": []
                    }
                ]
        },
        "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
        "x509cert": "",
        "privateKey": ""
    },

    "idp": {
        "entityId": "__Enter_step3_id__",
        "singleSignOnService": {
            "url": "__Enter_step3_singleSignOnServiceURL__",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "singleLogoutService": {
            "url": "__Enter_step3_singleLogoutServiceURL__",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "x509cert": "__Enter_step3_certificateText__"

    }
}
```

### Submit metadata
5). Generate metadata for your webserver & submit it to your SSO authority.

 * Your SSO Identity Provider operator will let you know if submitted metadata is acceptable, or if any settings changes must be made.
 * SSO operator will provide you with a SSO login URL, to allow users to log into your application via their Identity server: _________________________

```python
from pyicam.saml.metadata import get_entity_descriptor
settings = 'settings.json' #specify the path to your files
cert = 'cert.pem' #save cert issued by your Certificate Authority in Step 1). in PEM format
key = 'secrets/server.key'
metadata, content_type = get_entity_descriptor(settings, cert, key)
print(metadata)
```

### Add your metadata URL
6). Add the custom entityIdURL from [Step: Define your application attributes](#define-your-application-attributes) to your webserver, so it returns metadata as shown in the previous [Step: Submit metadata](#submit-metadata).

 * Note: the HTTP response returned by the URL must have the content type (`text/xml`) indicated by PyICAM.

### Add your login URL
7). Add the custom assertionConsumerServiceURL from [Step: Define your application attributes](#define-your-application-attributes) to your webserver, to recieve login notifications via HTTP POST:

```python
from pyicam.saml.sso import login
host = request.env['HTTP_HOST'] #get the HTTP request details from your webserver
port = request.env['SERVER_PORT']
path = request.env['SCRIPT_NAME']+request.env['PATH_INFO']
settings = 'settings.json' #specify the path to your files
cert = 'cert.pem'
key = 'secrets/server.key'
user = login(host, port, path, settings, cert, key, post_data=request.params)
# log in the user, using the provided dict, in whatever fashion used by your program
# your URL may now respond to the user, or redirect them, however you see fit
if 'relay_state' in user:
    # If the SSO login URL specified a SAML2 "RelayState" parameter for
    # the final redirect destination, PyICAM will return that value as: 'relay_state'
    users_saml2_RelayState_redirect_value = user['relay_state']
```

Congratulations! Users may now log into your application via the SSO link provided by your Identity authority in [Step: Submit metadata](#submit-metadata).

### Add your logout URL
8). (Adding custom singleLogoutServiceURL - TBD)

#### Copyright (C) 2017-2018 ERT Inc.
