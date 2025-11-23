from django.conf import settings

class ContentSecurityPolicyMiddleware:
    """
    Middleware to add Content Security Policy (CSP) headers to responses.
    This helps prevent XSS attacks by restricting the sources of content.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Build CSP header from settings
        csp_parts = []
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_parts.append(f"default-src {' '.join(settings.CSP_DEFAULT_SRC)}")
        if hasattr(settings, 'CSP_SCRIPT_SRC'):
            csp_parts.append(f"script-src {' '.join(settings.CSP_SCRIPT_SRC)}")
        if hasattr(settings, 'CSP_STYLE_SRC'):
            csp_parts.append(f"style-src {' '.join(settings.CSP_STYLE_SRC)}")
        if hasattr(settings, 'CSP_IMG_SRC'):
            csp_parts.append(f"img-src {' '.join(settings.CSP_IMG_SRC)}")
        if hasattr(settings, 'CSP_FONT_SRC'):
            csp_parts.append(f"font-src {' '.join(settings.CSP_FONT_SRC)}")

        if csp_parts:
            csp_header = "; ".join(csp_parts)
            response['Content-Security-Policy'] = csp_header

        return response