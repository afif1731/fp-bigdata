import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from datetime import date
import joblib  # For saving the model

# Konfigurasi AWS Access
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_S3_REGION = "us-east-1"  # Ganti dengan region S3 Anda jika berbeda

# Path file di S3
today = date.today().strftime("%b-%d-%Y")
s3_file_path = f"s3://{AWS_BUCKET_NAME}/bronze/hospitaldb/{today}/patient_readmissions.parquet"

# Membaca data dari S3 ke Pandas DataFrame
def load_parquet_from_s3_to_pandas(s3_path, aws_access_key, aws_secret_key):
    try:
        # Konfigurasi Pandas untuk menggunakan S3
        df = pd.read_parquet(
            s3_path,
            storage_options={
                "key": aws_access_key,
                "secret": aws_secret_key,
            },
        )
        print("Parquet data successfully loaded into Pandas DataFrame.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

data = load_parquet_from_s3_to_pandas(s3_file_path, AWS_ACCESS_KEY, AWS_SECRET_KEY)

# Step 2: Preprocess the data
# Encoding categorical variables
label_encoder = LabelEncoder()
data['gender'] = label_encoder.fit_transform(data['gender'])
data['primary_diagnosis'] = label_encoder.fit_transform(data['primary_diagnosis'])
data['discharge_to'] = label_encoder.fit_transform(data['discharge_to'])

# Separate features (X) and target variable (y)
X = data.drop('readmitted', axis=1)
y = data['readmitted']

# Split data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Standardize the numerical features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 3: Initialize the models with hyperparameter grids for GridSearchCV
models = {
    "Logistic Regression": LogisticRegression(class_weight='balanced'),
    "Random Forest Classifier": RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'),
    "Support Vector Machine (SVM)": SVC(random_state=42, class_weight='balanced'),
    "K-Nearest Neighbors (KNN)": KNeighborsClassifier()
}

# Hyperparameter grids for GridSearchCV
param_grids = {
    "Logistic Regression": {'C': [0.01, 0.1, 1, 10], 'solver': ['liblinear']},
    "Random Forest Classifier": {'n_estimators': [50, 100, 200, 250, 300, 350, 400, 450, 500], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5, 10]},
    "Support Vector Machine (SVM)": {'C': [0.01, 0.1, 1, 10], 'kernel': ['linear', 'rbf']},
    "K-Nearest Neighbors (KNN)": {'n_neighbors': [3, 5, 7], 'weights': ['uniform', 'distance']}
}

# Step 4: Initialize GridSearchCV for each model and tune hyperparameters
results = {}

best_model_name = None  # To store the name of the best model
best_accuracy = 0  # To store the best accuracy

for model_name, model in models.items():
    print(f"Tuning {model_name}...")
    grid_search = GridSearchCV(model, param_grids[model_name], cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
    
    # Train the model with GridSearchCV
    grid_search.fit(X_train, y_train)
    
    # Get the best model from the grid search
    best_model_for_current_model = grid_search.best_estimator_
    
    # Predict on the test set
    y_pred = best_model_for_current_model.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    results[model_name] = {
        "accuracy": accuracy,
        "classification_report": report,
        "best_params": grid_search.best_params_
    }
    
    # Check if this is the best model
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model_name = model_name
        best_model = best_model_for_current_model

# Step 5: Compare the results
# Print the accuracy and classification report for each model
for model_name, result in results.items():
    print(f"Model: {model_name}")
    print(f"Best Parameters: {result['best_params']}")
    print(f"Accuracy: {result['accuracy']}")
    print("Classification Report:")
    print(result['classification_report'])
    print("-" * 50)

# Step 6: Save the best model using joblib
print(f"The best model is: {best_model_name} with accuracy: {best_accuracy}")

# Save the best model using joblib (equivalent to model.save())
joblib.dump(best_model, 'best_model.pkl')

print("Best model saved as 'best_model.pkl'")