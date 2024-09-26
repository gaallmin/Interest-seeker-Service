import requests
import pandas as pd

def fetchCourse(api_key, max_courses):
    headers={
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json',
    }
    base_url = 'https://api.coursera.org/api/courses.v1'
    params = {
        'fields': 'name,description,slug,shortDescription',
        'limit': 100,  # Adjust based on API limits
    }

    courses = []
    offest = 0

    while len(courses) < max_courses:
        params['start'] = offest
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break

        data = response.json()
        elements= data.get('elements', [])
        if not elements:
            break

        for course in elements:
            courses.append({
                'id': course.get('id'),
                'name': course.get('name'),
                'slug': course.get('slug'),
                'description': course.get('description') or course.get('shortDescription'),
            })
        
        offest += len(elements)
        if len(elements) < params['limit']:
            break
    
    return pd.DataFrame(courses[:max_courses])