# memect-http-error

## install

```
pip install memect-http-error
```

## usage


```
import tornado
import memect_http_error as http_error

class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish(http_error.unknown_error.to_string())
```
