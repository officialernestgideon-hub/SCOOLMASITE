from urllib.parse import urlparse

from .models import SiteVisit


class SiteVisitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        # Only track successful HTML page requests
        if (
            request.method == "GET"
            and response.status_code == 200
            and "text/html" in response.get("Content-Type", "")
        ):
            path = request.path

            # Don't track admin, static, media, or Django admin pages
            excluded_paths = (
                "/admin/",
                "/django-admin/",
                "/static/",
                "/media/",
            )

            if not path.startswith(excluded_paths):

                # Make sure the session exists
                if not request.session.session_key:
                    request.session.create()

                user = (
                    request.user
                    if request.user.is_authenticated
                    else None
                )

                # -------------------------------------------------
                # IP ADDRESS
                # -------------------------------------------------

                ip_address = request.META.get(
                    "REMOTE_ADDR"
                )

                # -------------------------------------------------
                # USER AGENT
                # -------------------------------------------------

                user_agent = request.META.get(
                    "HTTP_USER_AGENT",
                    ""
                )

                user_agent_lower = user_agent.lower()

                # -------------------------------------------------
                # REFERRER
                # -------------------------------------------------

                referrer = request.META.get(
                    "HTTP_REFERER",
                    ""
                )

                # -------------------------------------------------
                # TRAFFIC SOURCE
                # -------------------------------------------------

                traffic_source = self.get_traffic_source(
                    request,
                    referrer
                )

                # -------------------------------------------------
                # DEVICE
                # -------------------------------------------------

                if "tablet" in user_agent_lower:
                    device_type = "Tablet"

                elif "mobile" in user_agent_lower:
                    device_type = "Mobile"

                else:
                    device_type = "Desktop"

                # -------------------------------------------------
                # BROWSER
                # -------------------------------------------------

                if "edg" in user_agent_lower:
                    browser = "Edge"

                elif "opr" in user_agent_lower or "opera" in user_agent_lower:
                    browser = "Opera"

                elif "chrome" in user_agent_lower:
                    browser = "Chrome"

                elif "firefox" in user_agent_lower:
                    browser = "Firefox"

                elif "safari" in user_agent_lower:
                    browser = "Safari"

                else:
                    browser = "Other"

                # -------------------------------------------------
                # OPERATING SYSTEM
                # -------------------------------------------------

                if "windows" in user_agent_lower:
                    operating_system = "Windows"

                elif "android" in user_agent_lower:
                    operating_system = "Android"

                elif "iphone" in user_agent_lower or "ipad" in user_agent_lower:
                    operating_system = "iOS"

                elif "mac os" in user_agent_lower:
                    operating_system = "macOS"

                elif "linux" in user_agent_lower:
                    operating_system = "Linux"

                else:
                    operating_system = "Other"

                # -------------------------------------------------
                # SAVE VISIT
                # -------------------------------------------------

                SiteVisit.objects.create(

                    session_key=request.session.session_key,

                    user=user,

                    path=path,

                    referrer=referrer,

                    traffic_source=traffic_source,

                    ip_address=ip_address,

                    user_agent=user_agent,

                    device_type=device_type,

                    browser=browser,

                    operating_system=operating_system,
                )

        return response

    # =============================================================
    # TRAFFIC SOURCE DETECTION
    # =============================================================

    def get_traffic_source(self, request, referrer):

        # -------------------------------------------------
        # 1. UTM SOURCE
        # -------------------------------------------------

        utm_source = request.GET.get(
            "utm_source",
            ""
        ).strip().lower()

        if utm_source:

            source_map = {

                "google": "Google",

                "facebook": "Facebook",
                "fb": "Facebook",

                "instagram": "Instagram",
                "ig": "Instagram",

                "whatsapp": "WhatsApp",
                "wa": "WhatsApp",

                "tiktok": "TikTok",

                "twitter": "X / Twitter",
                "x": "X / Twitter",

                "youtube": "YouTube",

                "linkedin": "LinkedIn",

                "telegram": "Telegram",
            }

            return source_map.get(
                utm_source,
                utm_source.title()
            )

        # -------------------------------------------------
        # 2. NO REFERRER = DIRECT
        # -------------------------------------------------

        if not referrer:
            return "Direct"

        # -------------------------------------------------
        # 3. GET REFERRER DOMAIN
        # -------------------------------------------------

        try:

            hostname = urlparse(
                referrer
            ).hostname or ""

            hostname = hostname.lower()

        except Exception:

            return "Other"

        # -------------------------------------------------
        # 4. SEARCH ENGINES
        # -------------------------------------------------

        search_engines = (
            "google.",
            "bing.",
            "yahoo.",
            "duckduckgo.",
            "baidu.",
            "yandex.",
        )

        if any(
            engine in hostname
            for engine in search_engines
        ):
            return "Google / Search"

        # -------------------------------------------------
        # 5. SOCIAL MEDIA
        # -------------------------------------------------

        if (
            "facebook.com" in hostname
            or "fb.com" in hostname
        ):
            return "Facebook"

        if "instagram.com" in hostname:
            return "Instagram"

        if "whatsapp.com" in hostname:
            return "WhatsApp"

        if "tiktok.com" in hostname:
            return "TikTok"

        if (
            hostname == "x.com"
            or hostname.endswith(".x.com")
            or "twitter.com" in hostname
        ):
            return "X / Twitter"

        if (
            "youtube.com" in hostname
            or "youtu.be" in hostname
        ):
            return "YouTube"

        if "linkedin.com" in hostname:
            return "LinkedIn"

        if (
            "t.me" in hostname
            or "telegram.me" in hostname
        ):
            return "Telegram"

        # -------------------------------------------------
        # 6. EVERYTHING ELSE = REFERRAL
        # -------------------------------------------------

        return "Referral"