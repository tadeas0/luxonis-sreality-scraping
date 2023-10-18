create_estate_table = b"""
    CREATE TABLE IF NOT EXISTS estate (
        id serial PRIMARY KEY,
        name varchar(255) NOT NULL,
        sreality_id bigint UNIQUE NOT NULL
    );
    """

create_image_table = b"""
    CREATE TABLE IF NOT EXISTS image (
        id serial PRIMARY KEY,
        url varchar(255) NOT NULL,
        estate_id int NOT NULL,
        FOREIGN KEY (estate_id)
            REFERENCES estate (id)
    );
    """

insert_estate = b"""
    INSERT INTO estate (name, sreality_id)
    VALUES (%s, %s) RETURNING id;
    """

insert_image = b"""
    INSERT INTO image (url, estate_id)
    VALUES (%s, %s)
    """

select_estates_images = b"""
    SELECT estate.id as estate_id,
           estate.sreality_id,
           image.id as image_id,
           estate.name as estate_name,
           url as image_url
    FROM estate
    LEFT JOIN image ON estate.id = image.estate_id
    ORDER BY estate_id;
    """
