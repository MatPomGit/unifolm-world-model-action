"""Basic import tests to ensure package is properly structured."""

import pytest


def test_import_main_package():
    """Test that the main package can be imported."""
    import unifolm_wma
    assert hasattr(unifolm_wma, '__version__')


def test_import_data_module():
    """Test that data module can be imported."""
    from unifolm_wma import data
    assert data is not None


def test_import_models_module():
    """Test that models module can be imported."""
    from unifolm_wma import models
    assert models is not None


def test_import_modules_module():
    """Test that modules can be imported."""
    from unifolm_wma import modules
    assert modules is not None


def test_import_utils_module():
    """Test that utils module can be imported."""
    from unifolm_wma import utils
    assert utils is not None
