**crawl_requests**
==================
*1. Feactures:*
---------------
- *crawl_requests(like requests) can update ua and proxy automatically.*

*2. Usage:*
-----------
>>>from crawl_requests import req_default

>>>req = req_default.Req()

>>>req.keep_req(method='get',url='https://www.python.org')

<Response [200]>

*3. Tips:*
----------
- *pip install crawl_requests*
- *req_default updates ua and proxy automatically.*
- *req need about [account of loading proxies]% minutes to load and test proxy to be used.*
