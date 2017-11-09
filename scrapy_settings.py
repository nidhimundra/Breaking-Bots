CUSTOM_SETTINGS = {
    "RETRY_TIMES" : 10,
    "RETRY_HTTP_CODES" : [500, 503, 504, 400, 403, 404, 408],
    "DOWNLOADER_MIDDLEWARES" : {
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
        'scrapy_proxies.RandomProxy': 100,
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    },
    "PROXY_LIST" : '/path/to/proxy/list.txt',
    "PROXY_MODE" : 0

}