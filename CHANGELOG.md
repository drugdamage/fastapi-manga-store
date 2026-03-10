# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog.

---

## [Unreleased]

### Added

* Manga product data model (`ProductCreate`, `ProductOut`)
* Catalog service with in-memory product storage
* Initial manga dataset (Jujutsu Kaisen, Vinland Saga, Chainsaw Man, Tokyo Ghoul, Attack on Titan)
* Homepage with featured manga
* Catalog page with manga cards
* Product detail page
* HTML form for creating new manga items
* Basic CSS styling for layout and cards
* API endpoints for manga items

### Fixed

* Route conflict between `/products/new` and `/products/{product_id}`

---

## [0.1.0] - Initial project setup

### Added

* FastAPI application structure
* Router layer
* Service layer
* Models layer
* Jinja2 template support
* Static files support
* OpenAPI documentation
