import os
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Panammun_edition, Committee, Country
from .serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.shortcuts import redirect
from PIL import Image 
import io
from django.db import transaction

def is_admin(user):
    return user.is_authenticated and user.account_type == 'administrator'

def is_normal(user):
    return user.is_authenticated and user.account_type == 'normal_user'



def home_page(request):
    
    return render(request, "index.html")

def meet_us(request):
    
    return render(request, "meet_us.html")

def create_account(request):
    current_edition = Panammun_edition.objects.filter(actual=True).first()
    context = {
        'current_edition': current_edition
    }
    
    return render(request, 'create_account.html', context)


def compress_image(image_file, max_size=5120):

    with Image.open(image_file) as img:
        original_size = img.size[0] * img.size[1] * 3 / 1024 
        if original_size > max_size: 
            original_size = max_size

        quality = max(20, int(65 - (original_size / max_size) * 40))
        quality = min(95, quality)
        
        output_buffer = io.BytesIO()
        img.save(output_buffer, format=img.format, quality=quality)

        return output_buffer.getvalue()

@user_passes_test(is_admin)
def admin_panel_page(request):
    current_edition = Panammun_edition.objects.filter(actual=True).first()
    
    users = CustomUser.objects.filter(
        panammun_edition=current_edition, 
        account_type='normal_user'
    ).order_by('last_name')
    no_users = users.count()
    committees = Committee.objects.filter(panammun_edition=current_edition)
    committee_count = committees.count()
    committee_users = {}
    for committee in committees:
        countries = Country.objects.filter(committee=committee)
        users_for_committee = CustomUser.objects.filter(
            panammun_edition=current_edition, 
            account_type='normal_user', 
            country__in=countries
        ).order_by('last_name')
        
        committee_users[committee] = users_for_committee
    
    context = {
        'users': users,
        'no_users': no_users,
        'current_edition': current_edition,
        'edition_name': current_edition.name if current_edition else '',
        'committee_count': committee_count,
        'committee_users': committee_users,
    }
    
    return render(request, "admin_panel.html", context)

@login_required()
def public_panel_page(request):
    current_edition = Panammun_edition.objects.filter(actual=True).first()
    committees = Committee.objects.filter(panammun_edition=current_edition)
    
    committees_with_countries = {}
    for committee in committees:
        countries_without_users = committee.countries.filter(users__isnull=True)
        if countries_without_users.exists():
            committees_with_countries[committee] = countries_without_users
        else:
            committees_with_countries[committee] = ''
            
    date = False
    if current_edition and current_edition.start_choose_date and current_edition.start_mun_date :
        date = timezone.now() >= current_edition.start_choose_date and timezone.now() <= current_edition.start_mun_date 
    
    context = {
        'user': request.user,
        'edition': current_edition,
        'committees_with_countries': committees_with_countries,
        'date': date,
    }
    
    return render(request, "public_panel.html", context)




#APIS
class CreateUserAPIView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if request.content_type.startswith('multipart/form-data'):
            dataP = request.data
            data= dataP
        elif request.content_type == 'application/json':
            dataP = request.data
            data= dataP
        else:
            return Response({'error': 'Unsupported media type'}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        if 'panammun_edition' not in data or not data['panammun_edition']:
            current_panammun_edition = Panammun_edition.objects.filter(actual=True).first()
            if current_panammun_edition:
                data['panammun_edition'] = current_panammun_edition.id
            else:
                return Response({'error': 'not panammun edition activated'}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'voucher' in request.FILES:
            voucher = request.FILES['voucher']
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            new_filename = f"{last_name}_{first_name}_voucher{os.path.splitext(voucher.name)[1]}"
            new_filename = new_filename[:95]
            compressed_image = compress_image(voucher, max_size=5120)
            new_file = InMemoryUploadedFile(
                file=io.BytesIO(compressed_image),
                field_name='voucher',
                name=new_filename,
                content_type=voucher.content_type,
                size=len(compressed_image),
                charset=None
            )
            data['voucher'] = new_file
            
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Cuenta creada.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateUserStatusAPIView(APIView):
    @method_decorator(user_passes_test(is_admin))
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        verified = request.data.get('verified')

        if not user_id or verified is None:
            return Response({'error': 'Missing user ID or verification status.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, id=user_id)

        user.verified = bool(int(verified))
        user.save()

        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AssignCountryView(APIView):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        user = request.user
        country_id = request.data.get('id')

        if not country_id:
            return Response({'error': 'country_id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                country = Country.objects.select_for_update().get(id=country_id)
                
                if CustomUser.objects.filter(country=country).exists():
                    return Response({'error': 'Este país ya tiene un usuario asignado.'}, status=status.HTTP_400_BAD_REQUEST)

                current_edition = Panammun_edition.objects.filter(actual=True).first()
                if not current_edition:
                    return Response({'error': 'No hay una edición actual.'}, status=status.HTTP_400_BAD_REQUEST)

                if timezone.now() < current_edition.start_choose_date:
                    return Response({'error': 'No se puede asignar el país todavía.'}, status=status.HTTP_400_BAD_REQUEST)

                user.country = country
                user.save()

        except Country.DoesNotExist:
            return Response({'error': 'Country no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'País asignado exitosamente.'}, status=status.HTTP_200_OK)
