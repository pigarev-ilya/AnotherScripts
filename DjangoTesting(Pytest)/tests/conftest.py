import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from datetime import date


@pytest.fixture
def course_factory():
    def course(**kwargs):
        return baker.make("Course", make_m2m=True, **kwargs)
    return course

@pytest.fixture
def student_factory():
    def student(**kwargs):
        return baker.make("Student", birth_date=date.today, **kwargs)
    return student

@pytest.fixture
def api_client():
    return APIClient()