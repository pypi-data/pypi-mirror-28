# emmapy

Python simple SMTP E-mail module

## Getting Started

In your python script, use this.

```
>>> from emmapy.model import EmailMessage
>>> em = EmailMessage(subj="something", body="hello there", to="recipient@domain", fro="sender@domain")
>>> em.send()
```

To send messages containing html markup as mime type plain/html,
use this.

```
>>> from emmapy.model import EmailMessage
>>> em = EmailMessage(
...  subj="something",
...  body="<p>hello</p><p>there</p>",
...  to="recipient@domain",
...  fro="sender@domain",
...  mime_type='text/html')
>>> em.send()
```

### Prerequisites

By default, the module uses an SMTP server running on localhost, e.g. postfix or sendmail.

### Installing

```
pip install emmapy
```

