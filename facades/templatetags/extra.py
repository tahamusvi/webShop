from django import template
#----------------------------------------------------------------------------------------------
register = template.Library()

@register.filter
def convert_price(price):
    formatted_price = "{:,.0f}".format(price)
    return formatted_price
#----------------------------------------------------------------------------------------------