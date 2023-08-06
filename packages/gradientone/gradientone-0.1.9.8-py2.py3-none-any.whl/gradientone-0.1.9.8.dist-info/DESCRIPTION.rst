Gateway Client
===============
The client code connecting test and measurement devices to the cloud.

**Warning:**
Currently this client software is intended to only run on pre-configured GradientOne machines. Running this without a properly configured machine may result in unexpected behavior. Use at your own risk.

Set Config File
------------------

It's important to set up your config file before running the module. After installing with pip, a **/etc/gradientone.gradient_one.cfg.sample** file is created. Edit the variables to include the GATEWAY_AUTH_TOKEN and change variable names to match your particular configuration. Then change the file name back to **/etc/gradient_one.cfg** before running the client.

$ sudo cp gradient_one.cfg.sample /etc/gradient_one.cfg

Usage
------------------

It's recommended to create a 'client' directory and execute from there::

$ mkdir ~/client
$ cd ~/client
$ sudo gradientone

More Info
----------
For more information visit: http://www.gradientone.com/


