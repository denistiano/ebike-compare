"""
Website configurations for e-bike crawlers.

This configuration defines websites to crawl, their URL patterns,
and CSS selectors for extracting product data.
"""

WEBSITES = {
    "trek_international": {
        "name": "Trek International",
        "base_url": "https://www.trekbikes.com",
        "product_url_template": "https://www.trekbikes.com/international/en_IN_TL/bikes/{product_id}",
        "languages": ["en-US"],
        "discovery": {
            "url": "https://www.trekbikes.com/international/en_IN_TL/bikes/electric-bikes/c/B507/",
            "product_link_selector": "li.productListItem a",
            "pagination_selector": ".pagination .next, .load-more-button"
        },
        "selectors": {
            "name": "h1.buying-zone__title",
            "price": ".bike-header__price .price, .pdp-price .current-price",
            "description": ".bike-description, .pdp-description",
            "battery": ".spec-list .spec-item:contains('Battery') .spec-value, td:contains('Battery') + td",
            "motor_type": ".spec-list .spec-item:contains('Motor') .spec-value, td:contains('Motor') + td",
            "max_speed": ".spec-list .spec-item:contains('Speed') .spec-value, td:contains('Speed') + td",
            "range": ".spec-list .spec-item:contains('Range') .spec-value, td:contains('Range') + td",
            "weight": ".spec-list .spec-item:contains('Weight') .spec-value, td:contains('Weight') + td",
            "max_load": ".spec-list .spec-item:contains('Capacity') .spec-value, td:contains('Capacity') + td",
            "images": ".bike-gallery__image img, .pdp-gallery img"
        }
    },
    "specialized_usa": {
        "name": "Specialized USA",
        "base_url": "https://www.specialized.com",
        "product_url_template": "https://www.specialized.com/us/en/bikes/{product_id}",
        "languages": ["en-US"],
        "discovery": {
            "url": "https://www.specialized.com/us/en/shop/bikes/c/bikes",
            "product_link_selector": ".product-tile a, .bike-card__link",
            "pagination_selector": ".pagination .next, .load-more"
        },
        "selectors": {
            "name": "h1.product-name, .bike-header__name h1",
            "price": ".pdp-price .current-price, .bike-price .price",
            "description": ".pdp-description, .bike-description",
            "battery": ".tech-specs .spec:contains('Battery') .spec-value, td:contains('Battery') + td",
            "motor_type": ".tech-specs .spec:contains('Motor') .spec-value, td:contains('Motor') + td",
            "max_speed": ".tech-specs .spec:contains('Speed') .spec-value, td:contains('Speed') + td",
            "range": ".tech-specs .spec:contains('Range') .spec-value, td:contains('Range') + td",
            "weight": ".tech-specs .spec:contains('Weight') .spec-value, td:contains('Weight') + td",
            "max_load": ".tech-specs .spec:contains('Capacity') .spec-value, td:contains('Capacity') + td",
            "images": ".pdp-gallery img, .bike-gallery__image img"
        }
    },
    "cube_bikes": {
        "name": "Cube Bikes",
        "base_url": "https://www.cube.eu/de-en",
        "product_url_template": "https://www.cube.eu/de-en/{product_id}",
        "languages": ["de-DE"],
        "discovery": {
            "url": "https://www.cube.eu/de-en/e-bikes/mountainbike/fullsuspension?p=1",
            "product_link_selector": ".card-body a",
            "pagination_selector": ".pagination .next, .load-more-bikes"
        },
        "selectors": {
            "name": "h1.product-detail-name",
            "price": "p.product-detail-price",
            "description": "p.description",
            "battery": ".specs .spec-item:contains('Battery') .spec-value, td:contains('Battery') + td",
            "motor_type": ".specs .spec-item:contains('Motor') .spec-value, td:contains('Motor') + td",
            "max_speed": ".specs .spec-item:contains('Speed') .spec-value, td:contains('Speed') + td",
            "range": ".specs .spec-item:contains('Range') .spec-value, td:contains('Range') + td",
            "weight": ".specs .spec-item:contains('Weight') .spec-value, td:contains('Weight') + td",
            "max_load": ".specs .spec-item:contains('Capacity') .spec-value, td:contains('Capacity') + td",
            "images": "img.cms-image"
        }
    }
} 