from rest_framework.views import APIView
from rest_framework import status
from django.utils.decorators import method_decorator
from . import models
from hashlib import sha1
from rest_framework.response import Response
from helpers.api_helper import *
from helpers.authentication_helper import *
from helpers.auth_helper import login_required
from helpers.views_helper import *
import requests,os,json,mimetypes
from backend import settings
from django.http import HttpResponse
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

url_constants=settings.URLConstants()

class Registration(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                models.User.objects.get(email=email)
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_EXISTS), status=status.HTTP_400_BAD_REQUEST)
            except:
                user=models.User.objects.create(email=email,password=sha1(password.encode()).hexdigest())
                auth=AuthenticationHelper(user.id)
                auth_response = auth.authentication(user,password)
                if(not auth_response):
                    return Response(api_response(ResponseType.FAILED, API_Messages.INCORRECT_PASSWORD), status=status.HTTP_400_BAD_REQUEST)
                
                access_token = auth.generate_access_token()
                data = {
                    'user': user.id,
                    'email': user.email,
                    'access_token': access_token
                    }
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_REGISTRATION,data))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            try:
                user=models.User.objects.get(email=email)
                auth=AuthenticationHelper(user.id)
                auth_response = auth.authentication(user,password)
                if(not auth_response):
                    return Response(api_response(ResponseType.FAILED, API_Messages.INCORRECT_PASSWORD), status=status.HTTP_400_BAD_REQUEST)
                
                access_token = auth.generate_access_token()
                data = {
                    'user': user.id,
                    'email': user.email,
                    'access_token': access_token
                    }
                return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGIN,data))
            except:
                return Response(api_response(ResponseType.FAILED, API_Messages.EMAIL_DOESNOT_EXIST))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    @method_decorator(login_required())
    def post(self, request):
        try:
            token = request.headers['Authorization'].split(" ")[-1]
            models.TokenBlackList.objects.create(token=token)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.SUCCESSFUL_LOGOUT))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)


class Uploading(APIView):
    @method_decorator(login_required())
    def post(self,request):
        try:
            patient_name=request.data.get('patient_name')
            patient_age=request.data.get('patient_age')
            patient_gender=request.data.get('patient_gender')
            myfile = request.FILES['document']
            file=myfile.read()
            data={}
            data['Pneumonia']=pneumonia_detection(file)
            data['Tuberculosis']=tuberculosis_detection(file)
            res=requests.post(url_constants.UPLOAD_URL,files={'upload_file':file}).text
            xray_hash=json.loads(res)['Hash']
            models.PatientDetails.objects.create(
                full_name=patient_name,
                age=patient_age,
                gender=patient_gender,
                xray_hash=xray_hash,
                pneumonia_result=data['Pneumonia'],
                tuberculosis_result=data['Tuberculosis']
                )
            return Response(api_response(ResponseType.SUCCESS, API_Messages.FILE_UPLOADED,data))
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)


""" class Downloading(APIView):
    @method_decorator(login_required())
    def post(self,request):
        try:
            private_key=request.data.get('private_key')
            tx_hash=request.data.get('tx_hash')
            xray_hash=get_xray_hash(tx_hash)
            file_name=models.FileDetails.objects.get(xray_data=sha1(xray_hash.encode()).hexdigest()).name
            r=requests.get(url_constants.DOWNLOAD_URL+xray_hash,stream=True, verify=False, 
                headers={"Accept-Encoding": "identity"})
            
            content_type, encoding = mimetypes.guess_type(file_name)
            file=decrypt(private_key, r.content)
            response = HttpResponse(file, content_type=content_type)
            response['Content-Disposition']=f'attachment; filename={file_name}'
            response['file_name']=file_name
            return response
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)
 """