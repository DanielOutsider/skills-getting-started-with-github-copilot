import pytest
from httpx import AsyncClient
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "participants" in data["Chess Club"]

@pytest.mark.asyncio
async def test_signup_for_activity():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Test successful signup
        response = await client.post("/activities/Chess%20Club/signup", data={"email": "test@mergington.edu"})
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]

        # Test duplicate signup
        response = await client.post("/activities/Chess%20Club/signup", data={"email": "test@mergington.edu"})
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

        # Test invalid activity
        response = await client.post("/activities/Invalid%20Activity/signup", data={"email": "test@mergington.edu"})
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_unregister_from_activity():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # First signup
        await client.post("/activities/Chess%20Club/signup", data={"email": "unregister@mergington.edu"})

        # Test successful unregister
        response = await client.request("DELETE", "/activities/Chess%20Club/unregister", data={"email": "unregister@mergington.edu"})
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]

        # Test unregister not signed up
        response = await client.request("DELETE", "/activities/Chess%20Club/unregister", data={"email": "notsigned@mergington.edu"})
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

        # Test invalid activity
        response = await client.request("DELETE", "/activities/Invalid%20Activity/unregister", data={"email": "test@mergington.edu"})
        assert response.status_code == 404