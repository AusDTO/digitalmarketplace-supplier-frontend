# coding=utf-8

import mock
from nose.tools import assert_equal, assert_true
from .helpers import BaseApplicationTest
from dmutils.apiclient.errors import HTTPError


class TestApplication(BaseApplicationTest):
    def setup(self):
        super(TestApplication, self).setup()

    def test_response_headers(self):
        response = self.client.get('/suppliers/login')

        assert 200 == response.status_code
        assert (
            response.headers['cache-control'] ==
            "no-cache"
        )

    def test_url_with_non_canonical_trailing_slash(self):
        response = self.client.get('/suppliers/')
        assert 301 == response.status_code
        assert "http://localhost/suppliers" == response.location

    def test_404(self):
        res = self.client.get('/service/1234')
        assert_equal(404, res.status_code)
        assert_true(
            "Check you've entered the correct web "
            "address or start again on the Digital Marketplace homepage."
            in res.get_data(as_text=True))
        assert_true(
            "If you can't find what you're looking for, contact us at "
            "<a href=\"mailto:enquiries@digitalmarketplace.service.gov.uk?"
            "subject=Digital%20Marketplace%20feedback\" title=\"Please "
            "send feedback to enquiries@digitalmarketplace.service.gov.uk\">"
            "enquiries@digitalmarketplace.service.gov.uk</a>"
            in res.get_data(as_text=True))

    @mock.patch('app.main.views.services.data_api_client')
    def test_503(self, data_api_client):
        with self.app.test_client():
            self.login()

            data_api_client.get_supplier.side_effect = HTTPError('API is down')
            self.app.config['DEBUG'] = False

            res = self.client.get('/suppliers')
            assert_equal(503, res.status_code)
            assert_true(
                "Sorry, we're experiencing technical difficulties"
                in res.get_data(as_text=True))
            assert_true(
                "Try again later."
                in res.get_data(as_text=True))

    def test_header_xframeoptions_set_to_deny(self):
        res = self.client.get('/suppliers/login')
        assert 200 == res.status_code
        assert 'DENY', res.headers['X-Frame-Options']

    def test_should_use_local_cookie_page_on_cookie_message(self):
        res = self.client.get('/suppliers/login')
        assert_equal(200, res.status_code)
        assert_true(
            '<p>GOV.UK uses cookies to make the site simpler. <a href="/cookies">Find out more about cookies</a></p>'
            in res.get_data(as_text=True)
        )
