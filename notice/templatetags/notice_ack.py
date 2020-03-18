from django import template


register = template.Library()


@register.filter
def acked_by(value, arg):
    notice = value  # XXX: check
    user = arg  # XXX: check
    if notice.to_ack:
        return notice.ack_set.filter(person=user.person).exists()
    else:
        return True
