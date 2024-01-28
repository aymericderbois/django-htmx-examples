import calendar

from django import template

register = template.Library()


@register.filter
def day_name(value: int):
    """Retourne le nom du jour à partir de son numéro dans la semaine

    Parameters
    ----------
    value : int
        le numéro du jour dans la semaine, lundi étant 0 et dimanche étant 6

    Returns
    -------
    str : le nom du jour

    """
    return calendar.day_name[value]


@register.filter
def month_name(value: int):
    """Retourne le nom du mois à partir de son numéro

    Parameters
    ----------
    value : int
        le numéro du jour dans la semaine, janvier étant 1 et décembre étant 12

    Returns
    -------
    str : le nom du mois

    """
    return calendar.month_name[value]
