# IDChecker

**IDChecker** is a tool to get a list of ID records from 1Password, sorted by expiration date.

## Description

Since **Lotus Notes DB** is about to fall into oblivion, a new way of working with ID records is needed.
**1Password** was chosen to store this data. However, there was a problem:

1Password does not provide the ability to sort records by custom fields, and this makes working with records inconvenient. This tool solves the sorting problem by using the official 1Password CLI as the basis.

IDChecker uses the following ID record fields when working with:
* **Title** - the name of the record
* **Expire** - a custom field that actually contains the expiration date
* **ID revalidation owner** - ID revalidation owner information
* **notes** - notes about the record that may contain useful information

## Environment
* Language: Python
* Third-party software: [1Password command-line tool](https://support.1password.com/command-line-getting-started/)
* Interface: CLI
* Supported OS: Linux, macOS

## Installation

**Requirements:**

 * Python 3.6+
 > The operating systems previously marked as supported have built-in Python support
 * pip
 > Usually Linux distributions have the pip package manager installed by default. If it is not installed, then follow the installation instructions:
 >
 > https://pip.pypa.io/en/stable/installing/#using-linux-package-managers

 > To install pip on macOS, use this instruction:
 >
 > https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py


**Linux:**
~~~
 $ pip install idchecker
~~~

**macOS:**
~~~
 $ python3 get-pip.py idchecker
~~~

## Usage

```
Usage:
    idchecker login <1password_url> <useranme>
    idchecker check [--vault=<vault_name>] [--dir=<path>] [--notes]
    idchecker -h | --help
    idchecker -v | --version

Options:
    --vault=<vault_name>            The name of the 1Password vault where the IDs are stored (it is better to frame the name with quotation marks)
    --dir=<path>                    The path to the folder where the report_<datetime>.csv file will be saved
    --notes                          Add notes from the ID record to the report
    -h, --help                      Show this help message.
    -v, --version                   Show the version.
```

> All the commands listed below are examples. Use them along with the usage section presented above to understand what you need to do

### Logging in

1. Execute **login** command

  ~~~
  $ idchecker login example.company.1password.com username@example.com
  ~~~

2. Then you will get a message that you need to enter **Secret Key**. Type it

  ~~~
  Enter the Secret Key for username@example.com at example.company.1password.com: A3-RTNYOW9-****-****-****-****-****
  ~~~

3. After that you will get a message that you need to enter **Master Password**. Type it

  ~~~
  Enter the password for username@example.com at example.company.1password.com: **********
  ~~~

4. If you have access and you did everything right, you will get **Session Token** in the following message:

  ~~~
  export OP_SESSION_company="M2gCFb-****-f6qe****vYfx****hdoF****1LJL****"
  # This command is meant to be used with your shell's eval function.
  # Run 'eval $(op signin company)' to sign in to your 1Password account.
  # Use the --raw flag to only output the session token.
  ~~~

  Just copy the entire line starting with **export**, paste it into the terminal, and press Enter

  ~~~
  $ export OP_SESSION_company="M2gCFb-****-f6qe****vYfx****hdoF****1LJL****"
  ~~~

### Checking

The tool allows you to get the result in two ways:
 * As a simple **output to the terminal**

 ~~~
 $ idchecker check
     title: ID : NAME 1
     expire: 2020/01/01
     ID revalidation owner: ID revalidation owner information
     ——————————————————
     title: ID : NAME 2
     expire: 2020/02/10
     ID revalidation owner: ID revalidation owner information
     ——————————————————
     title: ID : NAME 3
     expire: 2020/03/21
     ID revalidation owner: ID revalidation owner information
     ——————————————————
     title: ID : NAME 4
     expire: 2020/04/30
     ID revalidation owner: ID revalidation owner information
 ~~~

 * As a **CSV file**

  ~~~
  $ idchecker check --dir=./
  ~~~
  After the command is executed, a file called **report_d-m-Y_H-M-S.csv** containing the same information in the view of the table will appear in the **[specified directory](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard)**.

> As described in the usage section, you can additionally add the **--notes** option to include notes from 1Password records in the report

## Additional info
>The app is currently under development. The app may contain bugs. **Use at your own risk**.

## Contributing

1.  Fork it.
2.  Create your feature branch:  `git checkout -b my-new-feature`
3.  Commit your changes:  `git commit -am 'Add some feature'`
4.  Push to the branch:  `git push origin my-new-feature`
5.  Submit a pull request

## License
The MIT License (MIT)

Copyright (c) 2021 Mikalai Lisitsa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
