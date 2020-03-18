from rules import *


@predicate
def has_post(user):
    if not hasattr(user, 'person'):
        return False
    return user.person.post_set.exists()

@predicate
def of_post(user, report):
    if not hasattr(user, 'person'):
        return False
    if report is None:
        return True
    return user.person.post_set.filter(id=report.post.id).exists()


add_perm('uawg', always_allow)

add_perm('uawg.view_post', always_allow)
add_perm('uawg.add_post', is_superuser)
add_perm('uawg.change_post', is_superuser)
add_perm('uawg.delete_post', is_superuser)

add_perm('uawg.view_task', always_allow)
add_perm('uawg.add_task', is_superuser)
add_perm('uawg.change_task', is_superuser)
add_perm('uawg.delete_task', is_superuser)

add_perm('uawg.view_report', always_allow)
add_perm('uawg.add_report', has_post)
add_perm('uawg.change_report', of_post)
add_perm('uawg.delete_report', of_post)

add_perm('uawg.view_reportattachment', always_allow)
add_perm('uawg.add_reportattachment', always_allow)
add_perm('uawg.change_reportattachment', always_allow)
add_perm('uawg.delete_reportattachment', always_allow)
