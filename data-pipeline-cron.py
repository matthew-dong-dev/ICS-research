import requests

def new_semester_released(term_id):
    
    class_api_url = 'https://apis.berkeley.edu/uat/sis/v1/classes?term-id=%s&page-number=1&page-size=50'
    class_api_url = class_api_url % (term_id)
    headers = {
        'Accept': 'application/json',
    }
    headers['app_id'] = getpass()
    headers['app_key'] = getpass()
    
    try:
        resp = requests.get(class_api_url, headers=headers)
#         print(resp.json())
        is_semester_released = resp.json()['apiResponse']['httpStatus']['code'] == '200'
    except requests.exceptions.RequestException as e:
        print(e.response.text)
    
    return is_semester_released

if __name__ == "main":
    currentSemester = os.env
    targetSemester = os.env 
    if new_semester_released(targetSemester):
        increment(targetSemester)
        os.command('python refresh.py') 
    if new_edw_data():
        increment(currentSemester)
        os.command('python refresh.py') 
    
    
