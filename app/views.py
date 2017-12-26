from app.models import FilmRating
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
import simplejson as json
from django.http import HttpResponse
from django.db import DatabaseError

def root(request):
    return HttpResponse(json.dumps({"respMsg": u'alive'}),  status=200,
            content_type='application/json')

def is_parameter_valid(param_name, param):
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


def check_id(id):
    try:
        val = int(id)
    except ValueError:
        return HttpResponse(json.dumps({"respMsg": u'id is not a digit'}),  status=400,
        content_type='application/json')
    if val < 0:
        return HttpResponse(json.dumps({"respMsg": u'id is cant be less 0'}),  status=400,
        content_type='application/json')
    return True



def get_rating(request, id):
    data = check_id(id)
    if data != True:
        return data

    f_id = int(id)
    try:
        f_rating = FilmRating.objects.get_rating(f_id)
        if f_rating == -1:
            return HttpResponse(json.dumps({"respMsg": u'no rating'}),  status=404,
            content_type='application/json')
    except DatabaseError as text_error:
        message = u'Database Error: {0}'.format(text_error)
        return HttpResponse(json.dumps({"respMsg": message}),  status=500,
        content_type='application/json')
    return HttpResponse(json.dumps({"respMsg": u'Ok', "filmAvgRating": f_rating}),  status=200,
    content_type='application/json')

# @csrf_exempt
def delete_rating(request): #f_id, u_id):
    data = json.loads(request.body.decode("utf-8"))

    important_params = ['filmId', 'filmRating', 'userId']
    for param in important_params:
        check = is_parameter_valid(param, data.get(param))
        if check != True:
            return HttpResponse(json.dumps({"respMsg": check}),  status=400,
            content_type='application/json')
    try:
        if flag == "true":
            rec = FilmRating.objects.filter(film_id = f_id, user_id = u_id)
            rec.delete()
        else:
            film_avg_rating = FilmRating.objects.save_rating(f_id, f_rating, u_id)
    except DatabaseError as text_error:
        message = u'Database Error: {0}'.format(text_error)
        return HttpResponse(json.dumps({"respMsg": message}),  status=500,
        content_type='application/json')
    return HttpResponse(json.dumps({"respMsg": u'Ok', out_data: ids}),  status=200,
    content_type='application/json')





def get_linked_objects(request, id):
    data = check_id(id)
    if data != True:
        return data
    object_id = int(id)

    search_by = request.GET.get('search_by', '')

    try:
        if search_by=='user_id':
            ids = FilmRating.objects.get_films_by_user(object_id)
            if ids != -1:
                out_data = "filmId"
            else:
                return HttpResponse(json.dumps({"respMsg": "no films rated by user"}) ,status=404,
                content_type='application/json')
        else:
            ids = FilmRating.objects.get_users_by_film(object_id)
            if ids != -1:
                out_data = "userId"
            else:
                return HttpResponse(json.dumps({"respMsg": "no users rated this film"}) ,status=404,
                content_type='application/json')
    except DatabaseError as text_error:
        message = u'Database Error: {0}'.format(text_error)
        return HttpResponse(json.dumps({"respMsg": message}),  status=500,
        content_type='application/json')

    return HttpResponse(json.dumps({"respMsg": u'Ok', out_data: ids}),  status=200,
    content_type='application/json')




@csrf_exempt
def delete_film_rating(request):
    data = json.loads(request.body.decode("utf-8"))
    check = is_parameter_valid('filmId', data.get('filmId'))
    if check != True:
        return HttpResponse(json.dumps({"respMsg": check}),  status=400,
        content_type='application/json')

    film_id = int(data['filmId'])
    try:
        FilmRating.objects.delete_ratings_by_film_id(film_id)
    except DatabaseError as text_error:
        message = u'Database Error: {0}'.format(text_error)
        return HttpResponse(json.dumps({"respMsg": message}),  status=500,
        content_type='application/json')
    return HttpResponse(json.dumps({"respMsg": u'Ok'}),  status=200,
    content_type='application/json')

@csrf_exempt
def set_rating(request):
    data = json.loads(request.body.decode("utf-8"))

    #check params
    important_params = ['filmId', 'filmRating', 'userId']
    for param in important_params:
        check = is_parameter_valid(param, data.get(param))
        if check != True:
            return HttpResponse(json.dumps({"respMsg": check}),  status=400,
            content_type='application/json')

    f_id = int(data['filmId'])
    u_id = int(data['userId'])
    f_rating = int(data['filmRating'])

    # flag, old_data, film_rating_record = FilmRating(f_id, f_rating, u_id)
    try:
        flag, old_data, film_avg_rating = FilmRating.objects.save_rating(f_id, f_rating, u_id)

        # film_avg_rating = FilmRating.objects.save_rating(f_id, f_rating, u_id)
    except DatabaseError as text_error:
        message = u'Database Error: {0}'.format(text_error)
        return HttpResponse(json.dumps({"respMsg": message}),  status=500,
        content_type='application/json')

    return HttpResponse(json.dumps({"respMsg": "Ok", "filmAvgRating": film_avg_rating,
        "isUpdated" : flag, "oldData" : old_data}),
                        status=200, content_type='application/json')




    #
    # data = check_id(id)
    # if data != True:
    #     return data
    # fid = int(id)
    #
    # data = check_id(u_id)
    # if data != True:
    #     return data
    # uid = int(id)
