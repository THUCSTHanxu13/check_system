from rules import *


def belongs_to(person, organization):
    return person.affiliation == organization

@predicate
def can_contact(user, contactee):
    contactor = getattr(user, 'person', None)
    if not contactor:
        return False
    if not contactee:
        return contactor.can_contact.exists()
    for organization in contactor.can_contact.all():
        if belongs_to(contactee, organization):
            return True
    return False

@predicate
def can_approve(user, entry):
    approver = getattr(user, 'person', None)
    if not approver:
        return False
    if not entry:
        return approver.can_approve1.exists() or approver.can_approve2.exists() or approver.can_approve3.exists()
    for organization in approver.can_approve1.all():
        if belongs_to(entry.person, organization):
            return True
    for organization in approver.can_approve2.all():
        if belongs_to(entry.person, organization):
            return True
    for organization in approver.can_approve3.all():
        if belongs_to(entry.person, organization):
            return True
    return False


add_perm('report', always_allow)

add_perm('report.view_person', can_contact)
add_perm('report.view_record', always_allow)
add_perm('report.view_entry', can_approve)
