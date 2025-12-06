from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_get_pitches():
    with TestClient(app) as client:
        response = client.get("/api/pitches")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # We don't verify exact length or content as it depends on DB state which persists
        if len(data) > 0:
            assert "id" in data[0]
            assert "type" in data[0]

def test_vote():
    with TestClient(app) as client:
        # Get a pitch to vote on
        pitches_resp = client.get("/api/pitches")
        pitches_data = pitches_resp.json()
        
        if not pitches_data:
            # Seed if empty to make test robust
            client.post("/api/seed")
            pitches_data = client.get("/api/pitches").json()

        pitch_id = pitches_data[0]["id"]
        
        vote_data = {
            "pitch_id": pitch_id,
            "vote_type": "like"
        }
        response = client.post("/api/vote", json=vote_data)
        assert response.status_code == 200
        assert response.json()["status"] == "recorded"
        assert response.json()["vote"]["vote_type"] == "like"
