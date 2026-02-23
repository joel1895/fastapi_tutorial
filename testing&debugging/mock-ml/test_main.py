from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
import numpy as np

client = TestClient(app)

def test_predict_with_mock():
    with patch("model.model.predict") as mock_predict: #file mode,objet model, and the method predict
        mock_predict.return_value = [99]
        response = client.post(
            "/predict",
            json={
                "SepalLengthCm":5.5,	
                "SepalWidthCm": 3.1,	
                "PetalLengthCm": 5.0,	
                "PetalWidthCm":2.8
                }
        )
        assert response.status_code == 200
        assert response.json() == {"prediction":99}
        # mock_predict.assert_called_once_with(np.array([[5.5,2.1,4.3,1.23]]))
