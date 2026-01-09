async def test_post_facilities(ac):
    facility = "Wi-Fi"
    response = await ac.post("/facilities", json={"title": facility})
    data = response.json()
    assert response.status_code == 201
    assert isinstance(data, dict)
    assert data.get("data").get("title") == facility


async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities",
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
