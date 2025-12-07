from apps.users.models import CustomUser
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from datetime import datetime
import uuid
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile
import zipfile
import os


def square_avatar(image_file, size=300):
    # 1. Rasmni ochish
    image = Image.open(image_file)

    # 2. EXIF orientatsiyasini tuzatish (agar mavjud bo'lsa)
    image = ImageOps.exif_transpose(image)

    width, height = image.size

    # 3. Markazdan kvadrat kesish
    if width > height:
        # eni katta, horizontal kesish
        left = (width - height) / 2
        top = 0
        right = left + height
        bottom = height
    else:
        # bo'y katta, vertikal kesish
        left = 0
        top = (height - width) / 2
        right = width
        bottom = top + width

    image = image.crop((left, top, right, bottom))

    # 4. Resize va RGB ga o'tkazish
    image = image.resize((size, size), resample=Image.Resampling.LANCZOS)
    image = image.convert("RGB")

    # 5. ContentFile ga tayyorlash
    img_io = BytesIO()
    image.save(img_io, format='JPEG')  # doim JPG
    new_filename = f"{uuid.uuid4().hex}.jpg"
    
    return new_filename, ContentFile(img_io.getvalue(), new_filename)


def Paths(request):
    path = {path:path.split('-')[0] for path in request.path.strip('/').split('/') if path}
    return path

def get_base_context(request):

    if request.user.is_authenticated:
        # notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        
        return {
            'current_year': datetime.now().year,
            'paths': Paths(request),
            # 'notifications': notifications[:3],
            # 'notifications_unread': notifications.count(),
        }
    
    return {
        'current_year': datetime.now().year,
        'paths': Paths(request),
    }

def get_pagination_range(current_page, total_pages, delta=1):
    range_with_dots = []
    left = current_page - delta
    right = current_page + delta + 1
    range_with_dots.append(1)

    if left > 2:
        range_with_dots.append('...')

    for i in range(max(left, 2), min(right, total_pages)):
        range_with_dots.append(i)

    if right < total_pages:
        range_with_dots.append('...')

    if total_pages > 1:
        range_with_dots.append(total_pages)

    return range_with_dots