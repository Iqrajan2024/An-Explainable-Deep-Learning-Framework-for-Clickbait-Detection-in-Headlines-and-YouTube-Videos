"""
===========================================================
ClickDetect AI

Metadata SHAP Generator

Generates SHAP explanations for the metadata
surrogate model.

===========================================================
"""

from __future__ import annotations

import numpy as np
import shap

from backend.models.loader import assets


class MetadataShap:
    """
    Generates SHAP explanations for
    YouTube metadata.

    Uses

    assets.metadata_surrogate
    """

    def __init__(self):

        self.model = assets.metadata_surrogate

        self.background = np.asarray(
            assets.bg_metadata
        )

        self.feature_names = (
            assets.metadata_feature_names
        )

        self.explainer = shap.KernelExplainer(
            self.predict_fn,
            self.background
        )

    # --------------------------------------------------
    # Prediction Function
    # --------------------------------------------------

    def predict_fn(
        self,
        metadata: np.ndarray
    ) -> np.ndarray:

        return self.model.predict(
            metadata,
            verbose=0
        )

    # --------------------------------------------------
    # Build Feature Importance
    # --------------------------------------------------

    def build_importance(
        self,
        shap_values: np.ndarray,
    ) -> list[dict]:
        """
        Convert SHAP values into a ranked list of metadata
        feature importance.
        """

        importance = []

        for feature, score in zip(
            self.feature_names,
            shap_values
        ):

            importance.append({

                "feature": feature,

                "importance": round(
                    float(score),
                    6
                ),

                "direction":
                    "positive"
                    if score >= 0
                    else "negative"

            })

        importance.sort(

            key=lambda x: abs(
                x["importance"]
            ),

            reverse=True

        )

        return importance


    # --------------------------------------------------
    # Positive Contributors
    # --------------------------------------------------

    def top_positive(
        self,
        importance,
        top_k=10,
    ):

        return [

            item

            for item in importance

            if item["importance"] > 0

        ][:top_k]


    # --------------------------------------------------
    # Negative Contributors
    # --------------------------------------------------

    def top_negative(
        self,
        importance,
        top_k=10,
    ):

        return [

            item

            for item in importance

            if item["importance"] < 0

        ][:top_k]


    # --------------------------------------------------
    # Generate Explanation
    # --------------------------------------------------

    def generate_explanation(
        self,
        validator_output: dict,
        top_k: int = 10,
    ) -> dict:
        """
        Generate SHAP explanation for metadata.
        """

        metadata = validator_output["metadata"]

        prediction = float(

            self.model.predict(

                metadata,

                verbose=0

            )[0][0]

        )

        shap_values = self.explainer.shap_values(

            metadata,

            nsamples=50

        )

        if isinstance(shap_values, list):

            shap_values = shap_values[0]

        shap_values = np.asarray(shap_values)

        if shap_values.ndim == 3:

            shap_values = shap_values[0]

        if shap_values.ndim == 2:

            shap_values = shap_values[0]

        importance = self.build_importance(
            shap_values
        )

        positive = self.top_positive(
            importance,
            top_k
        )

        negative = self.top_negative(
            importance,
            top_k
        )

        metrics = [
            {
                "feature": item["feature"],
                "impact": item["importance"],
                "direction": item["direction"],
            }
            for item in importance
        ]

        try:

            base_value = float(

                np.asarray(

                    self.explainer.expected_value

                ).flatten()[0]

            )

        except Exception:

            base_value = None

        return {

            "prediction": prediction,

            "label": (
                "Clickbait"
                if prediction >= 0.5
                else "Not Clickbait"
            ),

            "base_value": base_value,

            "important_features": importance[:top_k],

            "positive_features": positive,

            "negative_features": negative,

            "metrics": metrics,

            "shap_values": shap_values.tolist()
        }