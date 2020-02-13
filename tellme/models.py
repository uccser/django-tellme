from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible

PRIORITY_URGENT = "U"
PRIORITY_HIGH   = "H"
PRIORITY_NORMAL = "N"
PRIORITY_LOW    = "L"
PRIORITY_FLOOR  = "F"
PRIORITY_NONE   = "-"

PRIORITY_CHOICES = (
    (PRIORITY_URGENT, "Urgent"),
    (PRIORITY_HIGH,   "High"),
    (PRIORITY_NORMAL, "Normal"),
    (PRIORITY_LOW,    "Low"),
    (PRIORITY_FLOOR,  "Floor"),
    (PRIORITY_NONE,   "Unassigned")
)


@python_2_unicode_compatible
class Feedback(models.Model):
    url = models.CharField(_('Url'), max_length=255)
    browser = models.TextField(_('Browser'))
    comment = models.TextField(_('Comment'))
    screenshot = models.ImageField(_('Screenshot'), blank=True, null=True, upload_to="tellme/screenshots/")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    created = models.DateTimeField(_('Creation date'), auto_now_add=True, db_index=True)

    priority = models.CharField(max_length=1, blank=True, choices=PRIORITY_CHOICES, default=PRIORITY_NONE)

    ack = models.BooleanField(_('Resolved'), default=False)

    class Meta:
        verbose_name = _("feedback")
        verbose_name_plural = _("feedbacks")

    def __str__(self):
        return '%s: %s' % (self.created, self.url)


@receiver(post_delete, sender=Feedback)
def feedback_screenshot_delete(sender, instance, **kwargs):
    """
    Delete feedback's screenshot.
    """
    if instance.screenshot:
        instance.screenshot.delete(save=False)
