# Bugs Found During API Testing

## 1. **schemas.py – Pet `name` type** (fixed)
- **Location:** `schemas.py` – `pet` schema
- **Issue:** `name` was defined as `"type": "integer"` while the API returns pet names as strings (e.g. `"snowball"`, `"ranger"`).
- **Fix applied:** Changed to `"type": "string"` so schema validation matches the API.

---

## 2. **app.py – Error message not interpolated**
- **Location:** `app.py` line 100 – `PetFindByStatus` GET (findByStatus)
- **Issue:** The 400 error message uses a normal string: `'Invalid pet status {status}'`, so the response body is literally `"Invalid pet status {status}"` instead of the actual invalid value.
- **Expected:** Use an f-string: `f'Invalid pet status {status}'` (or include the value in the message).

---

## 3. **app.py – PATCH /store/order/{order_id} with missing/invalid body**
- **Location:** `app.py` lines 145, 154 – `OrderUpdateResource.patch`
- **Issue:** `update_data = request.json` can be `None` if the client sends no body or invalid JSON. Then `update_data['status']` raises `TypeError`, and the API returns **500** instead of **400**.
- **Expected:** Check that `update_data` is a dict and has a `status` key before using it; otherwise return 400 with a clear message.

---

## 4. **app.py – POST /pets with missing `id`**
- **Location:** `app.py` lines 72–74 – `PetList.post` (create pet)
- **Issue:** The code uses `pet['id']` when checking for duplicate IDs. If the client omits `id` in the body (allowed by the model), this raises **KeyError** and returns **500**.
- **Expected:** Either require `id` in the payload, or handle missing `id` (e.g. assign one or return 400).

---

## Summary
| # | Component    | Bug summary                          | Severity |
|---|--------------|--------------------------------------|----------|
| 1 | schemas.py   | Pet `name` type was integer (fixed) | Fixed    |
| 2 | app.py       | findByStatus 400 message not f-string | Minor   |
| 3 | app.py       | PATCH order with no/invalid body → 500 | Medium  |
| 4 | app.py       | POST pet without `id` → 500         | Medium   |
