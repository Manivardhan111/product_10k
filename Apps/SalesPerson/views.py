import json
import random
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from Apps.SalesPerson.models import admin_salesPerson
from Apps.SalesPerson.serializers import RegisterSalesPersonSerializer
from Apps.Student.models import registeredStudents, intrestedStudent
from django.core.serializers import serialize
from Apps.Student.serializers import intrestedStudentsSerializer,registeredStudentsSerializer

# Create your views here.


@csrf_exempt
def salesperson_sample(request):
    return HttpResponse("salesperson_sample")


@csrf_exempt
def admin_login(request, added_email=None):

    if request.method == "POST":
        if added_email:
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')

            try:
                admin = admin_salesPerson.objects.filter(
                    email=email, password=password).first()
                do_exist = admin_salesPerson.objects.filter(
                    email=added_email).first()
                if do_exist is None:
                    if admin and admin.role == "super_admin":
                        serializer = RegisterSalesPersonSerializer(
                            data={'id': "null", 'name': "null", 'password': "null", 'is_admin': False, "email": added_email, 'approval_status': "pending", 'approved_by': admin.name})
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse({'success': True, 'message': 'Access granted successfully'})
                        else:
                            return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)
                    else:
                        return JsonResponse({'success': False, 'message': 'User does not have admin access'}, status=403)
                else:
                    return JsonResponse({'message': "User already exists"})

            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error granting access: {str(e)}'}, status=500)
        elif request.method == "POST":
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if email and password:
                try:
                    admin = admin_salesPerson.objects.filter(
                        email=email, password=password).first()
                    if admin is not None:
                        students = intrestedStudent.objects.all()
                        serializer = RegisterSalesPersonSerializer(
                            students, many=True)
                        return JsonResponse(json.loads(serializer.data, safe=False))
                    else:
                        return JsonResponse({'success': False, 'message': 'User does not have  admin access'}, status=403)
                except Exception as e:
                    return JsonResponse({'success': False, 'message': f'Error processing request: {str(e)}'}, status=500)
            elif not email or not password:
                return HttpResponse("Invalid credentials")
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def salesperson_registration(request):
    try:
        if request.method == "POST":
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            existing_salesperson = admin_salesPerson.objects.get(email=email)
            str_name = name.split()
            id_name = str_name[0]
            id_num = ''.join(random.choices('0123456789', k=3))
            id = f"{id_name}{id_num}"
            if existing_salesperson.approval_status != 'success':
                approver = existing_salesperson.approved_by
                existing_salesperson.delete()
                serializer = RegisterSalesPersonSerializer(
                    data={
                        'id': id, 'name': name, 'password': password, 'is_admin': True, "email": email, 'approval_status': "success", 'approved_by': approver
                    }
                )
                if serializer.is_valid():
                    serializer.save()

                return JsonResponse({'success': True, 'message': 'Update successful! You are now an admin.'})
            else:
                return JsonResponse({'success': False, 'message': 'The user already exists or is already approved.'}, status=400)

    except admin_salesPerson.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Salesperson not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error processing request: {str(e)}'}, status=500)


@csrf_exempt
def get_intrested_students(request, sp_email=None):
    if request.method=='POST' and sp_email:
        try:
            is_authorised = admin_salesPerson.objects.filter(
                email=sp_email).first()

            if is_authorised is not None and is_authorised.is_admin == True:
                interested_student_list = intrestedStudent.objects.all()
                serializer=intrestedStudentsSerializer(interested_student_list,many=True)
                return JsonResponse({"interested_students":serializer.data})
                # serialized_data = serialize('json', interested_student_list)
                # return JsonResponse({"interested_students": serialized_data}, safe=False)
            elif is_authorised is not None and is_authorised.is_admin == False:
                return HttpResponse("You do not have admin access")
            else:
                return HttpResponse("You are not authorized!")

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    return HttpResponse("Only POST methods are allowed!")


@csrf_exempt
def get_registered_students(request,sp_email=None):
    if request.method=='POST' and sp_email:
        # return HttpResponse("get_registered_students")
        # return HttpResponse("Hello")
        try:
            is_authorised = admin_salesPerson.objects.filter(
                email=sp_email).first()

            if is_authorised is not None and is_authorised.is_admin == True:
                registered_student_list = registeredStudents.objects.all()
                serializer=registeredStudentsSerializer(registered_student_list,many=True)
                return JsonResponse({"registered_students":serializer.data})
                # serialized_data = serialize('json', registered_student_list)
                # return JsonResponse({"registered_students": serialized_data}, safe=False)
            elif is_authorised is not None and is_authorised.is_admin == False:
                return HttpResponse("You do not have admin access")
            else:
                return HttpResponse("You are not authorized!")

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    return HttpResponse("Only POST methods are allowed!")
