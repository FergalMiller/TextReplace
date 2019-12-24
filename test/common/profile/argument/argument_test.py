import pytest

from text_replace.common.profile.argument.argument import Argument
from text_replace.common.profile.argument.argument_error import ArgumentError


@pytest.fixture(autouse=True)
def required_argument() -> Argument:
    return Argument("-ra", "Required test argument.", True, r'^contains$')


@pytest.fixture(autouse=False)
def non_required_argument() -> Argument:
    return Argument("-nra", "Non required test argument", False, r'^contains$')


def test_self_validate_required_argument_no_value(required_argument: Argument):
    with pytest.raises(ArgumentError):
        required_argument.self_validate()


def test_self_validate_non_required_argument_no_value(non_required_argument: Argument):
    non_required_argument.self_validate()


def test_pass_value(required_argument: Argument):
    required_argument.pass_value(" val  ")
    assert required_argument.value == "val"


def test_self_validate_with_non_matching_value_pattern(required_argument: Argument):
    required_argument.pass_value("not valid")
    with pytest.raises(ArgumentError):
        required_argument.self_validate()


def test_self_validate_with_matching_value_pattern(required_argument: Argument):
    required_argument.pass_value("contains")
    required_argument.self_validate()


def test_has_value(required_argument: Argument):
    assert not required_argument.has_value()
    required_argument.pass_value("val")
    assert required_argument.has_value()
