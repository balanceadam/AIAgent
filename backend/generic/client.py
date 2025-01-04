import datetime
import logging
from requests.exceptions import HTTPError
from requests.sessions import Session
import time

from generic.models import RequestLog, RequestLogDetail

logger = logging.getLogger('main')


class BaseClient:
    service = ''
    proxies = None
    host = ''
    default_timeout = 10
    session = Session()

    def request(self, method, uri, *args, **kwargs):
        return self._request(method, uri, True, *args, **kwargs)

    def request_with_save_log(self, trade_id, method, uri, *args, **kwargs):
        request_at = datetime.datetime.now()
        req_data = 'url=%s\n method=%s\n args=%s\n kwargs=%s' % (self.host + uri, method, args, kwargs)
        # log = RequestLog(service=self.service, url=self.host + uri, trade_id=trade_id, request=req_data, request_at=datetime.datetime.now())
        try:
            res = self._request(method, uri, True, *args, **kwargs)
        except Exception as e:
            # log.response = 'err: %s' % e
            # log.response_at = datetime.datetime.now()
            # log.save()
            request_log = RequestLog.objects.create(
                service=self.service, url=self.host + uri, trade_id=trade_id, request_at=request_at,
                response_at=datetime.datetime.now()
            )
            RequestLogDetail.objects.create(log=request_log, request=req_data, response='err: %s' % e)
            raise e
        # log.response = 'headers: %s\n data: %s' % (res.headers, res.text)
        # log.response_at = datetime.datetime.now()
        # log.save()
        return res

    def request_without_log_body(self, method, uri, *args, **kwargs):
        return self._request(method, uri, False, *args, **kwargs)

    def _request(self, method, uri, log_body, *args, **kwargs):
        start = time.time()
        log_id = str(int(start * 1000))

        if method == "post" and "data" not in kwargs:
            kwargs['data'] = args[0] if args else {}

        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.default_timeout

        headers = kwargs.pop('headers', {})
        kwargs['headers'] = headers

        if 'raise_for_status' in kwargs:
            raise_for_status = kwargs.pop('raise_for_status')
        else:
            raise_for_status = True

        # if log_body:
        #     logger.info('http_request|%s|%s|url=%s, args=%s, kwargs=%s', self.service, log_id, self.host + uri, args, kwargs)
        # else:
        #     logger.info('http_request|%s|%s|url=%s', self.service, log_id, self.host + uri)

        try:
            resp = self.session.request(method, self.host + uri, proxies=self.proxies, *args, **kwargs)
        except Exception as e:
            if log_body:
                logger.error(
                    'http_response|%s|%s|url=%s, args=%s, kwargs=%s, err=%s', self.service, log_id, self.host + uri, args, kwargs, e
                )
            else:
                logger.error(
                    'http_response|%s|%s|url=%s, response=%s', self.service, log_id, self.host + uri, e
                )
            raise e
        end = time.time()

        if raise_for_status:
            try:
                resp.raise_for_status()
            except HTTPError as e:
                if log_body:
                    logger.error(
                        'http_response|%s|%s|url=%s, args=%s, kwargs=%s, response=%s, times=%s', self.service, log_id, self.host + uri, args, kwargs, resp.text, end-start
                    )
                else:
                    logger.error(
                        'http_response|%s|%s|url=%s, response=%s, times=%s', self.service, log_id, self.host + uri, resp.text, end-start
                    )
                raise e

        if log_body:
            logger.info('http_response|%s|%s|url=%s, args=%s, kwargs=%s, response=%s, times=%s', self.service, log_id, self.host + uri, args, kwargs, resp.text, end-start)
        else:
            logger.info('http_response|%s|%s|url=%s, response=%s, times=%s', self.service, log_id, self.host + uri, resp.text, end-start)

        return resp
