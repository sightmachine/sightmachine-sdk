#!/usr/bin/env python
# coding: utf-8
"""Unit tests for URL utility functions"""

import pytest
from smsdk.utils import get_url
from smsdk.client_v0 import convert_to_valid_url


class TestGetUrl:
    """Test cases for get_url() function"""

    def test_get_url_without_path(self) -> None:
        """Existing behavior - no path"""
        url = get_url(
            protocol="https",
            tenant="demo",
            site_domain="sightmachine.io",
            port=None,
            base_path=None,
        )
        assert url == "https://demo.sightmachine.io"

    def test_get_url_with_path(self) -> None:
        """New behavior - with path"""
        url = get_url(
            protocol="https",
            tenant="demo",
            site_domain="sightmachine.io",
            port=None,
            base_path="/nested/one/two",
        )
        assert url == "https://demo.sightmachine.io/nested/one/two"

    def test_get_url_with_path_trailing_slash_removed(self) -> None:
        """Path normalization - trailing slash removed"""
        url = get_url(
            protocol="https",
            tenant="demo",
            site_domain="sightmachine.io",
            port=None,
            base_path="/nested/one/two/",
        )
        assert url == "https://demo.sightmachine.io/nested/one/two"

    def test_get_url_with_path_leading_slash_added(self) -> None:
        """Path normalization - leading slash added"""
        url = get_url(
            protocol="https",
            tenant="demo",
            site_domain="sightmachine.io",
            port=None,
            base_path="nested/one/two",
        )
        assert url == "https://demo.sightmachine.io/nested/one/two"

    def test_get_url_with_path_both_slashes_normalized(self) -> None:
        """Path normalization - both leading and trailing"""
        url = get_url(
            protocol="https",
            tenant="demo",
            site_domain="sightmachine.io",
            port=None,
            base_path="nested/one/two/",
        )
        assert url == "https://demo.sightmachine.io/nested/one/two"

    def test_get_url_with_port_and_path(self) -> None:
        """Port and path together"""
        url = get_url(
            protocol="http",
            tenant="demo",
            site_domain="sightmachine.io",
            port=8080,
            base_path="/nested",
        )
        assert url == "http://demo.sightmachine.io:8080/nested"

    def test_get_url_with_port_no_path(self) -> None:
        """Port without path - existing behavior"""
        url = get_url(
            protocol="http",
            tenant="demo",
            site_domain="sightmachine.io",
            port=8080,
            base_path=None,
        )
        assert url == "http://demo.sightmachine.io:8080"

    def test_get_url_with_empty_string_path(self) -> None:
        """Empty string path treated as no path"""
        url = get_url(
            protocol="https",
            tenant="demo",
            site_domain="sightmachine.io",
            port=None,
            base_path="",
        )
        assert url == "https://demo.sightmachine.io"

    def test_get_url_with_whitespace_path(self) -> None:
        """Whitespace-only path treated as no path"""
        url = get_url(
            protocol="https",
            tenant="demo",
            site_domain="sightmachine.io",
            port=None,
            base_path="   ",
        )
        assert url == "https://demo.sightmachine.io"

    def test_get_url_with_single_level_path(self) -> None:
        """Single level nested path"""
        url = get_url(
            protocol="https",
            tenant="demo",
            site_domain="sightmachine.io",
            port=None,
            base_path="/nested",
        )
        assert url == "https://demo.sightmachine.io/nested"

    def test_get_url_with_deep_nested_path(self) -> None:
        """Deep nested path"""
        url = get_url(
            protocol="https",
            tenant="demo",
            site_domain="sightmachine.io",
            port=None,
            base_path="/a/b/c/d/e",
        )
        assert url == "https://demo.sightmachine.io/a/b/c/d/e"


class TestConvertToValidUrl:
    """Test cases for convert_to_valid_url() function"""

    def test_convert_to_valid_url_extracts_path(self) -> None:
        """Extract path from input URL"""
        url, path = convert_to_valid_url("https://demo.sightmachine.io/nested/one/two")
        assert url == "https://demo.sightmachine.io"
        assert path == "/nested/one/two"

    def test_convert_to_valid_url_no_path(self) -> None:
        """No path in URL"""
        url, path = convert_to_valid_url("demo")
        assert url == "https://demo.sightmachine.io"
        assert path is None

    def test_convert_to_valid_url_with_protocol_no_path(self) -> None:
        """Full URL without path"""
        url, path = convert_to_valid_url("https://demo.sightmachine.io")
        assert url == "https://demo.sightmachine.io"
        assert path is None

    def test_convert_to_valid_url_extracts_trailing_slash_normalized(self) -> None:
        """Extract path with trailing slash - normalized"""
        url, path = convert_to_valid_url("https://demo.sightmachine.io/nested/one/two/")
        assert url == "https://demo.sightmachine.io"
        assert path == "/nested/one/two"

    def test_convert_to_valid_url_with_port_and_path(self) -> None:
        """Extract path with port specified"""
        url, path = convert_to_valid_url(
            "https://demo.sightmachine.io:8080/nested/path"
        )
        assert url == "https://demo.sightmachine.io:8080"
        assert path == "/nested/path"

    def test_convert_to_valid_url_simple_tenant_with_custom_domain(self) -> None:
        """Simple tenant with custom domain"""
        url, path = convert_to_valid_url("demo", default_domain="custom.io")
        assert url == "https://demo.custom.io"
        assert path is None

    def test_convert_to_valid_url_http_protocol(self) -> None:
        """HTTP protocol instead of HTTPS"""
        url, path = convert_to_valid_url("http://demo.sightmachine.io/nested")
        assert url == "http://demo.sightmachine.io"
        assert path == "/nested"

    def test_convert_to_valid_url_empty_path(self) -> None:
        """URL with trailing slash but no actual path"""
        url, path = convert_to_valid_url("https://demo.sightmachine.io/")
        assert url == "https://demo.sightmachine.io"
        assert path is None

    def test_convert_to_valid_url_single_level_path(self) -> None:
        """Single level path extraction"""
        url, path = convert_to_valid_url("demo.sightmachine.io/api")
        assert url == "https://demo.sightmachine.io"
        assert path == "/api"

    def test_convert_to_valid_url_adds_default_domain(self) -> None:
        """Adds default domain when not present"""
        url, path = convert_to_valid_url("demo/nested/path")
        assert url == "https://demo.sightmachine.io"
        assert path == "/nested/path"
