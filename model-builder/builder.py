import os
import pyarrow.parquet as pq
import pyarrow.fs
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from datetime import date
import joblib  # For saving the model
from dotenv import load_dotenv

load_dotenv()
# Konfigurasi AWS Access
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_S3_REGION = "us-east-1"  # Ganti dengan region S3 Anda jika berbeda

# Path file di S3
today = date.today().strftime("%b-%d-%Y")
s3_file_path = f"{AWS_BUCKET_NAME}/bronze/hospitaldb/{today}/patient_readmissions/part-00000-4288396d-aa41-4bf8-8e72-d82f49ebfaec-c000.snappy.parquet"

# Membaca data dari S3 ke Pandas DataFrame
def load_parquet_from_s3_to_pandas(s3_path):
    try:
        # Konfigurasi Pandas untuk menggunakan S3
        print(f"Loading file from S3 path: {s3_path}")
        s3 = pyarrow.fs.S3FileSystem(
            access_key=AWS_ACCESS_KEY,
            secret_key=AWS_SECRET_KEY,
            endpoint_override="http://localhost:9000"  # Ganti ini jika menggunakan MinIO
        )
        table = pq.read_table(s3_file_path, filesystem=s3)
        df = table.to_pandas()
        print("Parquet data successfully loaded into Pandas DataFrame.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


data = load_parquet_from_s3_to_pandas(s3_file_path)

print(data.columns)

# Step 1: Preprocessing
# Define categorical and numerical columns
categorical_columns = ['gender', 'primary_diagnosis', 'discharge_to']
numerical_columns = [col for col in data.columns if col not in categorical_columns + ['readmitted']]

# Define transformers for preprocessing
categorical_transformer = OneHotEncoder(handle_unknown='ignore')
numerical_transformer = StandardScaler()

# Combine transformers into a ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_columns),
        ('cat', categorical_transformer, categorical_columns)
    ]
)

# Separate features (X) and target variable (y)
X = data.drop('readmitted', axis=1)
y = data['readmitted']

# Split data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Step 2: Create pipeline with preprocessor and model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42, class_weight='balanced'))
])

# Define hyperparameter grid
param_grid = {
    'classifier__n_estimators': [350],
    'classifier__max_depth': [None],
    'classifier__min_samples_split': [2]
}

# Step 3: Use GridSearchCV with the pipeline
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)

# Train the model with GridSearchCV
grid_search.fit(X_train, y_train)

# Get the best pipeline
best_pipeline = grid_search.best_estimator_

# Predict on the test set
y_pred = best_pipeline.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Best Model Accuracy: {accuracy}")
print("Classification Report:")
print(report)

# Step 4: Save the pipeline
joblib.dump(best_pipeline, '/root/bigdata/model/best_model.pkl')
print("Pipeline berhasil disimpan ke '/root/bigdata/model/best_model.pkl'")