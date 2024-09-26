# recommendation_engine.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def extract_features(row, feature_columns, prefix, clean=True):
    features = {}
    for col in feature_columns:
        if row[col] > 0:  # Include only features with positive importance
            feature_name = col.replace(prefix, '')
            if clean:
                feature_name = feature_name.replace('_', ' ').title()
            features[feature_name] = row[col]
    return features

def recommend_career(
    user_profile, 
    agg_df_scaled, 
    occupation_df, 
    riasec_features, 
    knowledge_features, 
    abilities_features, 
    skills_features, 
    top_n=5, 
    top_skills=10, 
    top_abilities=10, 
    top_knowledge=10,
    min_skill_score=0.5, 
    min_ability_score=0.5, 
    min_knowledge_score=0.5
):
    user_df = pd.DataFrame([user_profile])
    
    for feature in riasec_features:
        if feature not in user_df.columns:
            user_df[feature] = 0.0
    user_df = user_df[riasec_features]
    user_vector = user_df.values
    
    # Compute cosine similarity between user and all jobs
    similarities = cosine_similarity(user_vector, agg_df_scaled[riasec_features].values)[0]
    
    # Add similarity scores to the DataFrame
    agg_df_scaled = agg_df_scaled.copy()  # Avoid SettingWithCopyWarning
    agg_df_scaled['similarity'] = similarities
    top_jobs = agg_df_scaled.sort_values(by='similarity', ascending=False).head(top_n)
    top_jobs = top_jobs.merge(occupation_df[['title']], on='onetsoc_code', how='left')
    
    # Extract Skills, Abilities, Knowledge Areas for top occupations
    recommendations = []
    for _, row in top_jobs.iterrows():
        job = {
            'onetsoc_code': row['onetsoc_code'],
            'title': row['title'] if pd.notnull(row['title']) else 'Unknown Title',
            'similarity_score': row['similarity'],
            'skills': extract_features(row, skills_features, 'skills_'),
            'abilities': extract_features(row, abilities_features, 'abilities_'),
            'knowledge_areas': extract_features(row, knowledge_features, 'knowledge_')
        }
        recommendations.append(job)
    
    # Aggregate Skills, Abilities, Knowledge Areas with their weighted importance scores
    aggregated_skills = {}
    aggregated_abilities = {}
    aggregated_knowledge = {}
    
    for job in recommendations:
        similarity = job['similarity_score']
        for skill, importance in job['skills'].items():
            aggregated_skills[skill] = aggregated_skills.get(skill, 0) + (importance * similarity)
        for ability, importance in job['abilities'].items():
            aggregated_abilities[ability] = aggregated_abilities.get(ability, 0) + (importance * similarity)
        for knowledge, importance in job['knowledge_areas'].items():
            aggregated_knowledge[knowledge] = aggregated_knowledge.get(knowledge, 0) + (importance * similarity)
    
    # Sort aggregated features by total weighted importance scores
    sorted_skills = sorted(aggregated_skills.items(), key=lambda x: x[1], reverse=True)
    sorted_abilities = sorted(aggregated_abilities.items(), key=lambda x: x[1], reverse=True)
    sorted_knowledge = sorted(aggregated_knowledge.items(), key=lambda x: x[1], reverse=True)
    
    # Apply thresholds and limit to top N features
    final_skills = [(skill, round(score, 2)) for skill, score in sorted_skills if score >= min_skill_score][:top_skills]
    final_abilities = [(ability, round(score, 2)) for ability, score in sorted_abilities if score >= min_ability_score][:top_abilities]
    final_knowledge = [(knowledge, round(score, 2)) for knowledge, score in sorted_knowledge if score >= min_knowledge_score][:top_knowledge]
    
    final_recommendations = {
        'occupations': recommendations,
        'skills': final_skills,
        'abilities': final_abilities,
        'knowledge_areas': final_knowledge
    }
    
    return final_recommendations
