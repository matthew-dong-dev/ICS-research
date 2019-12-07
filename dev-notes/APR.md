
#  Goal return the top 10 unfulfilled requirements - general?  college?

1. Can't launch staging service - all sorts of SQL things happening that you can't load
1. what was the problem with master again?  SSL errors - fixed
1. is it even possible to look at APR data with np mode?  - Yes dummy requirements exists
1. method seems to already exist at `/api/getAprInfo`

```
@app.route('/api/getAprInfo', methods=['POST'])
def get_apr_info():
    sid = request.args.get('sid')
    anon = '-1'
    if sid in lookup_dict:
        anon = lookup_dict[sid]
    else:
        anon = request.args.get('anon')
    response = academic_plan_review.get_student_requirements(anon)
    response['status'] = 'OK'

    return json.dumps(response)
```

1. but something is being broken in `get_student_requirements` in APR filter
    - it's actually being called in the FE??  `/api/getAprInfo` being hit on login 
    return {
            'generic_requirements': generic_requirement,
            'major_requirements': major_requirements
        }
    - then what is being done with this information? 

1. what is this data being sent from FE to the `nextcourse/predict` endpoint - is this loaded first to the FE and then sent back to the BE?  
    - `getRecs`
    - filter_apr: {"genericRequirement":"genericRequirementCourseList","majorRequirement":[]}
    - filter_apr_requirements: {"aprSelected":true,"genericRequirementSelected":false,"majorRequirementSelected":false}
1. read APR df from dummy_data & hashed data

1. What is APR data?
    - sid, course and what requirement it fulfills, t/f for fulfilled
    - you can look at your own APR data from CalCentral

1. all processed data loaded in service through `load.py` - get familiar with this file
1. get familiar with `dummy_data.py`

