def get_descendants(menu):
    descendants = set(menu.children.all())
    for child in menu.children.all():
        descendants.update(get_descendants(child))
    return descendants


def get_ancestors(menu):
    """Recursively collect all ancestors of a menu including itself."""
    
    ancestors = []
    current = menu
    while current:
        ancestors.append(current)
        current = current.parent
    return ancestors