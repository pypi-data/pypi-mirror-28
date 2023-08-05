import requests_mock
import unittest

from glance_check.shell import GlanceCheck
import glance_check.exception as glance_check_exception


class TestGlanceCheck(unittest.TestCase):

    def setUp(self):
        self.imageid = "00000000-0000-0000-0000-000000000000"
        self.imageurl = "http://127.0.0.1:9292"
        self.creds = {"os_auth_url": "http://127.0.0.1:5000/v2.0",
                      "os_username": "testusername",
                      "os_tenant": "testtenant",
                      "os_password": "testpassword"}

    def test_check_http_connection_success(self):
        check = GlanceCheck(self.creds, self.imageid, self.imageurl)
        with requests_mock.Mocker() as m:
            m.get(self.imageurl, status_code=300)
            self.assertFalse(check.check_connection())

    def test_check_http_connection_failure(self):
        check = GlanceCheck(self.creds, self.imageid, self.imageurl)
        with requests_mock.Mocker() as m:
            m.get(self.imageurl, status_code=500)
            with self.assertRaises(
                    glance_check_exception.CheckConnectionError):
                check.check_connection()

    def test_check_create_image_success(self):
        check = GlanceCheck(self.creds, self.imageid, self.imageurl)
        with requests_mock.Mocker() as m:
            m.post(("%s/v2/images" % self.imageurl),
                   status_code=201)
            self.assertFalse(check.check_create_image('testtoken'))

    def test_check_create_image_duplicate(self):
        check = GlanceCheck(self.creds, self.imageid, self.imageurl)
        with requests_mock.Mocker() as m:
            m.post(("%s/v2/images" % self.imageurl),
                   status_code=409)
            with self.assertRaises(
                    glance_check_exception.TestImageAlreadyExistsError):
                check.check_create_image('testtoken')

    def test_check_create_image_failure(self):
        check = GlanceCheck(self.creds, self.imageid, self.imageurl)
        with requests_mock.Mocker() as m:
            m.post(("%s/v2/images" % self.imageurl),
                   status_code=500)
            with self.assertRaises(glance_check_exception.CreateImageError):
                check.check_create_image('testtoken')

    def test_check_get_image_success(self):
        check = GlanceCheck(self.creds, self.imageid, self.imageurl)
        with requests_mock.Mocker() as m:
            m.get(("%s/v2/images/%s"
                   % (self.imageurl, self.imageid)), status_code=200)
            self.assertFalse(check.check_get_image('testtoken'))

    def test_check_get_image_failure(self):
        check = GlanceCheck(self.creds, self.imageid, self.imageurl)
        with requests_mock.Mocker() as m:
            m.get(("%s/v2/images/%s"
                   % (self.imageurl, self.imageid)), status_code=500)
            with self.assertRaises(glance_check_exception.GetImageError):
                check.check_get_image('testtoken')

    def test_check_update_image_success(self):
        check = GlanceCheck(self.creds, self.imageid, self.imageurl)
        with requests_mock.Mocker() as m:
            m.patch(("%s/v2/images/%s" %
                     (self.imageurl, self.imageid)), status_code=200)
            self.assertFalse(check.check_update_image('testtoken'))

    def test_check_update_image_failure(self):
        check = GlanceCheck(self.creds, self.imageid, self.imageurl)
        with requests_mock.Mocker() as m:
            m.patch(("%s/v2/images/%s" %
                     (self.imageurl, self.imageid)), status_code=500)
            with self.assertRaises(glance_check_exception.UpdateImageError):
                check.check_update_image('testtoken')
