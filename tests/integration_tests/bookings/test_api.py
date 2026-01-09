import pytest


@pytest.mark.parametrize(
    "date_from, date_to, status_code",
    [
        ("2025-12-30", "2026-01-06", 201),
        ("2026-01-01", "2026-01-03", 201),
        ("2026-01-02", "2026-01-05", 201),
        ("2025-12-30", "2025-12-31", 201),
        ("2025-12-30", "2025-12-31", 201),
        ("2026-01-02", "2026-01-02", 201),
        ("2026-01-02", "2026-01-02", 201),
        ("2026-01-02", "2026-01-02", 409),
    ],
)
async def test_add_booking(date_from, date_to, status_code, db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    booking_data = {"room_id": room_id, "date_from": date_from, "date_to": date_to}
    response = await authenticated_ac.post("/bookings", json=booking_data)
    assert response.status_code == status_code
    if status_code == 201:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert res["data"]["room_id"] == room_id
        assert res["data"]["date_from"] == booking_data["date_from"]
        assert res["data"]["date_to"] == booking_data["date_to"]


@pytest.fixture(scope="module")
async def delete_all_bookings(db_module):
    await db_module.bookings.delete()
    await db_module.commit()


@pytest.mark.parametrize(
    "date_from, date_to, status_code, bookings_count",
    [
        ("2026-01-01", "2026-01-06", 201, 1),
        ("2026-01-01", "2026-01-03", 201, 2),
        ("2026-01-01", "2026-01-05", 201, 3),
    ],
)
async def test_add_and_get_bookings(
    date_from,
    date_to,
    status_code,
    bookings_count,
    delete_all_bookings,
    db,
    authenticated_ac,
):
    room_id = (await db.rooms.get_all())[0].id
    booking_data = {"room_id": room_id, "date_from": date_from, "date_to": date_to}
    response = await authenticated_ac.post("/bookings", json=booking_data)
    assert response.status_code == status_code
    res_data = response.json()
    assert isinstance(res_data, dict)
    assert res_data["status"] == "OK"
    assert res_data["data"]["room_id"] == room_id

    get_response = await authenticated_ac.get("/bookings/me")
    assert get_response.status_code == 200
    get_res_data = get_response.json()
    assert len(get_res_data) == bookings_count
