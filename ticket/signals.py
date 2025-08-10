from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket

def send_notification_email(subject, message, recipient_email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )
    
@receiver(pre_save, sender=Ticket)
def cache_old_assigned_to(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Ticket.objects.get(pk=instance.pk)
            instance._old_assigned_to = old_instance.assigned_to
        except Ticket.DoesNotExist:
            instance._old_assigned_to = None
    else:
        instance._old_assigned_to = None


@receiver(post_save, sender=Ticket)
def ticket_notification(sender, instance, created, **kwargs):
    if hasattr(instance, '_notification_sent') and instance._notification_sent:
        return  # skip duplicate

    creator = instance.created_by
    old_assigned_to = getattr(instance, '_old_assigned_to', None)
    new_assigned_to = instance.assigned_to

    if created:
        # Ticket Created
        subject = f"Ticket Created: {instance.title}"
        message = f"Hello {creator.username},\n\nYour ticket '{instance.title}' has been created successfully."
        send_notification_email(subject, message, creator.email)

    else:
        # Ticket updated or assigned/reassigned
        if old_assigned_to != new_assigned_to:
            # Assigned or reassigned case
            subject = f"Ticket Assigned: {instance.title}"
            if new_assigned_to:
                message = f"Hello {new_assigned_to.username},\n\nYou have been assigned to ticket '{instance.title}'."
                send_notification_email(subject, message, new_assigned_to.email)

            creator_message = f"Hello {creator.username},\n\nYour ticket '{instance.title}' has been assigned to {new_assigned_to.username if new_assigned_to else 'no one'}."
            send_notification_email(subject, creator_message, creator.email)

        else:
            # Only updated
            subject = f"Ticket Updated: {instance.title}"
            message = f"Hello {creator.username},\n\nYour ticket '{instance.title}' has been updated."
            send_notification_email(subject, message, creator.email)

    # Mark that notification was sent for this save cycle
    instance._notification_sent = True


@receiver(m2m_changed, sender=Ticket.menu.through)
def ticket_menu_assigned(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        creator = instance.created_by
        subject = f"Ticket Assignment Updated: {instance.title}"
        message = f"Hello {creator.username},\n\nThe assignment of menus for your ticket '{instance.title}' has been updated."
        send_notification_email(subject, message, creator.email)
