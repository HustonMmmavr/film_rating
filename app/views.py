from app.models import FilmRating
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
import simplejson as json
from django.http import HttpResponse
from django.db import DatabaseError

def root(request):
    return HttpResponse(json.dumps({"respMsg": u'alive'}),  status=200,
            content_type='application/json')

def is_parameter_valid(params, param_name):
    param = params.get(param_name)
    if param == None or param == "":
        return param_name + " is Empty"
    else:
        try:
            val = int(param)
        except ValueError:
            return param_name + " is not a digit"
        if val < 0:
            return param_name + " cant be < 0"
    return True


def get_rating(request, f_id):
    try:
        val = int(f_id)
    except ValueError:
        return HttpResponse(json.dumps({"respMsg": u'id is not a digit'}),  status=400,
        content_type='application/json')
    if val < 0:
        return HttpResponse(json.dumps({"respMsg": u'id is cant be less 0'}),  status=400,
        content_type='application/json')

    try:
        f_rating = FilmRating.objects.get_rating(val)
        if f_rating == -1:
            return HttpResponse(json.dumps({"respMsg": u'no rating'}),  status=404,
            content_type='application/json')
    except DatabaseError as text_error:
        message = u'Database Error: {0}'.format(text_error)
        return HttpResponse(json.dumps({"respMsg": message}),  status=500,
        content_type='application/json')
    return HttpResponse(json.dumps({"respMsg": u'Ok', "filmRating": f_rating}),  status=200,
    content_type='application/json')



@csrf_exempt
def set_rating(request):
    data = json.loads(request.body.decode("utf-8"))
    print(data)
    is_valid_f_id = is_parameter_valid(data, "filmId")
    if is_valid_f_id != True:
        return HttpResponse(json.dumps({"respMsg": is_valid_f_id}),  status=400,
        content_type='application/json')
    f_id = int(data['filmId'])


    is_valid_f_rating = is_parameter_valid(data, "filmRating")
    print(is_valid_f_rating)
    if is_valid_f_rating != True:
        return HttpResponse(json.dumps({"respMsg": is_valid_f_rating}),  status=400,
        content_type='application/json')

    f_rating = int(data['filmRating'])
    if f_rating > 10:
        return HttpResponse(json.dumps({"respMsg": u'Rating cant be mare than 10'}),  status=400,
        content_type='application/json')

    is_valid_u_id = is_parameter_valid(data, "userId")
    if is_valid_u_id != True:
        return HttpResponse(json.dumps({"respMsg": is_valid_u_id}),  status=400,
        content_type='application/json')
    u_id = int(data['userId'])

    film_rating_record = FilmRating(f_id, f_rating, u_id)
    try:
        film_avg_rating = FilmRating.objects.save_rating(f_id, f_rating, u_id)
    except DatabaseError as text_error:
        message = u'Database Error: {0}'.format(text_error)
        return HttpResponse(json.dumps({"respMsg": message}),  status=500,
        content_type='application/json')

    return HttpResponse(json.dumps({"respMsg": "Ok", "filmAvgRating": str(film_avg_rating)}),
                        status=200, content_type='application/json')
