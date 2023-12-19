# Copyright 2021 Siemens AG
# SPDX-License-Identifier: MIT

import pytest
import responses

from fossology import Fossology
from fossology.exceptions import FossologyApiError


def test_get_info(foss: Fossology):
    assert foss.info.name == "FOSSology API"
    assert foss.info.license.name == "GPL-2.0-only"
    assert foss.info.version


@responses.activate
def test_info_does_not_return_200(foss_server: str, foss: Fossology):
    responses.add(
        responses.GET,
        f"{foss_server}/api/v2/info",
        status=400,
    )
    with pytest.raises(FossologyApiError) as excinfo:
        foss.get_info()
        assert "Error while getting API info" in str(excinfo.value)


def test_get_health(foss: Fossology):
    assert foss.health.status == "OK"
    assert foss.health.scheduler.status == "OK"
    assert foss.health.db.status == "OK"


@responses.activate
def test_health_does_not_return_200(foss_server: str, foss: Fossology):
    responses.add(
        responses.GET,
        f"{foss_server}/api/v2/health",
        status=503,
    )
    with pytest.raises(FossologyApiError) as excinfo:
        foss.get_health()
        assert "Error while getting health info" in str(excinfo.value)
