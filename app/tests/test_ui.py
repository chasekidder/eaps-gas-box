


class TestUIPages():
    def test_home_page(self, test_client):
        response = test_client.get("/")
        assert response.status_code == 200

    def test_config_page(self, test_client):
        response = test_client.get("/config/")
        assert response.status_code == 200

    def test_data_page(self, test_client):
        response = test_client.get("/data/")
        assert response.status_code == 200

    def test_download_page(self, test_client):
        response = test_client.get("/download/")
        assert response.status_code == 404
        #TODO: add a file link and test status code 200

    def test_live_page(self, test_client):
        response = test_client.get("/live/")
        assert response.status_code == 200

    def test_api_page(self, test_client):
        response = test_client.get("/api/")
        assert response.status_code == 200