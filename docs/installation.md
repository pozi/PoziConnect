# Pozi Connect Installation

## Instructions

1. go to [https://github.com/groundtruth/PoziConnect/releases/latest](https://github.com/groundtruth/PoziConnect/releases/latest)
2. click on the link to the .msi file to download the installer
3. run the installer
4. change the default path to the desired PoziConnect location on your network (pick the location of the existing installation if you have previously installed it)
5. follow the prompts to complete the installation

<img src="http://i.imgur.com/yvkIfL9.png" alt="Pozi Connect Setup" width="350">

### Customise Configuration

You can customise the Pozi Connect drop-down task list to display only the tasks that you're interested in.

The `PoziConnect\PoziConnect.site.ini` file contains filters to specifically include or exclude tasks. Open the file in a text editor, and specify the filter. For example, if you only want to display tasks that relate to 'Glen Eira', update the file as follows:

```
[Settings]
Include: Glen Eira
Exclude:
```

You can enter multiple filter terms, separated by commas. Save the file and exit.

This file should persist in your Pozi Connect application folder, so you need only do this step once, not every time you update the application or configuration.

## FAQ

### How does Pozi Connect connect to my corporate database?

Pozi Connect uses your PC's existing ODBC connection settings. It does not require any additional network or firewall configuration. It requires only that the user's PC has the appropriate DSN configured to access (read-only) the council's property database. Authentication can be based on a username/password or trusted connection (using Windows login name).

## Troubleshooting

### Pozi Connect fails to start

Download and install the [Microsoft Visual C++ 2008 Redistributable Package (x86)](http://www.microsoft.com/downloads/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en), and try running Pozi Connect again.

### Pozi Connect returns an 'Incorrect padding' error

If you encounter an error saying 'Incorrect padding', it may be because your database password contains a special character (such as '&') that interferes with the database connection string.

Reset your password so that it doesn't contain any special characters. (If your password needs to use at least one special character, use '#'.) 

### Cannot connect to data source

_In this example, we'll assume that we're trying to connect to a DSN called 'pthprod'._

Run the 32 bit ODBC setup wizard (instead of the standard DSN wizard in the Control Panel). At the Windows Start menu, type in cmd, then at the command-line prompt, type or paste in the following, then hit 'Enter':

`C:\Windows\SysWOW64\odbcad32.exe`

In the System DSN tab, check if there is a data source for 'pthprod'. If not, add a new DSN, using the same settings as your existing 64 bit one. It is recommended to use a different name for the new 32 bit DSN. For example, name it 'pthprod32' or similar so it can be distinguished from the existing DSN.

Open the relevant Pozi Connect config file (eg `PoziConnect\tasks\~Shared\M1 Shared - Import Pathway.ini` or equivalent client-specific task) in a text editor and update the DSN name:

```
Pathway_DSN: pthprod32
```

### Pozi Connect returns an error number 1073741512

Go into your `C:\Windows\System32` folder and see if there is a file called `libeay32.dll`. If so, rename it to `libeay32.bak`. Then try running Pozi Connect again.

(Rename the file back again when you've finished so that any other programs that may rely on it can use it.)
