from lino.api import rt

rt.actors.cal.GuestsByEvent.column_names = 'partner role remark workflow_buttons *'

rt.models.countries.Places.detail_layout = """
name country
type parent zip_code id
addresses.AddressesByCity
contacts.PartnersByCity PlacesByPlace
"""
