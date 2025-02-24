import logging
from io import BytesIO
import qrcode

from django.core.files.base import ContentFile
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import EventSubscription

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=EventSubscription)
def generate_check_in_qr_code(sender, instance, raw, **kwargs):
    if not instance.check_in_qr_code:
        try:
            identifier = instance.attendance_indentifier
            qr_image = qrcode.make(identifier)

            img_io = BytesIO()
            qr_image.save(img_io, format="PNG")

            qrcode_path = f"{identifier}.png"
            instance.check_in_qr_code = ContentFile(img_io.getvalue(), name=qrcode_path)
        except Exception as exception:  # pylint: disable=W0718
            logger.exception(
                "An exception was raised during the generation of qrcode for checkin.\
                Exception:  %s, Message: %s",
                type(exception).__name__,
                str(exception),
            )
