import joblib
from quart import Quart, request, jsonify
from quart_cors import cors
from middleware.custom_error import CustomError
from middleware.custom_response import CustomResponse
import asyncio
import json

PORT=4000

app = Quart(__name__)

app = cors(app, allow_origin="*")

# Fungsi untuk memuat model
def load_model(model_path):
    return joblib.load(model_path)

# Load model-model yang telah disimpan
model_path = "../../model/best_model.pkl"

def preprocess_request_to_dataframe(req_body):
    """
    Mengubah body request menjadi DataFrame yang sesuai untuk prediksi.

    Parameters:
    - req_body (dict): Body request JSON.

    Returns:
    - DataFrame: DataFrame yang siap digunakan untuk prediksi.
    """
    try:
        # Membuat DataFrame dari request body
        data = pd.DataFrame([req_body])
        print("DataFrame berhasil dibuat:")
        print(data)
        return data
    except Exception as e:
        print(f"Error saat memproses request body: {e}")
        return None

# @app.after_serving
# async def shutdown():
#     await spark.close()

@app.route('/', methods=['GET'])
def home():
    return 'runnin wild...'

@app.route('/predict', methods=['POST'])
async def RecommendationRouter():
    try:
        req = await request.get_json()

        if req['age'] is None:
            raise CustomError(400, 'age required')

        input_data = preprocess_request_to_dataframe(req)
        if input_data is None:
            raise CustomError(400, 'Gagal memproses data input')
        model = load_model(model_path)
        predictions = model.predict(input_data)
        # response = CustomResponse(200, 'get recommendation successfully', formatted_recommendations)
        # return jsonify(response.JSON()), response.code
        return {"predictions": predictions.tolist()}, 200
    except Exception as err:
        print(err)
        return jsonify(err.JSON()),err.code

if __name__ == '__main__':
    asyncio.run(app.run(host='159.89.203.127', port=PORT, debug=True))