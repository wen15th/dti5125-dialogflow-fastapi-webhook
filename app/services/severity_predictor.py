import os
import joblib
import pandas as pd
from app.services.utils import to_severity_score

class SeverityPredictor:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", "classification_model.pkl")
        self.model = joblib.load(model_path)

    def predict(self, input_features: dict) -> int:
        """
        Predicts the severity score based on the given input features.

        Parameters:
            input_features (dict): A dictionary containing the user's input features.
                e.g.:
                    input_features = {
                        "pain_type": "Sharp",
                        "duration": "Last week",
                        "radiates": "No",
                        "self_score": 3,
                        "activity_score": 2,
                        "mood_score": 2,
                        "sleep_score": 3,
                        "severity_class": "Moderate"
                    }
        Returns:
            int: The predicted severity score (1 to 5).
        """
        df = pd.DataFrame([input_features])
        return to_severity_score(int(self.model.predict(df)[0]))




