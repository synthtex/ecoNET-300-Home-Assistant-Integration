"""Functionsd used in Econet300 integration"""
import re


def camel_to_snake(key: str) -> str:
    """Converting camel case return from api ti snake case to mach translations keys structure"""
    key = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", key).lower()
