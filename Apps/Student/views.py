from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
from Apps.SalesPerson.models import admin_salesPerson
from Apps.Student.models import intrestedStudent
from Apps.Student.serializers import intrestedStudentsSerializer
import re
# Create your views here.


@csrf_exempt
def student_sample(request):
    return HttpResponse("student_sample")


@csrf_exempt
def interested_student(request, sp_email=None):
    if sp_email:
        if request.method == "POST":
            try:
                sp_exists = admin_salesPerson.objects.filter(
                    email=sp_email).first()

                if sp_exists is not None and sp_exists.approval_status == 'success':
                    students = intrestedStudent.objects.all()
                    serializer = intrestedStudentsSerializer(
                        students, many=True)
                    # return HttpResponse(s)
                    return JsonResponse(serializer.data, safe=False)
                elif sp_exists is not None and sp_exists.approval_status == 'pending':
                    return JsonResponse({'success': False, 'message': 'You do not have accessimg rights! Please contact the Administrator'})
                elif sp_exists is None:
                    return JsonResponse({'success': False, 'message': 'You are not authorized!'})
            except Exception as e:
                print(f"An error occurred: {e}")
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        else:
            return JsonResponse({'success': False, 'message': 'You are not authorized! Please get authorization'})

    elif request.method == "POST":
        try:
            id = request.POST.get('id', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            city = request.POST.get('city', '')
            qualification = request.POST.get('qualification', '')
            mobile = request.POST.get('mobile', '')

            

            def is_valid_mobile(mobile):
                return len(mobile) == 10 and mobile.isdigit()

            def is_valid_email(email):
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                return re.match(pattern, email) is not None

            if all([email, name, id, city, qualification, mobile]):
                existing_student = intrestedStudent.objects.filter(
                    email=email, mobile=mobile).first()

                if existing_student is not None:
                    return JsonResponse({'success': False, 'message': 'User already exists with the email or mobile'}, status=403)
                user_id = intrestedStudent.objects.filter(id=id).first()
                if user_id is not None:
                    return JsonResponse({'success': False, 'message': 'User ID is already taken'}, status=403)

                if is_valid_email(email) and is_valid_mobile(mobile):
                    serializer = intrestedStudentsSerializer(data={
                        'id': id,
                        'name': name,
                        'email': email,
                        'city': city,
                        'qualification': qualification,
                        'mobile': mobile
                    })
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'success': True, 'message': 'Thanks for filling the form. Our experts will reach out to you soon'})
                    else:
                        return JsonResponse({'success': False, 'message': 'Error saving data'})
                else:
                    return JsonResponse({'success': False, 'message': 'Invalid email format or mobile number'}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data provided for registration'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error processing form data: {str(e)}'}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid method. Only GET and POST requests are allowed.'}, status=405)

            # return HttpResponse("student")
    # return HttpResponse("hello")


@csrf_exempt
def student_login(request):
    if request.method == 'GET':
        return HttpResponse("GET")
    elif request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        city = request.POST.get('city')
        qualification = request.POST.get('qualification')
        mobile = request.POST.get('mobile')

        existing_user = intrestedStudent.objects.filter(email=email).first()
        # return HttpResponse(existing_user)

        if existing_user:
            existing_user.id = id
            existing_user.name = name
            existing_user.password = password
            existing_user.city = city
            existing_user.qualification = qualification
            existing_user.mobile = mobile
            existing_user.save()
            return JsonResponse({'status': 'success', 'message': 'User information updated successfully'})
        else:
            serializer = intrestedStudentsSerializer(data={
                'id': id,
                'name': name,
                'email': email,
                'city': city,
                'qualification': qualification,
                'mobile': mobile,
                'password': password
            })

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'status': 'success', 'message': 'User registered successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
