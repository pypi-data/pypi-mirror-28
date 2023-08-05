# The Onion Box
_The Onion Box_ provides a web interface to monitor the operation of
a [Tor](https://www.torproject.org) node. It is able to monitor any Tor node operated as relay, as bridge and even as client - as long as it can establish a connection to the node and authenticate successfully.

The connection to the Tor node to be monitored may be established via a local `ControlSocket` or a `ControlPort` (local or remote). Advanced users may establish a connection via the Tor network to a node proving access to it's `ControlPort` by means of a Hidden Service - supporting on demand as well [Hidden Service Client Authorization](https://www.torproject.org/docs/tor-manual.html.en#HiddenServiceAuthorizeClient).

_The Onion Box_ supports whatever authentication method the Tor node provides.

A single instance of _The Onion Box_ is able to provide monitoring functionality for as many nodes as you like.

Above that, _The Onion Box_ is able to display Tor network status protocol data for any Tor node known by [Onionoo](http://onionoo.torproject.org).


[TOC levels=3 markdown bullet formatted hierarchy]: # "## Table of Contents"
## Table of Contents
- [The Web Interface](#the-web-interface)
    - [Header](#header)
    - [General Information](#general-information)
    - [Configuration](#configuration)
    - [Hidden Services](#hidden-services)
    - [Local Status](#local-status)
    - [Network Status](#network-status)
    - [Control Center](#control-center)
    - [Messages](#messages)
- [Getting Started](#getting-started)
    - [Scenario Assumption](#scenario-assumption)
    - [Supported environment](#supported-environment)
    - [System Preparation](#system-preparation)
    - [Installation](#installation)
    - [First Flight](#first-flight)
- [Dependencies](#dependencies)
- [Configuration by file](#configuration-by-file)
    - [Location](#location)
    - [Structure](#structure)
- [Command line parameters](#command-line-parameters)
- [Advanced Operations: Authentication](#advanced-operations-authentication)
    - [Cookie Authentication](#cookie-authentication)
    - [Password Authentication](#password-authentication)
    - [No Authentication](#no-authentication)
- [Advanced Operations: Control Interface](#advanced-operations-control-interface)
    - [Caution](#caution)
    - [ControlSocket](#controlsocket)
    - [ControlPort](#controlport)
    - [ControlPort via Proxy](#controlport-via-proxy)
- [Hidden Service Operations](#hidden-service-operations)
    - [Basic configuration](#basic-configuration)
    - [Access control](#access-control)
- [_The Onion Box_ as system service (aka daemon)](#the-onion-box-as-system-service-aka-daemon)
    - [... on FreeBSD](#-on-freebsd)
    - [... using init.d](#-using-initd)
    - [... using systemd](#-using-systemd)
- [Usage Monitoring](#usage-monitoring)
- [Q&A](#qa)
    - [I receive a _Not supported proxy scheme socks5h_ warning. What shall I do?](#i-receive-a-not-supported-proxy-scheme-socks5h-warning-what-shall-i-do)
- [Acknowledgments](#acknowledgments)

## The Web Interface
_The Onion Box_ generates a 'web page' that displays information regarding your Tor node. This information is split up into a number of sections. If a section is displayed and how the section looks like, depends on the data your Box received from the Tor node monitored or knows about it from the Tor network status protocol. The web interface is generated on demand based on the latest data available.

> Tip: If a dedicated section is not displayed, just reload the page. Press `F5` or `command + R` to re-run the page creation process.

The following chapters introduce each available section and provide some further details to explain the content displayed:

---

### Header
The Header of the page shows some basic information about the Tor node monitored.

![image](docs/images/header.png)

If you connected to this node via [password authentication](#password-authentication), you'll find a Logout Button in the upper right corner.

If your Box discovers that there is an update of it's code available, a button in the upper left corner is displayed, providing access to some further information - and a link to GitHub.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### General Information
The section _Host | General Information_ displays information regarding the host system.

![image](docs/images/generalinfo.png)

This section is only available if the Box is running at the same physical device as the Tor node monitored.

_Latest Reboot_ as well as _Temperature_ are only available on supported operating systems.

If the host provides several CPU cores, you may click on the _CPU Usage_ chart to get a popup window displaying a seperate usage chart for each core.

---

### Configuration
The section _Tor | Configuration_ displays the configuration parameters of the Tor node monitored:

![image](docs/images/configuration.png)

_Commandline_ lists the command line parameters used when launching the Tor node.

_Configuration Files_: A Tor node is configured by several sets of parameters. Those are Tor internal default settings, default settings defined in a configuration file referenced as _torrc.default_ (usually given by the Tor developers), user defined parameters (usually in a configuration file referenced as _torrc_) and finally parameters defined via the command line. The path to the two configuration files is indicated here.

The rest of this section displays all parameters that differ from the Tor internal default settings - except Hidden Service configuration settings (which are displayed in their own section).

If the curser hovers over the name of a configuration parameter, a hashtag is displayed providing a link to the Tor documentation. On mobile devices, you have to click on the name to make the hashtag appear.

There are some parameters that can be defined (e.g. via the command line), despite Tor doesn't signal back that those are set. The following table lists those parameters:

| Non-displayable Parameters |
|---|
| __OwningControllerProcess |

---

### Hidden Services
The section _Tor | Hidden Services_ displays the configuration parameters for the hidden service(s) of the Tor node monitored:

![image](docs/images/hidden.png)

This section is only available if at least one hidden service is configured on this Tor node.

---

### Local Status
The section _Tor | Local Status_ displays information that the Tor node monitored knows about itself and its hosting environment.

![image](docs/images/local.png)

 ---

### Network Status
The section _Tor | Network Status_ displays information provided by [Onionoo](http://onionoo.torproject.org), the Tor network status protocol, concerning the Tor node monitored.

![image](docs/images/network.png)

Those information are fetched regularly from Onionoo. If not available (which could happen when you connect to a node for the first time or when operating via slow connections), you will be asked to reload the page.

Only portions of this section are available if the Tor node monitored is operated as a bridge.

_Location_ by default provides the information Onionoo knows about the location of the Tor node & shows the location on a map.

![image](docs/images/location.png)

By special configuration you can advise the Box to query the location of the IP address of the Tor node monitored from a user provided GeoIP City DB.

_Bandwidth_ displays the bandwidth history data as known to Onionoo.

![image](docs/images/bandwidth.png)

The number of available charts depends on the age of the Tor node monitored. You may switch the chart displayed via the _History Charts_ buttons.

_Weights_ displays the weights history data as known to Onionoo.

![image](docs/images/weights.png)

The number of available charts depends on the age of the Tor node monitored. You may switch the chart displayed via the _History Charts_ buttons.

---

### Control Center
Do you intend to monitor more than one Tor node? Are you interested in the Oninooo data of other Tor nodes? The section _Box | Control Center_ provides that functionality.

![image](docs/images/control.png)

#### Search
Enter a search phrase - which should be a (part of a) nickname of a Tor node or a (portion of a) fingerprint - into the _Search_ field and press enter. This search phrase will be used to query Onionoo - and the result presented in a popup bubble. If the search was successful, you may click on the links provided to display the Tor network status protocol data of that Tor node.

#### Controlled Hosts
If you provided access control information for additional Tor nodes in the configuration file of your Box, those nodes are listed under _Controlled Hosts_. Click on the fingerprint and you will be connected to that Tor node.

---

### Messages
The section _Box | Messages_ displays the messages received from the Tor node(s) monitored and from your Box.

![image](docs/images/messages.png)

You can alter the noisiness of the Tor node monitored by mean of the _Level_ selector buttons. Be advised that it takes some seconds to forward a message level change to the node.
> By default, _INFO_ and _DEBUG_ level messages are not forwarded to the monitoring application. _INFO_ is babblative - and _DEBUG_ even more. Both levels create a lot of traffic. Use those settings with caution!

This section is only available for controlled nodes.

> The message system of _The Onion Box_ cannot be manipulated via the web interface. If you are interested in receiving _DEBUG_ or _TRACE_ message from your Box, you have to set the appropriate [command line](#command-line-parameters) parameter.

---

## Getting Started
This chapter leads you through the installation procedure of you own _Onion Box_.  
The level of detail provided here should allow everyone, being a Novice or an Expert in the world of Tor, to successfully set up his personal _Box_. If you encountered any issues - due to whichever reason - drop me a line and I will try to improve this description to meet your demands.

### Scenario Assumption
For the following tutorial I will assume a quite common scenario, the intension to install _The Onion Box_ on a Raspberry Pi with Raspbian running a Tor node. This makes it easier to explain the procedures given a precise use case rather than elaborating through all potentional
shoulds and coulds.
> If you encounter a situation that is significantly different from this scenario, let's discuss how to amend the description to cover those specialities.

So we assume that you're logged in as user **pi**, operating on the **PIXEL** desktop (which is the default Raspbian desktop). Your starting point should look like this:

<p  align="center"><img src='docs/images/raspbian.png' width='50%'></p>

### Supported environment
_The Onion Box_ is a Python application, developed with v2.7 and v3.6.

By default, it should operate successfully on every platform providing Python support. Confirmation can be given that it works properly in following environments:
- Bananian | [Jessie](https://github.com/ralphwetzel/theonionbox/issues/7#issuecomment-346902660)
- Debian | Jessie
- FreeBSD
- macOS | Darwin
- Raspbian | Jessie
- Unbutu 16.04
- Windows 10

The Python version you are operating with (per default), can be verifyed via a terminal / command line by the issuing `python --version`:
```
~ $ python --version
python 2.7.9
```
As said, this displays the version of the _default_ Python interpreter. Explicitely you may use as well `python2 --version` or `python3 --version` to ask for the version numbers of the dedicated releases.

_The Onion Box_ is designed to run with either Python > 2.7.9 or Python > 3.6. If _none_ of your Python versions fit these reqirements, check [the Python page](http://www.python.org) for procedures how to upgrade your installation. On a Linux system, you could e.g. run `apt-get` like
```
~ $ sudo apt-get install --upgrade python
~ $ sudo apt-get install --upgrade python3
```
to install the latest versions available in the repositories.

### System Preparation
I strongly recommend to run _The Onion Box_ in a [Python Virtual Environment](https://docs.python.org/3/tutorial/venv.html) . The additional effort is (almost) zero - yet you gain certainty that the environment is and stays perfect for operating your _Box_:

Open a terminal and start your system preparation by installing the Python _virtualenv_ package:
```
~ $ sudo pip install virtualenv
Collecting virtualenv
  Using cached virtualenv-15.1.0-py2.py3-none-any.whl
Installing collected packages: virtualenv
Successfully installed virtualenv-15.1.0
```
After this successfully completed, create the virtual environment for your _Box_ in a dedicated directory, e.g. `./theonionbox`:
> There is no need to exactly use `theonionbox` as the name for the directory to create the virtual environment in; thus choose whatever you like yet ensure that it is a valid directory name and not pre-occupied.
```
~ $ virtualenv theonionbox
New python executable in /home/pi/theonionbox/bin/python
Installing setuptools, pip, wheel...done.
```

As final step, activate now the virtual environment just created:
```
~ $ cd theonionbox
~/theonionbox $ source bin/activate
(theonionbox) ~/theonionbox $ 
```
> The fact that the virtual environment is activated is indicated by the name of the virtualenv in parentheses preceding the path info, e.g. here via `(theonionbox)`.

To **later** close the Virtual Environment, issue a `deactivate` command:
```
(theonionbox) ~/theonionbox $ deactivate
~/theonionbox $ 
```

### Installation
The latest release package of [_The Onion Box_](https://testpypi.python.org/pypi/theonionbox/) is always available in [PyPi](https://testpypi.python.org), the Python Package Index. You can download and install it with `pip`. Please ensure, that you're doing this within the virtual environment created for your _Box_; (re-)activate it if necessary:
```
~ $ cd theonionbox
~/theonionbox $ source bin/activate
(theonionbox) ~/theonionbox $ pip install theonionbox
```
Along with the the files for _The Onion Box_, all additional [dependencies](#dependencies) will be installed into the virtual environment you created. No changes will be made to _The World Outside_ and there is no need to operate this `pip` command as `root.
> Be aware that it might need some minutes to download and compile the requested packages and all their dependencies.

Please ensure that the installation process is performed without any error. You should read a line like
```
[...]
Successfully installed PySocks-1.6.8 apscheduler-2.1.2 bottle-0.12.13 certifi-2017.11.5 [...]
(theonionbox) ~/theonionbox $
```
as the final message. This indicates, that your _Box_ should now be ready for testing.

### First Flight
Type `theonionbox` to launch your _Box_ for the first time:
```
(theonionbox) ~/theonionbox $ theonionbox
```
Your Box will perform some steps to initialize and then wait for connections at `http://127.0.0.1:8080`. A typical startup sequence of a fresh installation of _The Onion Box_ looks like

```
16:09:07.688 The Onion Box: WebInterface to monitor Tor node operations.
16:09:07.692 Version v4.1 (stamp 2018....|15....)
16:09:07.693 Running on a Linux host.
16:09:07.695 Running with permissions of user 'pi'.
16:09:07.696 Python version is 2.7.13 (/home/pi/theonionbox/bin/python).
16:09:07.697 This seems to be a Python VirtualEnv.
16:09:07.728 No (valid) configuration file found; operating with default settings.
16:09:11.471 Temperature sensor information located in file system. Expect to get a chart!
16:09:11.473 Uptime information located. Expect to get a readout!
16:09:12.077 Ready to listen on http://127.0.0.1:8080/
16:09:12.153 Press Ctrl-C to quit!
```

At that stage, open a webbrowser from the PIXEL desktop and connect to your _Box_ at the given address (here: `http://127.0.0.1:8080`).  

It is yet very likely, that you'll receive an error message like this one:
<p  align="center"><img src='docs/images/connectionerror.png' width='80%'></p>

Don't be disappointed! As your _Box_ explained during it's launch procedure, it is
```
16:09:07.695 Running with permissions of user 'pi'.
```
Very likely your Tor node yet was (e.g. by default) configured to guard the access to it's `ControlPort` by `CookieAuthentication`. As user `pi` (in common scenarios) has no permission to read this cookie, your _Box_ fails to authenticate against your Tor node - and has to issue a Connection Error.
To compensate for that error and to comply with the Tor configuration setting, just launch your _Box_ with the same user that owns & controls your Tor node - which on Debian like systems usually is `debian-tor`:

> Remember: To stop the operation of your Box, press `Ctrl-C`!
```
(theonionbox) ~/theonionbox $ sudo -u debian-tor lib/theonionbox
```
> Please note that you now have to state the full (yet relative) path of `lib/theonionbox` to run the _Box_!

```
[...]
16:33:16.543 Running on a Linux host.
16:33:16.544 Running with permissions of user 'debian-tor'.
16:33:16.544 Python version is 2.7.13 (/home/pi/theonionbox/bin/python).
16:33:16.566 No (valid) configuration file found; operating with default settings.
16:33:20.314 Temperature sensor information located in file system. Expect to get a chart!
16:33:20.315 Uptime information located. Expect to get a readout!
[...]
```
> You might notice as well, that _The Onion Box_ is now unable to detect that it's running inside a virtual environment! This is technically correct, as issueing the `sudo -u` command breaks those boundaries.

As before, browse now to `http://127.0.0.1:8080` ... and enjoy monitoring your Tor node!


## Dependencies
_The Onion Box_ depends on some libraries develloped and provided by third parties. If you follow the [installation procedure](#installation) , `pip` will care to install all necessary packages for you.  
If you perform a non-`pip` (manual) installation (e.g. directly from the GitHub repository), you have to ensure that those dependencies are installed accordingly:

* [psutil](https://pypi.python.org/pypi/psutil)
* [stem](https://pypi.python.org/pypi/stem)
* [bottle](https://pypi.python.org/pypi/bottle)
* [APScheduler](https://pypi.python.org/pypi/apscheduler)
* [PySocks](https://pypi.python.org/pypi/PySocks)
* [tzlocal](https://pypi.python.org/pypi/tzlocal)

To operate the Box in an Python 2.7 environment, you need as well the [futures](https://pypi.python.org/pypi/futures/) module.

If you intend to use the advanced GeoIP2 functionality, you have to install as well the module [geoip2](https://pypi.python.org/pypi/geoip2).

If you intend to operate The Box in SSL mode, you have to install as well the module [ssl](https://pypi.python.org/pypi/ssl).


These modules are usually installed using `pip`, e.g.: `pip install psutil`

Please use always the latest version available for your Python release. Remember that you (usually) need to have root privileges to operate `pip`, e.g. `sudo -u pip install psutil`.  
My advice is yet to always operate within a [Python Virtual Environment](#system-preparation) - which eliminates the demand to run `pip` with root privileges.

> Check this [Q&A](#i-receive-a-not-supported-proxy-scheme-socks5h-warning-what-shall-i-do) if your `pip` installation is broken or if you receive a `socks5h proxy not supported` warning.

## Configuration by file

By design, _The Onion Box_ is able to detect a typical local Tor node installation and will connect without further preparation.

Therefore no configuration be necessary - if you are operating your node at `ControlPort 9051` (which is the default for a relay) or `ControlPort 9151` (the default for TorBrowser).

For all other situations, you may configure the way of operation of your _Box_ via a configuration file.

### Location
If you do not provide a dedicated `--config=<path>` to define the path to a configuration file via the [command line](#command-line-parameters), _The Onion Box_ checks for availability of a file named `theonionbox.cfg` at one of the following locations (in the given order):
* if launched from a Python Virtual Environment, in a directory named `config` below the root directory of the virtual environment: `$VIRTUAL_ENV/config/theonionbox.cfg`
* in the same directory as `theonionbox.py`: `./theonionbox.cfg`
* in a directory named `config` below the directory of `theonionbox.py`: `./config/theonionbox.cfg`

If you've saved your configuration file at one of those locations, yet your _Box_ still states `No (valid) configuration file found.`, you might use the [-d command line parameter](#command-line-parameters) to enable the _Debug_ mode. This will trigger _The Onion Box_ to emit the absolute search paths it's checking for the configuration files:

```
(theonionbox) ~/theonionbox $ theonionbox -d
        17:57:10.551 The Onion Box: WebInterface to monitor Tor node operations.
[...]
[DEBUG] 17:57:10.590 theonionbox.py[391]: No configuration file found at '/home/pi/theonionbox/config/theonionbox.cfg'
[DEBUG] 17:57:10.594 theonionbox.py[391]: No configuration file found at '/home/pi/theonionbox/lib/python2.7/site-packages/theonionbox/theonionbox.cfg'
[DEBUG] 17:57:10.596 theonionbox.py[391]: No configuration file found at '/home/pi/theonionbox/lib/python2.7/site-packages/theonionbox/config/theonionbox.cfg'
```

### Structure
The configuration file of _The Onion Box_ is a simple text file "ini-style". A template of that file is available as [`./config/theonionbox.example`](./theonionbox/config/theonionbox.example) in the directory of `theonionbox.py`.

#### Section `[config]`
```
[config]
## v4.0 will only support version = 2
protocol = 2
```
_The Onion Box_ as of version 4 only supports configuration file protocol `2`.

#### Section `[TheOnionBox]`
```
[TheOnionBox]
## Address of your Onion Box:
## This defaults to 0.0.0.0 to listen on all interfaces.
# host = 0.0.0.0
## If 'localhost', connections are limited to the local system.
# host = localhost
## Of course you may define a dedicated IP4 address as well.
# host = your.IP.4.address

## Port for the Web Server
## Defaults to 8080, which should be fine in most cases!
# port = 8080

## To define the lower threshold for the notification system:
## Messages (of the Box) with at least this level will be forwarded to the attached clients.
## Possible setting are DEBUG, INFO, NOTICE, WARNING, ERROR
## Defaults to NOTICE, case insensitive
## To 'DEBUG' or 'TRACE' the box you have to set the respective commandline parameters!
# message_level = NOTICE

## Per default, the Box operates at the root level of a domain e.g. http://localhost:8080/.
## If you intend to operate it (behind a proxy!) at a deeper level (e.g. @ http://my.server.com/theonionbox/)
## you have to define that base path here. You are not limited to a single path element.
## Please assure that this is an absolute filepath yet without the domain:port, beginning with a leading slash,
## no trailing slash, no quotation marks:
# base_path = /theonionbox

## The acceptable duration in seconds between two communication events of a client to the Box.
## If this duration is exceeded, the Box will expire the session. Default is 300 (seconds).
# session_ttl = 300
## Note: This is applicable for login procedures as well as monitoring activities.
## Note: The minimum duration accepted == 30, max == 3600. Values will be forced into that range.

## Shall we operate with SSL?
## Note: To actually make this running, you have to create a valid ssl certificate first:
## So run e.g.
## openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
##
## DON'T distribute this combined private/public key to clients!
## (see http://www.piware.de/2011/01/creating-an-https-server-in-python/#comment-11380)
##
## ssl = yes    # deprecated 20170218
## Just set ssl_certificate & ssl_key to enable ssl mode!
## The file that holds the Certificate!
# ssl_certificate = server.pem
## The file that holds the Key!
# ssl_key = private_key.pem

## When a NTP server is provided
## we use it's time signal to compensate for the server's clock deviations
# ntp_server = pool.ntp.org
# ntp_server = fritz.box

## Tor ships with the GeoIPLight2 Country DB
## If you're interested in a more precise indication, you should install the GeoIP City DB
## e.g. from http://dev.maxmind.com/geoip/geoip2/geolite2/ and define here the path to the db file.
## Both flavours (Full or Light) are supported.
# geoip2_city = path/to/geoip2/city/db.mmdb
## Be aware that you need to install python module 'geoip2' as well to access those information.
```

#### Section `[Tor]`
These are the parameters to connect and authenticate to your "primary" (or first or main) Tor node to be monitored.
```
[Tor]
## How shall we establish the connection to your primary (controlled) Tor node?
## => via a ControlSocket (define additionally 'socket' parameter):
# control = socket
## => via a ControlPort (define additionally 'host' & 'port' parameter):
# control = port
## => via a Proxy (define a proxy via the [Proxy] section and set 'host' to an address reachable through this proxy):
# control = proxy
## Note: This defaults to control = port if not defined!

## Address of this Tor instance
## Do NOT use 'localhost' but 127.0.0.1 to connect locally
## Defaults to 127.0.0.1
# host = 127.0.0.1

## ControlPort of this Tor instance
## Default for a Relay (or Bridge)
# port = 9051
## Default for a TorBrowser
# port = 9151
## You may use 'default' (port = default) to test for 9051 (relay default) and 9151 (browser default)
# port = default
## Note: This defaults to port = default if not defined!

## ControlSocket of this Tor instance
# socket = /var/run/tor/control

## Timeout when connecting to Tor.
## Usually the connection should be established very quick;
## you may increase this if connecting to very remote systems.
# timeout = 5

## The Number of Seconds we keep the connection to
## Tor open after the last user disconnected.
## Hint: The minimum reasonable TTL is > 30(s)
## Defaults to 30 (seconds)
## eg. 1 day
# ttl = 86400
## eg. 1 hour
# ttl = 3600
## eg. forever
# ttl = -1

## Switches to preserve the messages of the Relay
## Up to 400 messages (total) will be preserved
## The severity of these messages can be defined here
## There's one switch for ERR, WARN & NOTICE
## The default setting is 'on' for all of these
## There's NO switch for INFO & DEBUG (as this would flood the memory without true value)
## Live - transmission of messages can be switched on/off in the client
# tor_preserve_ERR = no
# tor_preserve_WARN = no
# tor_preserve_NOTICE = no
```

#### Section `[TorProxy]`
```
[TorProxy]
## Note: Operation via a proxy given by a unix domain socket is (as of 04/2017) not supported!

## If you establish connection cookies for hosts to be controlled via the control center, there is the need
## to verify that those cookies are defined. To perform the verification, we need valid control port
## settings of the node acting as proxy:
## How shall we establish the connection to the node?
## => via a ControlSocket (define additionally 'socket' parameter):
# control = socket
## => via a ControlPort (define additionally 'port' parameter):
# control = port
## You may use control = default to operate with [Tor]control
## Note: This defaults to control = default if not defined!

## Address of the proxy to use
## Do NOT use 'localhost' but 127.0.0.1 to connect locally
## You may use 'default' (host = default) to use [Tor]host
# host = default
# host = 127.0.0.1
## Note: This defaults to host = default if not defined!

## Port for the proxy
## Default for a Relay (or Bridge)
# proxy = 9050
## Default for a Tor Browser
# proxy = 9150
## You may use 'default' (proxy = default) to test for 9050 (relay default) and 9150 (browser default)
# proxy = default
## Note: This defaults to proxy = default if not defined!

## ControlPort of the proxy Tor node
## Default for a Relay (or Bridge)
# port = 9051
## Default for a Tor Browser
# port = 9151
## You may use 'default' (port = default) to test for 9050 (relay default) and 9150 (browser default)
# port = default
## Note: This defaults to port = default if not defined!

## ControlSocket of the proxy Tor node
# socket = /var/run/tor/control
## You may use 'default' (socket = default) to use [Tor]socket
# socket = default
## Note: This defaults to socket = default if not defined!
```

#### One dedicated section for each additional _Controlled Host_
For each Tor node you intend to monitor - **but not** for the  "primary" node configured already in section `[Tor]` - you have to add a dedicated section proving the access data for its `ControlPort`.

> You must not name any of the following sections 'config', 'TheOnionBox', 'Tor' or 'TorProxy'.

```
#####
## Those are the Tor nodes to be controlled with the control center
## Note: You must not name any of the following sections 'config', 'TheOnionBox', 'Tor' or 'TorProxy'.


## Define one section per node:
# [myControlledNode]

## Alternatively: Beginning the section identifier with '#' indicates a nickname;
## if you later omit the 'nick' parameter, the nickname will be derived from the section identifier.
# [#myControlledNode]
## If you intend to define several ways to connect to this node,
## add whatever you like after a ':' to distinguish the sections:
# [#myControlledNode:2]

## Alternatively: You can use the fingerprint (with preceding '$') as section identifier.
## Ensure a length of 41 characters: '$' + fingerprint[40];
## if you later omit the 'fp' parameter, the fingerprint will be derived from the section identifier.
# [$5COOL5C30AXX4B3DE460815323967087ZZ53D947]
## If you intend to define several ways to connect to this node,
## add whatever you like after a ':' to distinguish the sections:
# [$5COOL5C30AXX4B3DE460815323967087ZZ53D947:2]


## How shall we establish the connection to this node?
## => via a ControlSocket (define additionally 'socket' parameter):
# control = socket
## => via a ControlPort (define additionally 'host' & 'port' parameter):
# control = port
## => via a Proxy (define a proxy via the [Proxy] section and set 'host' to an address reachable through this proxy):
# control = proxy
## Note: There is no default setting. If not defined, this section (and thus the node) will be ignored.

## IP Address of this Tor node
# host = 127.0.0.1
## You may as well define an onion or http address
# host = takeonionaddress.onion
## Note: There is no default setting.

## ControlPort of this Tor node
## Default for a Relay (or Bridge)
# port = 9051
## Note: There is no default setting.

## This is only relevant for very rare setups - yet if you like, you may use it!
## ControlSocket of this Tor node
# socket = /var/run/tor/control
## Note: There is no default setting.

## Hidden Service connections my be secured by definition of a authorization cookie.
## To operate via those connections, you may define this cookie here.
## For further details refer to 'HiddenServiceAuthorizeClient' on https://www.torproject.org/docs/tor-manual.html
# cookie = xuseyourcookieherexTOB
## The Box will ensure that the cookie is registered before establishing the connection.
## Note: There is no default setting.

## The nickname of this node
# nick = myControlledNode
## Defining a nickname here overrides a nickname defined as the name of the section.
## Note: The Box is able to retrieve the nickname itself,
##       yet defining nickname (and fingerprint) parameters saves onionoo queries.
## Note: There is no default setting.

## The fingerprint of this node
# fp = $5COOL5C30AXX4B3DE460815323967087ZZ53D947
## Defining a fingerprint here overrides a fingerprint defined as the name of the section.
## Note: The Box is able to retrieve the fingerprint itself,
##       yet defining fingerprint (and nickname) parameters saves onionoo queries.
## Note: There is no default setting.
```

## Command line parameters
_The Onion Box_ may be configured by a small number of commandline parameters:

```
-c <path> | --config=<path>: Provide path & name of configuration file.
                             Note: This is only necessary when NOT using
                             './theonionbox.cfg' or './config/theonionbox.cfg'.
-d | --debug: Switch on DEBUG mode.
-t | --trace: Switch on TRACE mode (which is more verbose than DEBUG mode).
-h | --help: Prints this information.
-m <mode> | --mode=<mode>: Configure The Box to run as 'service'.

```

`DEBUG` mode only affects the Box' core code. It forwards the debug messages of _The Onion Box_ to the console or the log file. If you encounter any problems, you may enable `DEBUG` mode to check what's happing.

`TRACE` additionally forwards debug level messages of `bottle` (the WSGI micro web-framework used by the Box) and trace level messages of `stem` (the Tor controller library). This mode is really noisy ... and the ultimate lever to follow the operation of _The Onion Box_ in case of problems.


## Advanced Operations: Authentication
Monitoring a Tor node in the end just demands two prerequisites: Access to an interface to control the node and a way to authenticate against the node. Therefore _Advanced Operations_ is all about the different ways to provide a [control interface](#advanced-operations-control-interface) and the different ways of **authentication**.

To clarify one topic upfront: You don't need to tell your Box the way of authentication it shall use. This topic will transparently be negotiated between the Tor node and the Box.

### Cookie Authentication
By default (defined in the configuration file [`torrc.default`](#configuration)) a Tor node offers _Cookie Authentication_ as standard authentication method.  

According to the Tor manual, when using _Cookie Authentication_, the Tor node allows "connections on the control port when the connecting process knows the contents of a file named `control_auth_cookie`, which Tor will create in its data directory".  
This implies that _Cookie Authentication_ can only be used locally - which means that this authentication method is only suitable if you have installed _The Onion Box_ on the same system that hosts the Tor node you intend to monitor.  
To access `control_auth_cookie`, your Box needs to have the correct privileges. This can be achieved most easily by running it as the same user as the Tor node (which e.g. is _debian-tor_ on Debian systems):
```
sudo -u debian-tor python theonionbox.py
```

### Password Authentication
By definition of the `HashedControlPassword` parameter in the `torrc` configuration file of your Tor node, you can advise Tor to operate with _Password Authentication_.

> To create a password hash of _mypassword_ issue a `sudo tor --hash-password mypassword`.

_Password Authentication_ provides a way of access control to your Tor node even if you monitor a remote node.

If your Box discovers that _Password Authentication_ is required, it will ask for that password providing a Login Screen:

![Login Screen](docs/images/login.png)


### No Authentication
There might be situations, where access control to the ControlPort is not demanded or even obstructive.
In that case it may be necessary to explicitely turn off _Cookie Authentication_ in your `torrc` - as it might be enabled by default:
```
CookieAuthentication 0
```

## Advanced Operations: Control Interface
Monitoring a Tor node in the end just demands two prerequisites: Access to an interface to control the node and a way to authenticate against the node. Therefore _Advanced Operations_ is all about the different ways to provide a **control interface** and the different ways of [authentication](#advanced-operations-authentication) .

### Caution
On Unix or Unix-like systems it is preferred to use a `ControlSocket` rather than a `ControlPort` as interface to the control port of a local Tor node.

Providing a socket ensures that only a process local to the system is able to connect.

If you mis-configure a `ControlPort`, you might endanger the security of your system; if you mis-configure a `ControlSocket`, you just cannot connect.

### ControlSocket
By default (defined in the configuration file [`torrc.default`](#configuration)) a Tor node offers a `ControlSocket` as standard controlling interface (at least on Unix and Unix-like systems). This default socket is e.g. defined as `/var/run/tor/control`.

A `ControlSocket` can only been accessed locally; therefore you need to install _The Onion Box_ on the same system that hosts the Tor node you intend to monitor.
To access a `ControlSocket` the process trying to connect needs to have the correct privileges. This can be achieved most easily by running your Box as the same user as the Tor node (which e.g. is _debian-tor_ on Debian systems): `sudo -u debian-tor python theonionbox.py`

To instruct your Box to connect to a local ControlSocket define the following parameters:
```
[Tor]
control = socket
socket = /var/run/tor/control
```

You can use the same parameter language - if applicable - in `[TorProxy]` or when defining the connection settings of a _Controlled Host_.

### ControlPort
Configuring a `ControlPort` as controlling interface for a Tor node is as simple as defining
```
ControlPort 9051
```
into the node's `torrc` file - and restarting Tor. Almost every _Beginner's guide to setup a Tor relay_ explains how to achieve this.

To instruct _The Onion Box_ to connect to a `ControlPort` interface, you have to define two parameters, the `host` and the `port`.

> A `ControlPort` - in the sense of this documentation - is **not** a `unix://path` unix domain socket definition yet only a port number according to internet protocol specification. If you intend to operate with an unix domain socket interface, follow the instructions in the chapter [ControlSocket](#controlsocket) - even if you've defined that socket in `torrc` with parameter `ControlPort`.

`host` can be either an IP4-address or a hostname.
> `host` definition via IP6 address currently is not supported.

`port` has to be a number in the standard range of port numbers between 0 and 65535.

Thus use the following language in your Box' configuration file to instruct it to connect to a ControlPort:
```
[Tor]
control = port
host = 127.0.0.1
port = 9051
```

You may use `control=port` to connect to local (`host=127.0.0.1`) or remote (`host=www.my.torserver.com`) Tor nodes.

You can use the same parameter language - if applicable - in `[TheOnionBox]`, `[TorProxy]` or when defining the connection settings of a _Controlled Host_.

### ControlPort via Proxy
You can instruct your Box to connect to a remote host via the Tor network. Prerequisite for such an operation is the definition and availability of a Tor node as proxy server:

> You can enable a Tor node's `socks` proxy capabilities by defining a `SocksPort` in `torrc` - and restarting Tor.

Use the following language in your Box' configuration file to instruct it to connect to the ControlPort of a Tor node via the Tor network:
```
[Tor]
control = proxy
host = www.my.torserver.com
port = 9051
```

Be aware that this kind of setup is only limited useful, as the monitoring traffic exits the Tor network at an exit node and circulates into the open internet until it reaches the Tor node to be monitored.

You yet can unfold the full potential of this feature if you use it with a Tor node providing access to it's controlling interface by a [hidden service](#hidden-service-operations).


## Hidden Service Operations
_The Onion Box_ supports remote monitoring of a Tor node via the Tor notwork services. While it might be a bit more effort to set up such a connection, it provides the advantage that the whole traffic circulates only within the Tor eco system; there is no footprint of the monitoring activity in the open internet, adding a further layer of security to your operations.

### Basic configuration
To create that kind of connection, you have to prepare a hidden service that allows connection to the ControlPort of the Tor node to be monitored - by adding
```
HiddenServiceDir /var/lib/tor/theonionbox/
HiddenServicePort 9876 /var/run/tor/control
```
to this node's `torrc`.  
The first parameter of `HiddenServicePort` is the virtual ControlPort we'll connect to later.  
The second parameter of `HiddenServicePort` is the local controlling interface of the node - which might be a `ControlSocket` (as in the example shown) or a `ControlPort` (like `127.0.0.1:9051`).

After a restart of the Tor node by `sudo service tor restart`, you will find the onion address of your Hidden Service in `<HiddenServiceDir>/hostname`. The address usually is a 16 character string followed by `.onion`, e.g. _7an5onionad2res2.onion_.

To monitor this Tor node, add a dedicated section to the configuration file of your Box.
```
[MyProxyNode]
control=proxy
host=7an5onionad2res2.onion
port=9876
```
Provide as `host` parameter the onion address of your hidden service, as `port` the virtual ControlPort number you defined in the node's `torrc`.

This node will then be listed as a _Controlled Host_ in the [Control Center](#control-center) section of the web interface.

### Access control

As this Hidden Service configuration exposes the ControlPort of your Tor node to everyone who is able to connect to a Hidden Service, you have to consider a way to control the access to prevent misuse.

The first option is to enable [_Password Authentication_](#password-authentication) on the Tor node monitored.

Alternatively you could take advantage of Tor's _Hidden Service Client Authorization_ feature. In short, it restricts access to the Hidden Service to those clients that are able to provide the correct _Authorization Cookie_.

To enable this feature, edit again your Tor node's `torrc`. Alter the Hidden Service section to
```
HiddenServiceDir /var/lib/tor/theonionbox/
HiddenServicePort 9876 /var/run/tor/control
HiddenServiceAuthorizeClient stealth myBoxConnector
```
The second parameter of `HiddenServiceAuthorizeClient` is the **unique** username you intend to use to operate this connection.
> Please do **not** use _myBoxConnector_ as in the example above; this term definitely is no more _unique_ and therefore quite unsuitable to secure your connection!

After another restart of Tor via `sudo service tor restart`, you will find the authorization cookie for the given username in `<HiddenServiceDir>/hostname`.  
Take this cookie - a 22 character string, e.g. _xa3NyourCookY6herexTOB_ - and add it to the settings you defined for this connection in the configuration file of your Box:
```
[MyProxyNode]
control=proxy
host=7an5onionad2res2.onion
port=9876
cookie=xa3NyourCookY6herexTOB
```
Your Box will ensure that the configuration cookie will be registered prior to a connection attempt.

As this procedure limits the use of the Hidden Service - and thus the access to the control port of the node - to only those (trusted) users that are able to provide the right authorization cookie, you might consider switching off the standard authentication functionality of the node's control port via it's `torrc`:
```
CoookieAuthentication 0
# HashedControlPassword
```

## _The Onion Box_ as system service (aka daemon)
After you've ensured that your Box operates without issues, you can set it up to operate as a background application, which is the same as a system service or daemon. The steps to perform this differ depending on the technology used by your operating derivate.

When operated as a service, **log files** are per default stored into `<theonionbox-root-path>/log/theonionbox.log` and rotated regularly. If you create the directory `/var/log/theonionbox` and set the propper access rights for the user running `theonionbox.py`, the log files will be written there.

### ... on FreeBSD
Let's assume, you've stored your OnionBox files in a directory called `/usr/home/pi/theonionbox`. Your intension is to run The Box as user `pi` (which is by far better then operating it as `root`!).

* Change to the directory where you stored the OnionBox files: `cd /usr/home/pi/theonionbox`
* Ensure that `theonionbox.py` is executable: `sudo chmod 755 ./theonionbox.py`
* Change to the `FreeBSD` directory within `/usr/home/pi/theonionbox`: `cd FreeBSD`
* Within this directory you'll find the script [`theonionbox.sh`](FreeBSD/theonionbox.sh) prepared to launch your OnionBox as a background service.
* Ensure that you set the path to the OnionBox files and the user to run the service as intended. Therefore open the file with an editor (here we use _nano_): `nano theonionbox.sh`
* According to our assumptions above, set line 29 to `: ${theonionbox_dir="/usr/home/pi/theonionbox"}`.
* Additionally set line 28 to `: ${theonionbox_user="pi"}`.
* Close _nano_ and save the changes to `theonionbox.sh`. (Press _Strg+X_ then follow the instructions given!)
* Copy the altered init script to `/usr/local/etc/rc.d`: `sudo cp ./theonionbox.sh /usr/local/etc/rc.d/theonionbox`
* Change to `/usr/local/etc/rc.d`: `cd /usr/local/etc/rc.d`
* Make sure the script you've copied before to `/usr/local/etc/rc.d` is executable: `sudo chmod 755 ./theonionbox`
* Register this service to the system: `sudo echo 'theonionbox_enable="YES"' >>/etc/rc.conf`
* Check that everything works so far: Launch your Onion Box for the first time as a service `sudo service theonionbox start`. This should give you no error messages.
* Check that your Onion Box is active: `sudo service theonionbox status` should tell you `theonionbox is running as pid xxx.` ... yet might complain about a `$command_interpreter` mismatch - which isn't polite but doesn't hurt.
* That's it!

**Troubleshooting**
* Please ensure that `/usr/sbin/daemon` is a valid path. If not either edit `/usr/local/etc/rc.d/theonionbox` line 49 or create a symbolic link to your installation's path to `daemon` as `/usr/sbin/daemon`.
* `/usr/local/bin/python` should be defined as well being a symbolic link to the python version you intend to operate with.

### ... using init.d
Let's assume, you've stored your OnionBox files in a directory called `/home/pi/theonionbox`. Your intension is to run The Box as user `pi` (which is by far better then operating it as `root`!).

* Change to the directory where you stored the OnionBox files: `cd /home/pi/theonionbox`
* Ensure that `theonionbox.py` is executable: `sudo chmod 755 ./theonionbox.py`
* Change to the `init.d` directory within `/home/pi/theonionbox`: `cd init.d`
* Within this directory you'll find the init script [`theonionbox.sh`](init.d/theonionbox.sh) prepared to launch your OnionBox as a background service.
* Ensure that you set the path to the OnionBox files and the user to run the service as intended. Therefore open the file with an editor (here we use _nano_): `nano theonionbox.sh`
* According to our assumptions above, set line 19 to `DIR=/home/pi/theonionbox`.
* Additionally set line 28 to `DAEMON_USER=pi`.
* Close _nano_ and save the changes to `theonionbox.sh`. (Press _Strg+X_ then follow the instructions given!)
* Copy the altered init script to `/etc/init.d`: `sudo cp ./theonionbox.sh /etc/init.d`
* Change to `/etc/init.d`: `cd /etc/init.d`
* Make sure the script you've copied before to `/etc/init.d` is executable: `sudo chmod 755 ./theonionbox.sh`
* Register this service to the system: `sudo system daemon-reload`
* Check that everything works so far: Launch your Onion Box for the first time as a service `sudo ./theonionbox.sh start`. This should give you no error messages but feedback a nice \[OK\].
* Check that your Onion Box is active: `sudo ./theonionbox.sh status` should tell you `active (running)`.
* Finally run `sudo update-rc.d theonionbox.sh defaults` to link `theonionbox.sh` into init's default launch sequence.

### ... using systemd
- Create user `theonionbox`
- Install _The Onion Box_ to `~theonionbox` and `sudo chmod 755 ./theonionbox.py`
- Edit `~theonionbox/config/theonionbox.cfg`to your needs
- Create service file with `sudo vi /etc/systemd/system/theonionbox.service` with the following content:

```
# Run The Onion Box as background service
# https://github.com/ralphwetzel/theonionbox/

[Unit]
Description=The Onion Box
Documentation=https://github.com/ralphwetzel/theonionbox/wiki
After=network.target

[Service]
Type=simple
User=theonionbox
WorkingDirectory=~
ExecStart=/srv/theonionbox/theonionbox.py --mode=service
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
> Alternatively you could copy the file from [here](systemd/theonionbox.service).

- Start the new service with `sudo systemctl start theonionbox.service`
- If everything is okay, start the service on next boot with `sudo systemctl enable theonionbox.service`

## Usage Monitoring
To create a small survey of its usage, _The Onion Box_ sends the following information to `t527moy64zwxsfhb.onion`, the hidden service acting as _The Onion Box Update Service_ when requesting the latest version information of Tor and the Box:

- An UUID created newly each time during launch of the Box.
- The stamp of your Box release
- The name of the operating system hosting your Box
- The release information of the operating system hosting your Box

By intension these information are not at all sufficient to identify you (as a person) or the system hosting your Box. They just allow to estimate the number of concurrently running instances of _The Onion Box_ and the diversity of the underlying operating systems.

Please refer to [version.py](theonionbox/tob/version.py) to review the code:
```python
[...]

proxies = {
    'http': 'socks5h://' + proxy_address,
    'https': 'socks5h://' + proxy_address
}
payload = {
    'protocol': __VERSION_PROTOCOL__,
    'version': self.version,
    'system': self.system,
    'release': self.release
}

address = 'http://t527moy64zwxsfhb.onion/{}/check.html'.format(self.id)

r = None

try:
    r = requests.get(address, proxies=proxies, params=payload, timeout=10)
except Exception as exc:
    pass

[...]

```

# Troubleshooting
## Q&A
### I receive a _Not supported proxy scheme socks5h_ warning. What shall I do?
If you receive this message, your `requests` module installation most probably is outdated - and not supporting _socks5h_ proxy operations.

If you do the obvious thing and try to `pip install requests --upgrade`, you risk to destroy your `pip` functionality.

Therefore you should first  
`sudo easy_install -U pip` (Python 2.x)  
or  
`sudo easy_install3 -U pip` (Python 3.x)
to install the latest `pip` version **together with a very recent version of `requests`**.

> This works even if your `pip` installation is already broken and issuing e.g. an _IncompleteRead_ error.

After that, you could `pip install requests --upgrade` if you like, yet usually it shouldn't be necessary any more.

## Acknowledgments
Day by day it is a repetitive pleasure to learn from uncountable people who share their knowledge, their time and their work with the world. This section shall express my gratefulness to those who supported me solving issues I encountered during the last years. **Thank You!**

Łukasz Dziedzic (and his friends) for creating and publishing the great [Lato](https://latofonts.com) font family.

[SC. Phillips](http://www.scphillips.com) whose [Blog](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/) gave a perfect starting point when I tried to operate the Box as a background service.

All the people contributing to [StackOverflow](https://stackoverflow.com/)
who taught me Python by example.

[svengo](https://github.com/svengo) who [contributed](https://github.com/ralphwetzel/theonionbox/issues/24) the [procedure](#-using-systemd) to operate _The Onion Box_ as a daemon with systemd`.

<table>
  <tbody>
    <tr >
    <td width = "100px">
    <img src="docs/images/pclogo.svg" align = "center" alt="PyCharm"/>
    </td>
    <td>

The [JetBrains](http://www.jetbrains.com) team for their support to _The Onion Box_ providing an Open Source license of their gorgeous PyCharm IDE. If you run your own personal Open Source project, you may as well apply for a license [here](https://www.jetbrains.com/buy/opensource/?product=pycharm) (non affiliated link).
</td>
</tr>
  </tbody>
</table>


> I apologize sincerely being convinced it is impossible to mention everyone who gave me the opportunity to participate from his or her experience.  
Please raise your hand if you think someone should be added to this list!