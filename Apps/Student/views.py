import datetime
from datetime import datetime, timedelta, timezone
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import jwt
from Apps.Student.models import intrestedStudent, registeredStudents
from Apps.Student.serializers import intrestedStudentsSerializer, registeredStudentsSerializer
import re
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import random
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, Token
from Apps.Mentor.models import Assessment_Questions
from django.contrib.auth import authenticate, login
from datetime import date



# Create your views here.


@csrf_exempt
def student_sample(request):
    return HttpResponse("student_sample without prefix")


@csrf_exempt
def interested_student(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            mobile = request.POST.get('mobile', '')
            current_date = date.today()

            def is_valid_mobile(mobile):
                return len(mobile) == 10 and mobile.isdigit()

            def is_valid_email(email):
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                return re.match(pattern, email) is not None

            if all([email, name, mobile]):
                existing_student = intrestedStudent.objects.filter(
                    email=email, mobile=mobile).first()

                if existing_student is None:
                    if is_valid_email(email) and is_valid_mobile(mobile):
                        serializer = intrestedStudentsSerializer(data={
                            'name': name,
                            'email': email,
                            'mobile': mobile,
                            'visited_on': current_date,
                            'is_registered': "pending",
                            'status': 'interested'
                        })
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse({'success': True, 'message': 'Thanks for filling the form. Our experts will reach out to you soon'})
                        else:
                            return JsonResponse({'success': False, 'message': 'Error saving data'})
                    else:
                        return JsonResponse({'success': False, 'message': 'Invalid email format or mobile number'}, status=400)
                else:
                    return JsonResponse({'success': False, 'message': 'User already exists with the given email or mobile'}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data provided for registration'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error processing form data: {str(e)}'}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid method. Only GET and POST requests are allowed.'}, status=405)


@csrf_exempt
def student_registration(request):
    if request.method == "POST":
        SECRET_KEY = 'django-insecure-$gnqz&zdv=0rl*#+v@#@bz$b#_ceg9uwip*q+1)_0wag^($q02'

        def generate_jwt_token(id):
            expiration_time = datetime.utcnow() + timedelta(days=30)
            payload = {
                'user_id': id,
                'exp': expiration_time,
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return token

        try:
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            city = request.POST.get('city', '')
            qualification = request.POST.get('qualification', '')
            mobile = request.POST.get('mobile', '')
            password = request.POST.get('password', '')
            str_name = name.split()
            id_name = str_name[0]
            id_num = ''.join(random.choices('0123456789', k=3))
            id = f"{id_name}{id_num}"

            def is_valid_mobile(mobile):
                return len(mobile) == 10 and mobile.isdigit()

            def is_valid_email(email):
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                return re.match(pattern, email) is not None

            if all([email, name, id, city, qualification, password, mobile]):
                existing_student = registeredStudents.objects.filter(
                    id=id, email=email, mobile=mobile).first()

                if existing_student is None:
                    if is_valid_email(email) and is_valid_mobile(mobile):
                        jwt_token = generate_jwt_token(id)
                        serializer = registeredStudentsSerializer(data={
                            'id': id,
                            'name': name,
                            'email': email,
                            'city': city,
                            'qualification': qualification,
                            'mobile': mobile,
                            'password': password,
                            "auth_token": jwt_token
                        })
                    if serializer.is_valid():
                        # return HttpResponse("register_working")
                        serializer.save()
                        return JsonResponse({'success': True, 'message': 'Thanks for filling the form. Our experts will reach out to you soon'})
                    elif not serializer.is_valid():
                        errors = serializer.errors
                        return JsonResponse({"error": errors})

                    else:
                        return JsonResponse({'success': False, 'message': 'User already exists with the email or mobile'}, status=403)

                else:
                    return JsonResponse({'success': False, 'message': 'Invalid email format or mobile number'}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'Invalid data provided for registration'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error processing form data: {str(e)}'}, status=500)
    else:
        return HttpResponse("Invalid request method.")


@csrf_exempt
def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # user = authenticate(request, email=email, password=password)
        user=registeredStudents.objects.filter(email=email,password=password).first()

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = JsonResponse(
                {'status': 'success', 'message': 'User authenticated successfully'})
            expiration_time = datetime.utcnow() + timedelta(hours=24)
            response.set_cookie(key='access_token', value=access_token,
                                expires=expiration_time, httponly=True)
            return  response
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=401)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})




@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    if request.method == 'POST':
        user_email = request.data.get('email')

        try:
            # Search for the user in the User model
            user = registeredStudents.objects.get(email=user_email)
            otp = ''.join(random.choices('0123456789', k=6))


            # Use TOTPDevice with the User instance
            totp_device, created = TOTPDevice.objects.get_or_create(
                user=user,
                confirmed=True,
                defaults={'key': otp, 'step': 300, 't0': 0}
            )

            # Rest of your code...
            send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is: {otp}',
            'from admin@10kCoders.com',
            [user_email],
            fail_silently=False,
        )

        except user.DoesNotExist:
            return JsonResponse({'message': 'User not found with the provided email.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    if request.method == 'POST':
        user_email = request.data.get('email')
        user_otp = request.data.get('otp')

        User = get_user_model()
        user = get_object_or_404(User, email=user_email)

        totp_device = TOTPDevice.objects.filter(
            user=user, confirmed=True).first()

        if totp_device and totp_device.verify(user_otp):
            return Response({'message': 'OTP verification successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'message': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = request.user

        if user.check_password(current_password):
            if new_password == confirm_new_password:
                user.password = new_password
                user.save()

                update_session_auth_hash(request, user)

                messages.success(request, 'Password changed successfully.')
                return redirect('change_password')
            else:
                messages.error(
                    request, 'New password and confirmation do not match.')
        else:
            messages.error(request, 'Invalid current password.')

    return HttpResponse("change password")


@csrf_exempt
# @login_required
def assessment_exam(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body)
            answers = json_data.get('answers', [])
            results = []
            total_correct = 0
            for answer in answers:
                question_id = answer.get("id")
                selected_option = answer.get("selected_option")
                correct_answer = Assessment_Questions.objects.filter(
                    id=question_id).values('correct_answer').first()
                correct_answer = correct_answer.get(
                    'correct_answer') if correct_answer else None

                is_correct = selected_option == correct_answer
                results.append({'question_id': question_id,
                               'is_correct': is_correct})
                if is_correct:
                    total_correct += 1

            return JsonResponse({'total_correct': total_correct, 'results': results})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
