from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

@pytest.fixture
def order_id():
    """Create an order via POST and yield the order_id for the test."""
    # Use an available pet (pet 0 may be 'pending' from a previous run)
    available = api_helpers.get_api_data("/pets/findByStatus", params={"status": "available"})
    available.raise_for_status()
    pets = available.json()
    assert pets, "No available pet to place an order"
    pet_id = pets[0]["id"]
    response = api_helpers.post_api_data("/store/order", {"pet_id": pet_id})
    assert response.status_code == 201
    data = response.json()
    validate(instance=data, schema=schemas.order)
    yield data["id"]


def test_patch_order_by_id(order_id):
    """Test PATCH /store/order/{order_id} updates order and pet status."""
    test_endpoint = f"/store/order/{order_id}"
    payload = {"status": "sold"}

    response = api_helpers.patch_api_data(test_endpoint, payload)

    assert response.status_code == 200
    data = response.json()
    validate(instance=data, schema=schemas.order_update_response)
    assert_that(data["message"], is_("Order and pet status updated successfully"))
