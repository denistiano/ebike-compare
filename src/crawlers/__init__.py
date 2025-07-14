"""
E-Bike Crawler Package

This package contains crawlers for various e-bike manufacturer websites.
Designed to run in GitHub Actions for automated data collection.
"""

from .crawler import run_crawler

__version__ = "2.0.0"
__all__ = ['run_crawler'] 