# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin.

"""

from lino.api import dd, rt, _
from lino.utils import join_words
from lino.mixins import  Hierarchical

from lino_xl.lib.contacts.models import *
from lino.modlib.comments.mixins import Commentable


PartnerDetail.address_box = dd.Panel("""
    name_box
    country #region city zip_code:10
    #addr1
    #street_prefix street:25 street_no street_box
    #addr2
    """)  # , label=_("Address"))

PartnerDetail.contact_box = dd.Panel("""
    url
    phone
    gsm #fax
    """, label=_("Contact"))

# from lino_xl.lib.addresses.mixins import AddressOwner
# from lino_xl.lib.phones.mixins import ContactDetailsOwner

@dd.python_2_unicode_compatible
class Person(Person, Commentable):
    
    class Meta(Person.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Person')
        
    def __str__(self):
        words = []
        words.append(self.first_name)
        words.append(self.last_name)
        return join_words(*words)

    def get_address_parent(self):
        p = super(Person, self).get_address_parent()
        if p is None:
            Member = rt.models.households.Member
            try:
                return Member.objects.get(
                    person=self, primary=True).household
            except Member.DoesNotExist:
                pass
        
    # def get_overview_elems(self, ar):
    #     elems = super(Person, self).get_overview_elems(ar)
    #     elems += AddressOwner.get_overview_elems(self, ar)
    #     elems += ContactDetailsOwner.get_overview_elems(self, ar)
    #     return elems

    @classmethod
    def setup_parameters(cls, fields):
        fields.setdefault(
            'company', models.ForeignKey(
                'contacts.Company', blank=True, null=True))
        fields.setdefault(
            'function', models.ForeignKey(
                'contacts.RoleType', blank=True, null=True))
        fields.setdefault(
            'topic', models.ForeignKey(
                'topics.Topic', blank=True, null=True))
        super(Person, cls).setup_parameters(fields)
    
    @classmethod
    def get_simple_parameters(cls):
        lst = list(super(Person, cls).get_simple_parameters())
        lst.append('company')
        lst.append('function')
        lst.append('topic')
        return lst
    
    @classmethod
    def add_param_filter(cls, qs, lookup_prefix='', company=None,
                         function=None,
                         topic=None, **kwargs):
        qs = super(Person, cls).add_param_filter(qs, **kwargs)
        if company:
            fkw = dict()
            wanted = company.whole_clan()
            fkw[lookup_prefix + 'rolesbyperson__company__in'] = wanted
            qs = qs.filter(**fkw)
        
        if function:
            fkw = dict()
            fkw[lookup_prefix + 'rolesbyperson__type'] = function
            qs = qs.filter(**fkw)
        
        if topic:
            fkw = dict()
            wanted = topic.whole_clan()
            fkw[lookup_prefix + 'interest_set__topic__in'] = wanted
        return qs
        

    # @classmethod
    # def get_request_queryset(cls, ar):
    #     qs = super(Person, cls).get_request_queryset(ar)
    #     pv = ar.param_values
    #     if pv.skill:
    #     return qs

# We use the `overview` field only in detail forms, and we
# don't want it to have a label "Description":
dd.update_field(Person, 'overview', verbose_name=None)    

class Company(Company, Hierarchical, Commentable):
    
    class Meta(Company.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Company')
        

    # def get_overview_elems(self, ar):
    #     elems = super(Company, self).get_overview_elems(ar)
    #     # elems += AddressOwner.get_overview_elems(self, ar)
    #     elems += ContactDetailsOwner.get_overview_elems(self, ar)
    #     return elems


class PersonDetail(PersonDetail):
    
    main = "general #contact #career links more"

    general = dd.Panel("""
    overview contact_box #phones.ContactDetailsByPartner
    contacts.RolesByPerson:30 lists.MembersByPartner:30 uploads.UploadsByController:20
    """, label=_("General"))

    contact_box = dd.Panel("""
    last_name first_name:15 
    gender #title:10 language:10 
    birth_date age:10 id:6
    """)  #, label=_("Contact"))

    # contact = dd.Panel("""
    # address_box
    # remarks
    # """, label=_("Contact"))

    # career = dd.Panel("""
    # cv.StudiesByPerson
    # # cv.TrainingsByPerson
    # cv.ExperiencesByPerson:40
    # """, label=_("Career"))

    links = dd.Panel("""
    humanlinks.LinksByHuman:30
    households.MembersByPerson:20 households.SiblingsByPerson:50
    """, label=_("Links"))

    more = dd.Panel("""
    remarks  checkdata.ProblemsByOwner
    comments.CommentsByRFC:30
    """, label=_("More"))


class CompaniesByCompany(Companies):
    label = _("Child organisations")
    master_key = 'parent'
    column_names = 'name_column email id *'

    
class CompanyDetail(CompanyDetail):
    main = "general contact more"

    general = dd.Panel("""
    overview general_middle address_box 
    contacts.RolesByCompany:30 lists.MembersByPartner:30 uploads.UploadsByController:20
    """, label=_("General"))

    general_middle = """
    id:6
    language:10 
    parent
    """
    contact = dd.Panel("""
    # address_box
    remarks 
    """, label=_("Contact"))

    more = dd.Panel("""
    CompaniesByCompany checkdata.ProblemsByOwner
    comments.CommentsByRFC
    """, label=_("More"))

    

# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.models.contacts
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())

Companies.set_detail_layout(CompanyDetail())
Persons.set_detail_layout(PersonDetail())
Person.column_names = 'last_name first_name gsm email city *'
Persons.params_layout = 'observed_event start_date end_date company function topic'
