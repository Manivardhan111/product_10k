from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from Apps.SalesPerson.models import admin_salesPerson

from Apps.SalesPerson.serializers import AdminSalesPersonSerializer

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
                # return HttpResponse(do_exist)

                if do_exist is None:
                    if admin and admin.role == "super_admin":
                        serializer = AdminSalesPersonSerializer(
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
                        students = admin_salesPerson.objects.all()
                        serializer = AdminSalesPersonSerializer(
                            students, many=True)
                        return JsonResponse(serializer.data, safe=False)
                    else:
                        return JsonResponse({'success': False, 'message': 'User does not have  admin access'}, status=403)
                except Exception as e:
                    return JsonResponse({'success': False, 'message': f'Error processing request: {str(e)}'}, status=500)
            elif not email or not password:
                return HttpResponse("Invalid credentials")
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def admin_salesperson_api(request):
    try:
        if request.method == "GET":
            return HttpResponse("admin person/GET")
        elif request.method == "POST":
            id = request.POST.get('id', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            existing_salesperson = admin_salesPerson.objects.get(email=email)
            if existing_salesperson.approval_status != 'success':
                approver = existing_salesperson.approved_by
                existing_salesperson.delete()
                serializer = AdminSalesPersonSerializer(
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
