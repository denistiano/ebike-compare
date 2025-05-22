"""
Configuration for ebike websites to crawl.
Each website configuration includes:
- Base URL
- Product URL template
- Supported languages
- CSS selectors for product attributes
- Discovery configuration for finding products
"""

WEBSITES = {
    "engwe_us": {
        "name": "Engwe US",
        "base_url": "https://engwe-bikes.com",
        "product_url_template": "https://engwe-bikes.com/collections/all-ebikes/products/{product_id}",
        "languages": ["en-US"],
        "discovery": {
            "url": "https://engwe-bikes.com/collections/all-ebikes",
            "product_link_selector": "div.block-inner > div.block-inner-inner > div.image-cont.image-cont--with-secondary-image.image-cont--same-aspect-ratio > a.product-link",
            "pagination_selector": "a.pagination__item[rel='next']"
        },
        "selectors": {
            "name": ".title-row > h1",
            "price": ".current-price > span",
            "description": ".title-row > p",
            "battery": "td:contains('Battery') + td",
            "motor_type": "td:contains('Motor') + td",
            "max_speed": "td:contains('Speed') + td",
            "range": "td:contains('Range') + td",
            "weight": "td:contains('Weight') + td",
            "max_load": "td:contains('Load') + td",
            "images": "img.product-gallery__image"
        }
    },
    "engwe_eu": {
        "name": "Engwe EU",
        "base_url": "https://engwe-bikes-eu.com",
        "product_url_template": "https://engwe-bikes-eu.com/products/{product_id}",
        "languages": ["en-GB"],
        "discovery": {
            "url": "https://engwe-bikes-eu.com/collections/eu-warehouse",
            "product_link_selector": "#filter-results > ul > li > product-card > div.card__media.has-hover-image.relative > a",
            "pagination_selector": "a.pagination__item[rel='next']"
        },
        "selectors": {
            "name": "div.product-info > div.product-info__block.product-info__block--sm.product-info__title > h1",
            "price": "div.product-info > div.product-info__block.product-info__block--sm.product-price > div > div.price > div.price__default > strong > span",
            "description": "div.product-meta__description",
            "battery": "td:contains('Battery') + td",
            "motor_type": "td:contains('Motor') + td",
            "max_speed": "td:contains('Speed') + td",
            "range": "td:contains('Range') + td",
            "weight": "td:contains('Weight') + td",
            "max_load": "td:contains('Load') + td",
            "images": "img.product-gallery__image"
        }
    },
    "fiido": {
        "name": "Fiido",
        "base_url": "https://fiido.com",
        "product_url_template": "https://fiido.com/products/{product_id}",
        "languages": ["en-US"],
        "discovery": {
            "url": "https://fiido.com/collections/electric-bikes",
            "product_link_selector": "a.product-item__title",
            "pagination_selector": "a.pagination__nav-item[data-page]"
        },
        "selectors": {
            "name": "h1.product-meta__title",
            "price": "span.price.price--highlight, span.price:not(.price--compare)",
            "description": "div.product-meta__description-container",
            "battery": "td:contains('Battery') + td, div.product-meta__description-container:contains('Battery')",
            "motor_type": "td:contains('Motor') + td, div.product-meta__description-container:contains('Motor')",
            "max_speed": "td:contains('Speed') + td, div.product-meta__description-container:contains('Speed')",
            "range": "td:contains('Range') + td, div.product-meta__description-container:contains('Range')",
            "weight": "td:contains('Weight') + td, div.product-meta__description-container:contains('Weight')",
            "max_load": "td:contains('Load') + td, div.product-meta__description-container:contains('Load')",
            "images": "img.product-gallery__image"
        }
    }
} 