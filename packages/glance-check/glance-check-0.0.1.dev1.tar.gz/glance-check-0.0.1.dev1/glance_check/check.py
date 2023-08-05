import json
import requests
import sys

import glance_check.exception as exc


class GlanceCheck:

    def __init__(self, creds=None, imageid=None, os_image_url=None,
                 cacert=None, verbose=False):
        self.__imageid = imageid
        self.__image_url = os_image_url
        self.__auth_url = creds['os_auth_url']
        self.__username = creds['os_username']
        self.__tenant = creds['os_tenant']
        self.__password = creds['os_password']
        self.__cacert = cacert
        self.__verbose = verbose

    def print_verbose(self, message):
        if self.__verbose:
            sys.stderr.write("%s\n" % message)

    def check_create_image(self, token):
        self.print_verbose("Attempting to create image id: %s using the api"
                           " at %s" % (self.__imageid, self.__image_url))
        headers = {'X-Auth-Token': token}
        payload = json.dumps({"name":
                              "GlanceCheck test image",
                              "id":
                              self.__imageid,
                              "tags": [
                                  "test"
                              ]})
        request = requests.post(("%s/v2/images" % self.__image_url),
                                headers=headers, data=payload,
                                verify=self.__cacert)
        self.print_verbose(request.text)
        if not request.status_code == requests.codes.created:
            if request.status_code == requests.codes.conflict:
                raise exc.TestImageAlreadyExistsError()
            else:
                raise exc.CreateImageError(
                    request.status_code)

    def check_get_image(self, token):
        self.print_verbose("Attempting to download image id: %s using the"
                           " api at %s" % (self.__imageid, self.__image_url))
        headers = {'X-Auth-Token': token}
        request = requests.get(("%s/v2/images/%s" % (self.__image_url,
                               self.__imageid)),
                               headers=headers,
                               verify=self.__cacert)
        self.print_verbose(request.text)
        if not request.status_code == requests.codes.ok:
            if request.status_code == requests.codes.not_found:
                raise exc.TestImageNotFoundError()
            else:
                raise exc.GetImageError(
                    request.status_code)

    def check_connection(self):
        self.print_verbose("Attempting to connect to glance at %s"
                           % self.__image_url)
        request = requests.get(self.__image_url,
                               verify=self.__cacert)
        self.print_verbose(request.text)
        if not request.status_code == requests.codes.multiple_choices:
            raise exc.CheckConnectionError(
                request.status_code)

    def check_update_image(self, token):
        self.print_verbose("Attempting to update image id: %s using the api"
                           " at %s" % (self.__imageid, self.__image_url))
        headers = {'X-Auth-Token': token,
                   'Content-Type':
                   "application/openstack-images-v2.1-json-patch"}
        payload = json.dumps([{"path": "/foo", "value":
                             "bar", "op": "add"}])
        request = requests.patch(
            "%s/v2/images/%s" %
            (self.__image_url, self.__imageid),
            headers=headers, data=payload, verify=self.__cacert)
        self.print_verbose(request.text)
        if not request.status_code == requests.codes.ok:
            raise exc.UpdateImageError(
                request.status_code)

    def get_keystone_token_v2(self):
        self.print_verbose("Attempting to get a keystone token using v2 of"
                           " the api at %s" % self.__auth_url)
        payload = json.dumps({"auth":
                             {"tenantName":
                              self.__tenant,
                              "passwordCredentials":
                              {"username": self.__username,
                               "password":
                               self.__password}}})
        request = requests.post(("%s/tokens"
                                % self.__auth_url),
                                data=payload,
                                verify=self.__cacert)
        self.print_verbose(request.text)
        authdict = dict(request.json())
        return authdict['access']['token']['id']
