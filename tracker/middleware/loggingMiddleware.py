import logging
import time

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        method = request.method
        path = request.get_full_path()

        user = "Anonymous"
        if hasattr(request, "user") and request.user.is_authenticated:
            user = str(request.user)

        # ✅ Only basic request log BEFORE view
        logger.info(f"[REQUEST] {method} {path} | User: {user}")

        try:
            response = self.get_response(request)
        except Exception as e:
            logger.error(f"[ERROR] {method} {path} | Error: {str(e)}", exc_info=True)
            raise

        # ✅ NOW it's safe to access request.data
        body = None
        if method in ["POST", "PUT", "PATCH"]:
            try:
                if hasattr(request, "data"):
                    body = dict(request.data)
                    body.pop("password", None)
            except Exception:
                body = "Unable to parse body"

        duration = time.time() - start_time

        logger.info(
            f"[RESPONSE] {method} {path} | Status: {response.status_code} | Time: {duration:.3f}s | Body: {body}"
        )

        return response