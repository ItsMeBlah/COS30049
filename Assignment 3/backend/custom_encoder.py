import numpy as np
from sklearn.preprocessing import LabelEncoder

# Custom label encoder class to handle unseen labels during transformation
class CustomLabelEncoder(LabelEncoder):
    def __init__(self):
        # Initializes the custom label encoder and extends the base LabelEncoder class
        super().__init__()
        self.classes_ = None  # Placeholder for class labels, including an extra label for unknowns

    def fit(self, y):
        # Fits the encoder to the labels and adds a '<unknown>' class for handling unseen labels
        super().fit(y)
        self.classes_ = np.append(self.classes_, '<unknown>')  # Append unknown label to classes
        return self

    def transform(self, y):
        # Transforms labels into encoded integers, with unseen labels mapped to the '<unknown>' class
        unseen_label = len(self.classes_) - 1  # Index for the '<unknown>' label

        transformed = []
        for label in y:
            if label in self.classes_:
                transformed.append(super().transform([label])[0])  # Use existing encoding for known labels
            else:
                transformed.append(unseen_label)  # Map unseen labels to '<unknown>'
        
        return np.array(transformed)

    def fit_transform(self, y):
        # Combines fit and transform methods for convenience
        return self.fit(y).transform(y)
