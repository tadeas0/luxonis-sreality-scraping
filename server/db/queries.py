select_estates_images = b"""
    SELECT estate.id, estate.name, url FROM estate
    LEFT JOIN image ON estate.id = image.estate_id
    ORDER BY id;
    """
