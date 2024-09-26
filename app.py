# app.py

import logging
from logging.handlers import RotatingFileHandler
# ... [other imports]

app = Flask(__name__)
CORS(app)

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Initialize Flask-Limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Load data
try:
    agg_df_scaled = pd.read_csv('agg_df_scaled.csv')
    occupation_df = pd.read_csv('occupation.csv')
    app.logger.info("Data files loaded successfully.")
except Exception as e:
    app.logger.error(f"Error loading data files: {e}")
    raise e

# ... [rest of the code]

@app.route('/recommend', methods=['POST'])
@limiter.limit("100 per hour")
def recommend():
    data = request.get_json()

    # Log incoming request
    app.logger.info(f"Received /recommend request: {data}")

    # Validate input presence
    if not data:
        app.logger.warning("No input data provided.")
        return jsonify({"error": "No input data provided"}), 400

    # Validate required features
    missing_features = [feature for feature in riasec_features if feature not in data]
    if missing_features:
        app.logger.warning(f"Missing RIASEC features: {', '.join(missing_features)}")
        return jsonify({"error": f"Missing RIASEC features: {', '.join(missing_features)}"}), 400

    # Validate API key
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        app.logger.warning(f"Unauthorized access attempt with API key: {api_key}")
        return jsonify({"error": "Unauthorized access. Invalid API key."}), 401

    # Convert input to float
    try:
        user_profile = {feature: float(data.get(feature, 0.0)) for feature in riasec_features}
    except (ValueError, TypeError) as e:
        app.logger.warning(f"Invalid input data types: {e}")
        return jsonify({"error": "Invalid input. RIASEC scores must be numbers."}), 400

    # Validate score ranges (0-5)
    for feature, score in user_profile.items():
        if not (0 <= score <= 5):
            app.logger.warning(f"{feature} score out of range: {score}")
            return jsonify({"error": f"{feature} score must be between 0 and 5."}), 400

    # Call the recommendation function
    try:
        recommendations = recommend_career_refined(
            user_profile=user_profile,
            agg_df_scaled=agg_df_scaled,
            occupation_df=occupation_df,
            riasec_features=riasec_features,
            knowledge_features=knowledge_features,
            abilities_features=abilities_features,
            skills_features=skills_features,
            top_n=5,
            top_skills=10,
            top_abilities=10,
            top_knowledge=10,
            min_skill_score=0.5, 
            min_ability_score=0.5, 
            min_knowledge_score=0.5
        )
        app.logger.info("Recommendation generated successfully.")
    except Exception as e:
        app.logger.error(f"Error during recommendation: {e}")
        return jsonify({"error": "Internal server error."}), 500

    # Structure the response
    response = {
        "occupations": [
            {
                "onetsoc_code": job['onetsoc_code'],
                "title": job['title'],
                "similarity_score": round(job['similarity_score'], 2)
            }
            for job in recommendations['occupations']
        ],
        "skills": [
            {"skill": skill, "importance_score": score}
            for skill, score in recommendations['skills']
        ],
        "abilities": [
            {"ability": ability, "importance_score": score}
            for ability, score in recommendations['abilities']
        ],
        "knowledge_areas": [
            {"knowledge_area": knowledge, "importance_score": score}
            for knowledge, score in recommendations['knowledge_areas']
        ]
    }

    app.logger.info(f"Response: {response}")
    return jsonify(response), 200
