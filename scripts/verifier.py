import re
from app.config import settings


def email_verifier(email: str):
    regex_pattern = rf"^{settings.admin_reg}"
    
    if re.search(regex_pattern, email):
        return True