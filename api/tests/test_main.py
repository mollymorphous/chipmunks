def test_hello(client):
    assert client.get("/").json() == {"message": "Hello, Chipmunks!"}
