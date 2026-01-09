import pytest


@pytest.mark.parametrize(
    "date_from, date_to, status_code",
    [
        ("2025-12-28", "2025-12-31", 200),
        ("2025-12-31", "2025-12-28", 422),
        ("2025-12-31", "2025-12-31", 422),
    ],
)
async def test_get_hotels(date_from, date_to, status_code, ac):
    response_data = {"date_from": date_from, "date_to": date_to}
    response = await ac.get("/hotels", params=response_data)

    assert response.status_code == status_code
