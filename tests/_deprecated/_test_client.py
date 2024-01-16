import pytest
import logging

from .client import create_gql_client


def test_client_read():
    client = create_gql_client()