from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    return dictionary.get(key)

@register.filter
def filter_reactions(reactions, reaction_type):
    """Filter reactions by type"""
    return reactions.filter(reaction=reaction_type)