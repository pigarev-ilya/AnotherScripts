import pytest
from django.urls import reverse


# Проверка получения 1го курса (retrieve-логика)
@pytest.mark.django_db
def test_get_one_course_in_db(course_factory, api_client):
    course_factory = course_factory(_quantity=1)
    url = reverse('courses-detail', args=[course_factory[0].id])
    response = api_client.get(url)
    assert response.status_code == 200
    expected_data_1 = course_factory[0].id
    result_data_1 = response.data['id']
    expected_data_2 = course_factory[0].name
    result_data_2 = response.data['name']
    assert result_data_1 == expected_data_1
    assert result_data_2 == expected_data_2

# Проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_list_course_in_db(course_factory, api_client):
    number_of_records = 10
    course_factory = course_factory(_quantity=number_of_records)
    url = reverse('courses-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == len(course_factory)
    expected_data = [course.id for course in course_factory]
    result_data = [course['id'] for course in response.data]
    assert result_data == expected_data


# Проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_id_course_in_db(course_factory, api_client):
    number_of_records = 10
    course_factory = course_factory(_quantity=number_of_records)
    url = reverse("courses-list")
    response = api_client.get(url, {"id": course_factory[3].id})
    assert response.status_code == 200
    assert len(response.data) == 1
    result_data = response.data[0]['id']
    expected_data = course_factory[3].id
    assert result_data == expected_data

# Проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_name_course_in_db(course_factory, api_client):
    number_of_records = 10
    course_factory = course_factory(_quantity=number_of_records)
    url = reverse("courses-list")
    response = api_client.get(url, {"name": course_factory[5].name})
    assert response.status_code == 200
    result_data = response.data[0]['name']
    expected_data = course_factory[5].name
    assert expected_data == result_data


# Тест успешного создания курса
@pytest.mark.django_db
def test_create_course_in_db(api_client):
    url = reverse('courses-list')
    course_load = {"name": "Test1"}
    response = api_client.post(url, course_load)
    assert response.status_code == 201
    expected_data = course_load['name']
    result_data = response.data['name']
    assert result_data == expected_data


# Тест успешного обновления курса
@pytest.mark.django_db
def test_update_course_in_db(course_factory, api_client):
    number_of_records = 10
    course_factory = course_factory(_quantity=number_of_records)
    url = reverse('courses-detail', args=[course_factory[4].id])
    course_load = {"name": "Test2"}
    response = api_client.patch(url, course_load)
    assert response.status_code == 200
    expected_data = course_load['name']
    result_data = response.data['name']
    assert result_data == expected_data


# Тест успешного удаления курса
@pytest.mark.django_db
def test_destroy_course_in_db(course_factory, api_client):
    number_of_records = 10
    course_factory = course_factory(_quantity=number_of_records)
    url = reverse('courses-list')
    url_with_id = reverse('courses-detail', args=[course_factory[3].id])
    response = api_client.delete(url_with_id)
    response_all = api_client.get(url)
    assert response.status_code == 204
    expected_data = [course.id for course in course_factory]
    expected_data.remove(course_factory[3].id)
    result_data = [course['id'] for course in response_all.data]
    assert result_data == expected_data


