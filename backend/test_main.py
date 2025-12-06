from fastapi.testclient import TestClient
from main import app, PITCHES

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_pitches():
    response = client.get("/api/pitches")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(PITCHES)
    assert "id" in data[0]
    assert "type" in data[0]

def test_vote():
    # Get a pitch to vote on
    pitches_resp = client.get("/api/pitches")
    pitch_id = pitches_resp.json()[0]["id"]
    
    vote_data = {
        "pitch_id": pitch_id,
        "vote_type": "like"
    }
    response = client.post("/api/vote", json=vote_data)
    assert response.status_code == 200
    assert response.json()["status"] == "recorded"
    assert response.json()["vote"]["vote_type"] == "like"
