import logging
import time
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('main')


class LogMiddleware(MiddlewareMixin):
    start = None
    log_id = None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        self.start = time.time()
        self.log_id = str(int(self.start * 1000))
        req_data = request.POST
        url = request.build_absolute_uri(request.get_full_path())
        if 'admin' in url:
            return
        if not req_data:
            try:
                req_data = request.body.decode('utf-8')
            except Exception:
                pass
        logger.info(
            'ACCESS_LOG|START|%s|url=[%s], user=[%s], method=[%s], headers=[%s], query_params=[%s],'
            ' data=[%s]',
            self.log_id,
            request.build_absolute_uri(request.get_full_path()),
            request.user,
            request.method,
            request.headers,
            request.GET,
            req_data,
        )

    def process_response(self, request, response):
        if self.start:
            times = time.time() - self.start
        else:
            times = '统计失败'
        req_data = request.POST
        url = request.build_absolute_uri(request.get_full_path())
        if 'admin' in url:
            return response
        if not req_data:
            try:
                req_data = request.body.decode('utf-8')
            except Exception:
                pass
        logger.info(
            'ACCESS_LOG|END|%s|url=[%s], user=[%s], method=[%s], headers=[%s], query_params=[%s],'
            ' data=[%s], response_status=[%s], response_content=[%s], times=[%s]',
            self.log_id,
            request.build_absolute_uri(request.get_full_path()),
            request.user,
            request.method,
            request.headers,
            request.GET,
            req_data,
            response.status_code,
            getattr(response, 'data', None),
            times,
        )
        return response


class SkipCsrfCheckMiddleware(MiddlewareMixin):
    # 当来源在配置的列表中时，跳过 CSRF 检查
    def process_request(self, request):
        origin = request.META.get('HTTP_ORIGIN')
        # 读取设置中的可信来源列表
        trusted_origins = getattr(settings, 'CUSTOM_CSRF_TRUSTED_ORIGINS', [])

        # 检查请求的来源是否在可信列表中
        if origin:
            for trusted_origin in trusted_origins:
                if trusted_origin in origin:
                    setattr(request, '_dont_enforce_csrf_checks', True)
                    break
