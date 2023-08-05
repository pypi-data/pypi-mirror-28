Glance check

Tooling for glance operators to verify the
health of/diagnose their Glance service.

Usage: glance-check [-h] [--connection] [--createimage] [--getimage]
                   [--updateimage] [--all] [--testimageid TESTIMAGEID]
                   [--configfile CONFIGFILE] [--envvar]

optional arguments:
  -h, --help            show this help message and exit
  --connection, -c      Checks if a connection to glance can be established
  --createimage, -i     Checks if an image can be created
  --getimage, -g        Checks if an image can be retrieved
  --updateimage, -u     Checks if image details can be updated
  --all, -a             Runs all checks (except create image)
  --testimageid TESTIMAGEID, -t TESTIMAGEID
                        Overrides the default test image id
  --configfile CONFIGFILE, -C CONFIGFILE
                        Specify a configuration file
  --envvar, -e          Use environment variable configurationverrides the default test image id

The following environment variables must be set if environment variable configuration is used:

OS_AUTH_URL	keystone API URL
OS_TENANT_NAME	keystone tenant name
OS_USERNAME	keystone username
OS_PASSWORD	keystone password

