# Pull Request Summary

## Summary

Completes the pytest API automation tasks: fixes and extends the pet tests, adds the store PATCH test, and documents bugs found in the API.

---

## Changes

### test_pet.py

- **test_pet_schema:** Fixed schema validation by changing pet `name` from `integer` to `string` in `schemas.py` so it matches the API.
- **test_find_by_status_200:** Parametrized with all statuses (`available`, `sold`, `pending`); added assertions for 200 response, `status` on each pet, and schema validation per item.
- **test_get_by_id_404:** Implemented 404 test for `GET /pets/{pet_id}`; parameterized with non-existent IDs (e.g. 999, 3, 100, -1).

### test_store.py

- **test_patch_order_by_id:** Added PATCH test for `/store/order/{order_id}`.
- **Fixture:** `order_id` fixture creates an order via POST using an available pet (from `findByStatus`) and yields the order ID for the test.
- **Assertions:** Validates 200, response schema, and message: `"Order and pet status updated successfully"`.

### schemas.py

- Fixed pet schema: `name` type set to `string`.
- Added `order` schema for POST order response validation.
- Added `order_update_response` schema for PATCH response validation.

### BUGS_NOTES.md

- Documented bugs found: schema `name` type (fixed), findByStatus 400 message not using f-string, PATCH order with missing/invalid body causing 500, POST pet without `id` causing 500.

---

## How to Run

1. `python app.py` (in one terminal).
2. `python -m pytest -v --html=report.html` (in another).
