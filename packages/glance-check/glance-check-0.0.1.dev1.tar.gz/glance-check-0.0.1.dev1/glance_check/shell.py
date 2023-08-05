#!/usr/bin/env python

import argparse
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import sys
import os

from glance_check.check import GlanceCheck


def main():
    parser = argparse.ArgumentParser(prog='GlanceCheck',
                                     description=('Checks if glance'
                                                  ' is running properly'))
    parser.add_argument("--connection",
                        "-c",
                        help=""
                        "Checks if a connection to glance can be established",
                        action="store_true")
    parser.add_argument("--createimage",
                        "-i",
                        help="Checks if an image can be created",
                        action="store_true")
    parser.add_argument("--getimage",
                        "-g",
                        help="Checks if an image can be retrieved",
                        action="store_true")
    parser.add_argument("--updateimage",
                        "-u",
                        help="Checks if image details can be updated",
                        action="store_true")
    parser.add_argument("--all",
                        "-a",
                        help="Runs all checks (except create image)",
                        action="store_true")
    parser.add_argument("--testimageid",
                        "-t",
                        help="Overrides the default test image id",
                        action="store",
                        default="00000000-0000-0000-0000-000000000000")
    parser.add_argument("--configfile",
                        "-C",
                        help="Specify a configuration file",
                        action="store",
                        default=("/etc/glance/glance-api.conf"))
    parser.add_argument("--envvar",
                        "-e",
                        help="Use environment variable configuration",
                        action="store_true")
    parser.add_argument("--verbose",
                        "-v",
                        help="Output verbose information to stderr",
                        action="store_true")
    args = parser.parse_args()

    def print_verbose(message):
        if args.verbose:
            sys.stderr.write("%s\n" % message)

    def exit(exit_code=1, message=None):
        if message:
            sys.stderr.write("%s\n" % message)
        sys.exit(exit_code)

    def get_creds(v2, v3):
        creds = None

        if v2['tenant'] is not None:
            creds = v2
            v2['project'] = v2['tenant']
            print_verbose("--tenant suggests v2")

        if v3['project'] is not None:
            creds = v3
            print_verbose("--project suggests v3")

        if creds is None:
            return None

        for key in creds:
            if creds[key] == "" or creds[key] is None:
                print_verbose("--%s is missing" % key)
                return None

        print_verbose("Using the following %s" % creds)
        return creds

    def get_config_args(configfile=None):
        print_verbose("Trying to get config file creds")
        print_verbose("-Config file passed in %s" % configfile)
        config = ConfigParser.RawConfigParser()
        if config.read([configfile,
                        "/opt/stack/service/glance-api/etc/glance-api.conf"]
                       ) == []:
            print_verbose("-No configfile found.")
            return None

        # This will get ignored in get_creds
        creds_v2 = {"tenant": None}
        try:
            creds_v2 = {"auth_url":  config.get("keystone_authtoken",
                                                "auth_uri"),
                        "username": config.get("keystone_authtoken",
                                               "admin_user"),
                        "tenant": config.get("keystone_authtoken",
                                             "admin_tenant_name"),
                        "password": config.get("keystone_authtoken",
                                               "admin_password")}
        except ConfigParser.NoSectionError:
            print_verbose("No section called keystone_authtoken in conf file")
            return None
        except ConfigParser.NoOptionError as e:
            print_verbose(e.message)

        # This will get ignored in get_creds
        creds_v3 = {"project": None}
        try:
            creds_v3 = {"auth_url":  config.get("keystone_authtoken",
                                                "auth_uri"),
                        "username": config.get("keystone_authtoken",
                                               "username"),
                        "project": config.get("keystone_authtoken",
                                              "project_name"),
                        "password": config.get("keystone_authtoken",
                                               "password")}
        except ConfigParser.NoOptionError as e:
            print_verbose(e.message)

        return get_creds(creds_v2, creds_v3)

    def get_environment_args():
        print_verbose("Trying to get creds from environment")
        creds_v2 = {"auth_url": os.environ.get('OS_AUTH_URL'),
                    "username": os.environ.get('OS_USERNAME'),
                    "tenant": os.environ.get('OS_TENANT_NAME'),
                    "password": os.environ.get('OS_PASSWORD'),
                    }

        creds_v3 = {"auth_url": os.environ.get('OS_AUTH_URL'),
                    "username": os.environ.get('OS_USERNAME'),
                    "project": os.environ.get('OS_PROJECT_NAME'),
                    "password": os.environ.get('OS_PASSWORD'),
                    }

        return get_creds(creds_v2, creds_v3)

    # Try the various places for credentials
    creds = get_config_args(args.configfile)
    if creds is None or args.envvar:
        creds = get_environment_args()
        if creds is None and args.envvar:
            exit(message="envvar was specified and no env creds were found")
    if creds is None:
        exit(message="No creds were found")

    # Create GlanceCheck
    check = GlanceCheck(creds, args.testimageid,)

    if args.connection:
        check.check_connection()

    if args.createimage:
        check.check_create_image()

    if args.getimage:
        check.check_get_image()

    if args.updateimage:
        check.check_update_image()

    if args.all:
        check.check_connection()
        check.check_create_image()
        check.check_get_image()
        check.check_update_image()

    exit(0)

if __name__ == "__main__":
    main()
