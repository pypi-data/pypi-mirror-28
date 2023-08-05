# emmapy

Python simple SMTP E-mail module

## Getting Started

In your python script, use this.

```
>>> from emmapy import model
>>> em = model.EmailMessage(subj="something", body="hello there", to="recipient@domain", fro="sender@domain")
>>> em.send()
```

### Prerequisites

By default, the module uses an SMTP server running on localhost, e.g. postfix or sendmail.

### Installing

```
pip install emmapy
```

