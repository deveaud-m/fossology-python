# Copyright 2019-2021 Siemens AG
# SPDX-License-Identifier: MIT

from fossology import Fossology
from fossology.exceptions import FossologyApiError
from fossology.obj import AccessLevel, SearchTypes, Upload


def delete_upload(foss: Fossology, upload: Upload):
    foss.delete_upload(upload)
    try:
        foss.detail_upload(upload, wait_time=2)
    except FossologyApiError:
        # Upload has been deleted
        pass


def test_upload_from_vcs(foss: Fossology):
    vcs = {
        "vcsType": "git",
        "vcsUrl": "https://github.com/fossology/fossology-python",
        "vcsName": "fossology-python-github-master",
        "vcsUsername": "",
        "vcsPassword": "",
    }
    vcs_upload = foss.upload_file(
        foss.rootFolder,
        vcs=vcs,
        description="Test upload from github repository via python lib",
        access_level=AccessLevel.PUBLIC,
        ignore_scm=False,
        wait_time=5,
    )
    assert vcs_upload.uploadname == vcs["vcsName"]
    # FIXME option ignore_scm does not work currently
    search_result = foss.search(
        searchType=SearchTypes.DIRECTORIES,
        filename=".git",
    )
    assert not search_result
    # Cleanup
    delete_upload(foss, vcs_upload)


def test_upload_from_url(foss: Fossology):
    url = {
        "url": "https://github.com/fossology/fossology-python/archive/master.zip",
        "name": "fossology-python-master.zip",
        "accept": "zip",
        "reject": "",
        "maxRecursionDepth": "1",
    }
    url_upload = foss.upload_file(
        foss.rootFolder,
        url=url,
        description="Test upload from url via python lib",
        access_level=AccessLevel.PUBLIC,
        wait_time=5,
    )
    assert url_upload.uploadname == url["name"]
    # Cleanup
    delete_upload(foss, url_upload)


def test_upload_from_server(foss: Fossology):
    server = {
        "path": "/tmp/base-files-11",
        "name": "base-files-11",
    }
    server_upload = foss.upload_file(
        foss.rootFolder,
        server=server,
        description="Test upload from server via python lib",
        access_level=AccessLevel.PUBLIC,
        apply_global=True,
        wait_time=5,
    )
    assert server_upload.uploadname == server["name"]

    # Cleanup
    delete_upload(foss, server_upload)
