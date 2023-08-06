# -*- coding: utf-8 -*-
import logging

from .io import (create_structure, create_virtualenv, get_package_metadata,
                 setup_git, update_git)

logger = logging.getLogger(__name__)


def create(package_path, project_name=None, force=None, interactive=False, check_url=None, venv=None, **ignored_options):
    """Create a new python project

    Args:
        package_path (str): path to the package

    Returns:
        dict: metadata
    """
    non_interactive = not interactive
    metadata = get_package_metadata(
        package_path=package_path,
        project_name=project_name,
        accept_defaults=non_interactive,
        check_url=check_url)

    metadata = setup_git(package_metadata=metadata)
    metadata = create_structure(package_metadata=metadata, overwrite=force)
    metadata = update_git(package_metadata=metadata)
    if venv:
        metadata = create_virtualenv(package_metadata=metadata)
    return metadata
