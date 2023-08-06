* * *
#   **keyup** |  Automated Access Key Rotation for Amazon Web Services IAM Users
* * *

## Purpose ##

`keyup` automates IAM user access key rotation from the cli.  

**Keyup**:

* is a safe, error-free mechanism to rotate (renew) access keys to Amazon Web Services as  
frequently as you wish, with minimal effort and risk.
* enables you to change your access keys when required by executing a single command from the cli.  
* Alternatively, enter a keyup command in your crontab with the ``` --auto ``` parameter and renew access  
keys on a daily schedule.
* **keyup** requires only the profile name of your IAM user in your local [awscli configuration](https://docs.aws.amazon.com/cli/latest/reference/):

```bash

    $ keyup --profile Dave --operation up

```

* * *

## Documentation ##

**Online Documentation**:

* Complete html documentation available at [http://keyup.readthedocs.io](http://keyup.readthedocs.io).

**Download Documentation**:

* [pdf format](https://readthedocs.org/projects/keyup/downloads/pdf/latest/)
* [Amazon Kindle](https://readthedocs.org/projects/keyup/downloads/epub/latest/) (epub) format

* * *

## Getting Started

Before starting, suggested to read the following:

* [Frequently Asked Questions (FAQ)](http://keyup.readthedocs.io/en/latest/FAQ.html)
* [Keyup License Terms](http://keyup.readthedocs.io/en/latest/license.html)

**keyup** is licensed under [General Public License v3](http://keyup.readthedocs.io/en/latest/license.html)

* * *

## Dependencies

- Python3 via one of the following:

    - Python 3.4.X+
    - Python 3.5.X+
    - Python 3.6.X+

- Linux Operating System, one of the following:

    - Redhat Enterprise Linux v7.X
    - Ubuntu 14.04, Ubuntu 16.04, and corresponding Ubuntu variants
    - Amazon Linux (2016.03+ )

- Windows Operating System: (SUPPORT PENDING)

    - Windows 7
    - Windows 8 (not tested)
    - Windows 10 (not tested)

- API credentials and access keys maintained via [local awscli configuration](https://docs.aws.amazon.com/cli/latest/reference/)

* * *

## Installation

Installation via pip (windows & Linux):

```bash

    $ sudo -H pip3 install keyup

```

* * *

### **Options**

Diplay help menu

```bash

    $ keyup -h

```

![](./assets/help-menu.png)

* * *

## Author & Copyright

All works contained herein copyrighted via below author unless work is explicitly noted by an alternate author.

* Copyright Blake Huber, All Rights Reserved.

* * *

## License

* Software contained in this repo is licensed under the [GNU General Public License Agreement (GPL-3)](https://bitbucket.org/blakeca00/keyup/src/master/LICENSE.txt).

* * *

## Disclaimer

*Code is provided "as is". No liability is assumed by either the code's originating author nor this repo's owner for their use at AWS or any other facility. Furthermore, running function code at AWS may incur monetary charges; in some cases, charges may be substantial. Charges are the sole responsibility of the account holder executing code obtained from this library.*

Additional terms may be found in the complete [license agreement](https://bitbucket.org/blakeca00/keyup/src/master/LICENSE.txt).

* * *
