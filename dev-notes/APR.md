
1. is it even possible to look at APR data with np mode?

method seems to already exist:

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

look at `get_student_requirements` in APR filter

1. What is APR data?
    - sid, course and what requirement it fulfills, t/f for fulfilled
    - you can look at your own APR data from CalCentral

1. everything loaded from data through load.py - get familiar with this file

1. Can't use staging - all sorts of SQL things happening that you can't load
1. what was the problem with master again?  SSL errors - fixed