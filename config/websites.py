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
    "riese_muller": {
        "name": "Riese & Müller",
        "base_url": "https://www.r-m.de",
        "product_url_template": "https://www.r-m.de/en-gb/bikes/{product_id}",
        "languages": ["en-GB"],
        "discovery": {
            "url": "https://www.r-m.de/en-gb/bikes/",
            "product_link_selector": ".bike-card a, .product-tile__link",
            "pagination_selector": ".pagination .next, .load-more-button"
        },
        "selectors": {
            "name": "h1.bike-header__title, .product-title h1",
            "price": ".bike-price .price, .product-price .current-price",
            "description": ".bike-description, .product-description",
            "battery": ".specs .spec:contains('Battery') .spec-value, td:contains('Battery') + td",
            "motor_type": ".specs .spec:contains('Motor') .spec-value, td:contains('Motor') + td",
            "max_speed": ".specs .spec:contains('Speed') .spec-value, td:contains('Speed') + td",
            "range": ".specs .spec:contains('Range') .spec-value, td:contains('Range') + td",
            "weight": ".specs .spec:contains('Weight') .spec-value, td:contains('Weight') + td",
            "max_load": ".specs .spec:contains('Load') .spec-value, td:contains('Load') + td",
            "images": ".bike-gallery img, .product-gallery__image img"
        }
    },
    "haibike": {
        "name": "Haibike (Germany)",
        "base_url": "https://www.haibike.com/de-en/",
        "product_url_template": "https://www.haibike.com/en-gb/p/{product_id}",
        "languages": ["en-GB"],
        "discovery": {
            "url": "https://www.haibike.com/de-en/e-bikes/",
            "product_link_selector": "a[class^='OProductListXL']",
            "pagination_selector": ".pagination .next, .load-more"
        },
        "selectors": {
            "name": "h1#phpHeading",
            "price": "",
            "description": ".bike-description, .product-description",
            "battery": ".technical-data .data-item:contains('Battery') .data-value, td:contains('Battery') + td",
            "motor_type": ".technical-data .data-item:contains('Motor') .data-value, td:contains('Motor') + td",
            "max_speed": ".technical-data .data-item:contains('Speed') .data-value, td:contains('Speed') + td",
            "range": ".technical-data .data-item:contains('Range') .data-value, td:contains('Range') + td",
            "weight": ".technical-data .data-item:contains('Weight') .data-value, td:contains('Weight') + td",
            "max_load": ".technical-data .data-item:contains('Capacity') .data-value, td:contains('Capacity') + td",
            "images": ".bike-gallery img, .product-images img"
        }
    },
    "cube_bikes": {
        "name": "Cube Bikes (Germany)",
        "base_url": "https://www.cube.eu/de-en",
        "product_url_template": "https://www.cube.eu/de-en/{product_id}",
        "languages": ["de-DE"],
        "discovery": {
            "url": "https://www.cube.eu/de-en/e-bikes/mountainbike/fullsuspension?p=1&properties=53b292582427f4349523b4645759aa0c%7Cd7444edf313781d247b1b86f82e5954e%7Cbd7dab28a50b9c5e732aef2e14682beb%7Cd503341559d0d56510a9dfcc459130d8%7C0cb7c8524598174d3227a316b9d8ec0f%7C88b2cd9d3053fb9461ba5a2cf0234e9b",
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
    },
    # "gazelle": {
    #     "name": "Gazelle",
    #     "base_url": "https://www.gazelle.com",
    #     "product_url_template": "https://www.gazelle.com/en/bikes/{product_id}",
    #     "languages": ["en-GB", "de-DE", "nl-NL"],
    #     "discovery": {
    #         "url": "https://www.gazelle.com/en/bikes/",
    #         "product_link_selector": ".bike-card a, .product-grid__item a",
    #         "pagination_selector": ".pagination .next, .load-more"
    #     },
    #     "selectors": {
    #         "name": "h1.bike-title, .product-header__title h1",
    #         "price": ".bike-price .price, .product-price .current-price",
    #         "description": ".bike-description, .product-description",
    #         "battery": ".specifications .spec:contains('Battery') .spec-value, td:contains('Battery') + td",
    #         "motor_type": ".specifications .spec:contains('Motor') .spec-value, td:contains('Motor') + td",
    #         "max_speed": ".specifications .spec:contains('Speed') .spec-value, td:contains('Speed') + td",
    #         "range": ".specifications .spec:contains('Range') .spec-value, td:contains('Range') + td",
    #         "weight": ".specifications .spec:contains('Weight') .spec-value, td:contains('Weight') + td",
    #         "max_load": ".specifications .spec:contains('Capacity') .spec-value, td:contains('Capacity') + td",
    #         "images": ".bike-gallery img, .product-images img"
    #     }
    # },
    # "canyon": {
    #     "name": "Canyon",
    #     "base_url": "https://www.canyon.com",
    #     "product_url_template": "https://www.canyon.com/en-us/bikes/{product_id}",
    #     "languages": ["en-US", "en-GB", "de-DE", "fr-FR"],
    #     "discovery": {
    #         "url": "https://www.canyon.com/en-us/bikes/",
    #         "product_link_selector": ".productTile__link, .bike-card a",
    #         "pagination_selector": ".pagination .next, .loadMore"
    #     },
    #     "selectors": {
    #         "name": "h1.productTitle, .bike-header__title h1",
    #         "price": ".productConfiguration__price .price, .bike-price .current-price",
    #         "description": ".productDescription, .bike-description",
    #         "battery": ".productSpecifications .spec:contains('Battery') .spec-value, td:contains('Battery') + td",
    #         "motor_type": ".productSpecifications .spec:contains('Motor') .spec-value, td:contains('Motor') + td",
    #         "max_speed": ".productSpecifications .spec:contains('Speed') .spec-value, td:contains('Speed') + td",
    #         "range": ".productSpecifications .spec:contains('Range') .spec-value, td:contains('Range') + td",
    #         "weight": ".productSpecifications .spec:contains('Weight') .spec-value, td:contains('Weight') + td",
    #         "max_load": ".productSpecifications .spec:contains('Load') .spec-value, td:contains('Load') + td",
    #         "images": ".productGallery img, .bike-gallery img"
    #     }
    # },
    # "moustache_bikes": {
    #     "name": "Moustache Bikes",
    #     "base_url": "https://moustachebikes.com",
    #     "product_url_template": "https://moustachebikes.com/en/bikes/{product_id}",
    #     "languages": ["en-GB", "fr-FR", "de-DE"],
    #     "discovery": {
    #         "url": "https://moustachebikes.com/en/bikes/",
    #         "product_link_selector": ".bike-card a, .product-tile__link",
    #         "pagination_selector": ".pagination .next, .load-more"
    #     },
    #     "selectors": {
    #         "name": "h1.bike-title, .product-header__name h1",
    #         "price": ".bike-price .price, .product-price .current-price",
    #         "description": ".bike-description, .product-description",
    #         "battery": ".bike-specs .spec:contains('Battery') .spec-value, td:contains('Battery') + td",
    #         "motor_type": ".bike-specs .spec:contains('Motor') .spec-value, td:contains('Motor') + td",
    #         "max_speed": ".bike-specs .spec:contains('Speed') .spec-value, td:contains('Speed') + td",
    #         "range": ".bike-specs .spec:contains('Range') .spec-value, td:contains('Range') + td",
    #         "weight": ".bike-specs .spec:contains('Weight') .spec-value, td:contains('Weight') + td",
    #         "max_load": ".bike-specs .spec:contains('Load') .spec-value, td:contains('Load') + td",
    #         "images": ".bike-gallery img, .product-gallery img"
    #     }
    # },
    # "engwe_us": {
    #     "name": "Engwe US",
    #     "base_url": "https://engwe-bikes.com",
    #     "product_url_template": "https://engwe-bikes.com/collections/all-ebikes/products/{product_id}",
    #     "languages": ["en-US"],
    #     "discovery": {
    #         "url": "https://engwe-bikes.com/collections/all-ebikes",
    #         "product_link_selector": "div.block-inner > div.block-inner-inner > div.image-cont.image-cont--with-secondary-image.image-cont--same-aspect-ratio > a.product-link",
    #         "pagination_selector": "a.pagination__item[rel='next']"
    #     },
    #     "selectors": {
    #         "name": ".title-row > h1",
    #         "price": ".current-price > span",
    #         "description": ".title-row > p",
    #         "battery": "cell:contains('Battery') + cell",
    #         "motor_type": "cell:contains('Motor') + cell",
    #         "max_speed": "cell:contains('Speed') + cell",
    #         "range": "cell:contains('Range') + cell",
    #         "weight": "cell:contains('Weight') + cell",
    #         "max_load": "cell:contains('Load') + cell",
    #         "images": ".product-detail a.show-gallery img"
    #     }
    # },
    # "engwe_eu": {
    #     "name": "Engwe EU",
    #     "base_url": "https://engwe-bikes-eu.com",
    #     "product_url_template": "https://engwe-bikes-eu.com/products/{product_id}",
    #     "languages": ["en-GB"],
    #     "discovery": {
    #         "url": "https://engwe-bikes-eu.com/collections/eu-warehouse",
    #         "product_link_selector": "#filter-results > ul > li > product-card > div.card__media.has-hover-image.relative > a",
    #         "pagination_selector": "a.pagination__item[rel='next']"
    #     },
    #     "selectors": {
    #         "name": "div.product-info > div.product-info__block.product-info__block--sm.product-info__title > h1",
    #         "price": "div.product-info > div.product-info__block.product-info__block--sm.product-price > div > div.price > div.price__default > strong > span",
    #         "description": "div.product-meta__description",
    #         "battery": "td:contains('Battery') + td",
    #         "motor_type": "td:contains('Motor') + td",
    #         "max_speed": "td:contains('Speed') + td",
    #         "range": "td:contains('Range') + td",
    #         "weight": "td:contains('Weight') + td",
    #         "max_load": "td:contains('Load') + td",
    #         "images": "img.product-image"
    #     }
    # },
    # "fiido": {
    #     "name": "Fiido",
    #     "base_url": "https://fiido.com",
    #     "product_url_template": "https://fiido.com/products/{product_id}",
    #     "languages": ["en-US"],
    #     "discovery": {
    #         "url": "https://fiido.com/collections/electric-bikes",
    #         "product_link_selector": "a.product-item__title",
    #         "pagination_selector": "a.pagination__nav-item[data-page]"
    #     },
    #     "selectors": {
    #         "name": "h1.product-meta__title",
    #         "price": "span.price.price--highlight, span.price:not(.price--compare)",
    #         "description": "div.product-meta__description-container",
    #         "battery": "div.pi-sp:contains('Battery')",
    #         "motor_type": "div.pi-sp:contains('Motor')",
    #         "max_speed": "div.pi-sp:contains('Speed')",
    #         "range": "div.pi-sp:contains('Range')",
    #         "weight": "div.pi-sp:contains('Weight')",
    #         "max_load": "div.pi-sp:contains('Load')",
    #         "images": "img.product-gallery__image"
    #     }
    # },
    # "rad_power_bikes_us": {
    #     "name": "Rad Power Bikes (US)",
    #     "base_url": "https://www.radpowerbikes.com",
    #     "product_url_template": "https://www.radpowerbikes.com/products/{product_id}",
    #     "languages": ["en-US"],
    #     "discovery": {
    #         "url": "https://www.radpowerbikes.com/collections/electric-bikes",
    #         "product_link_selector": ".card a.product-link",
    #         "pagination_selector": ".pagination__item--next a, .pagination .next"
    #     },
    #     "selectors": {
    #         "name": "h2.product-title",
    #         "price": "span.price",
    #         "description": ".product-single__description, .product__description",
    #         "battery": "td:contains('Battery') + td, .spec-item:contains('Battery') .spec-value",
    #         "motor_type": "td:contains('Motor') + td, .spec-item:contains('Motor') .spec-value",
    #         "max_speed": "td:contains('Speed') + td, .spec-item:contains('Speed') .spec-value",
    #         "range": "td:contains('Range') + td, .spec-item:contains('Range') .spec-value",
    #         "weight": "td:contains('Weight') + td, .spec-item:contains('Weight') .spec-value",
    #         "max_load": "td:contains('Load') + td, .spec-item:contains('Capacity') .spec-value",
    #         "images": ".product-media-parent img"
    #     }
    # },
    # "rad_power_bikes_eu": {
    #     "name": "Rad Power Bikes (EU)",
    #     "base_url": "https://www.radpowerbikes.eu",
    #     "product_url_template": "https://www.radpowerbikes.com/products/{product_id}",
    #     "languages": ["en-US"],
    #     "discovery": {
    #         "url": "https://www.radpowerbikes.com/collections/electric-bikes",
    #         "product_link_selector": ".product-card-wrapper a.product-card__link, .grid-product__link",
    #         "pagination_selector": ".pagination__item--next a, .pagination .next"
    #     },
    #     "selectors": {
    #         "name": "h1.product-single__title, .product-single__meta h1",
    #         "price": ".product__price .money, .price .current-price",
    #         "description": ".product-single__description, .product__description",
    #         "battery": "td:contains('Battery') + td, .spec-item:contains('Battery') .spec-value",
    #         "motor_type": "td:contains('Motor') + td, .spec-item:contains('Motor') .spec-value",
    #         "max_speed": "td:contains('Speed') + td, .spec-item:contains('Speed') .spec-value",
    #         "range": "td:contains('Range') + td, .spec-item:contains('Range') .spec-value",
    #         "weight": "td:contains('Weight') + td, .spec-item:contains('Weight') .spec-value",
    #         "max_load": "td:contains('Load') + td, .spec-item:contains('Capacity') .spec-value",
    #         "images": ".product-media-parent img"
    #     }
    # },
    # "aventon": {
    #     "name": "Aventon",
    #     "base_url": "https://www.aventon.com",
    #     "product_url_template": "https://www.aventon.com/products/{product_id}",
    #     "languages": ["en-US"],
    #     "discovery": {
    #         "url": "https://www.aventon.com/collections/ebikes",
    #         "product_link_selector": ".product-card a, .grid-view-item__link",
    #         "pagination_selector": ".pagination__item--next a, .pagination .next"
    #     },
    #     "selectors": {
    #         "name": ".buyBox__details-title h1",
    #         "price": "span.buyBox__details-product-price",
    #         "description": ".product-single__description, .product__description",
    #         "battery": "td:contains('Battery') + td, .spec-item:contains('Battery') .spec-value",
    #         "motor_type": "td:contains('Motor') + td, .spec-item:contains('Motor') .spec-value",
    #         "max_speed": "td:contains('Speed') + td, .spec-item:contains('Speed') .spec-value",
    #         "range": "td:contains('Range') + td, .spec-item:contains('Range') .spec-value",
    #         "weight": "td:contains('Weight') + td, .spec-item:contains('Weight') .spec-value",
    #         "max_load": "td:contains('Payload') + td, .spec-item:contains('Payload') .spec-value",
    #         "images": ".product-single__photos img, .product__main-photos img"
    #     }
    # },
    # "lectric_ebikes": {
    #     "name": "Lectric eBikes",
    #     "base_url": "https://lectricebikes.com",
    #     "product_url_template": "https://lectricebikes.com/products/{product_id}",
    #     "languages": ["en-US"],
    #     "discovery": {
    #         "url": "https://lectricebikes.com/collections/ebikes",
    #         "product_link_selector": "div.card-product-media a",
    #         "pagination_selector": ".pagination__item--next a, .pagination .next"
    #     },
    #     "selectors": {
    #         "name": "h1.product-title, .product-title h1",
    #         "price": "span.new-price",
    #         "description": ".product__description, .product-single__description",
    #         "battery": "h3:contains('Battery') + p",
    #         "motor_type": "td:contains('Motor') + td, .spec-grid .spec-item:contains('Motor') .spec-value",
    #         "max_speed": "td:contains('Speed') + td, .spec-grid .spec-item:contains('Speed') .spec-value",
    #         "range": "td:contains('Range') + td, .spec-grid .spec-item:contains('Range') .spec-value",
    #         "weight": "td:contains('Weight') + td, .spec-grid .spec-item:contains('Weight') .spec-value",
    #         "max_load": "td:contains('Payload') + td, .spec-grid .spec-item:contains('Payload') .spec-value",
    #         "images": "#gallery-main img"
    #     }
    # }
}