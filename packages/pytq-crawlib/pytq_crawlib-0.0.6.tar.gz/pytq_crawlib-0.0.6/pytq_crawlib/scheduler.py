#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**中文文档**

此模块解决的什么问题？

在网页爬虫项目中，如果我们对数据质量要求很高，我们会希望每一个待爬的页面都被正确精准的爬过
至少一次。而在将来可能不定时的重新访问每个页面更新数据。

在抓取网页的过程中，有可能出现以下几种情况：

1. 网址出错，无法进行Http Request。
2. 服务器出错，暂时 / 永久 的无法访问。
3. 服务器拒绝访问，比如要求验证码等，反爬虫。
4. 从网页抓取数据失败了。
5. 网页的数据不完整。
...

等各种奇怪的情况，所以我们需要标记记录当前抓取的状态。

解决方案：

1. 使用MongoDB作为后端数据库。
2. 使用DiskCache作为成功抓取的Html的缓存。
3. 使用 ``crawlib.Status`` 对各种情况进行标注。
4. 使用 ``crawlib.exc`` 对各种错误进行捕捉。
"""

import six
import time
import attr
import diskcache
import mongoengine
from datetime import datetime, timedelta
from sfm.exception_mate import ErrorTraceBackChain
from attrs_mate import AttrsClass
from pytq import MongoDBStatusFlagScheduler
from crawlib import exc, Status, decoder, requests_spider, ChromeSpider


def format_exc():
    return ErrorTraceBackChain.get_last_exc_info().source_error.formatted


@attr.s
class InputData(AttrsClass):
    data = attr.ib()
    request_kwargs = attr.ib(default=attr.Factory(dict))
    get_html_kwargs = attr.ib(default=attr.Factory(dict))
    parse_html_kwargs = attr.ib(default=attr.Factory(dict))
    ignore_cache = attr.ib(default=False)
    update_cache = attr.ib(default=True)
    expire = attr.ib(default=None)


@attr.s
class OutputData(AttrsClass):
    url = attr.ib(default=None)
    html = attr.ib(default=None)
    data = attr.ib(default=None)
    status = attr.ib(default=Status.S0_ToDo.id)


class BaseScheduler(MongoDBStatusFlagScheduler):
    """

    - ``def build_url(self, doc, **kwargs)``
    - ``def request(self, url, **kwargs)``
    - ``def get_html(self, url, **kwargs)``
    - ``def parse_html(self, html, **kwargs)``
    """
    model_klass = None
    """
    ``mongoengine_mate.ExtendedDocument`` object, represent the data model
    you are crawling with.
    """

    duplicate_flag = Status.S50_Finished.id
    """
    A integer value represent its a duplicate item. Any value greater or equal 
    than this will be a duplicate item, otherwise its not.

    You could define that when you initiate the scheduler.
    """

    update_interval = 24 * 3600
    """
    If a item has been finished more than ``update_interval`` seconds, then
    it should be re-do, and it is NOT a duplicate item.

    You could define that when you initiate the scheduler.
    """

    cache = None
    """
    html disk cache, :class:`diskcache.Cache` object.
    """

    use_requests = True
    """
    bool. if true, use ``requests`` library for crawler.
    """

    chrome_drive_path = None
    """
    str. 
    
    if ``use_requests`` is False, then use selenium ChromeDriver for html
    retrieve, a chrome driver executable file has to be given.
    """

    html_encoding = None
    """
    site wide html charset. if None, then decoder will automatically detect it.
    """

    decode_error_handling = "strict"
    """
    parameters in ``bytes.decode(encoding, errors=decode_error_handling)``.
    """

    def __init__(self, logger=None):
        if self.duplicate_flag < 0:  # pragma: no cover
            raise ValueError
        if not isinstance(self.update_interval,
                          six.integer_types):  # pragma: no cover
            raise TypeError
        if (self.cache is None) or (
                not isinstance(self.cache,
                               diskcache.Cache)):  # pragma: no cover
            raise TypeError
        collection = self.model_klass._get_collection()
        super(MongoDBStatusFlagScheduler, self). \
            __init__(logger=logger, collection=collection)

        self.collection = collection
        self.col = self.collection

    def user_hash_input(self, input_data):
        """
        Get fingerprint of input_data.

        fingerprint of `mongoengine.Document` usually is the ``_id`` field.
        """
        doc = input_data.data
        return doc._id

    def build_url(self, doc, **kwargs):  # pragma: no cover
        """
        :return: url.
        """
        msg = ("You have to implement this method to create url using "
               "document data. Document data is an instance of "
               "mongoengine.Document, typically it should be uniquely "
               "associated with Document._id.")
        raise NotImplementedError(msg)

    def request(self, url, **kwargs):
        """
        :return: :class:`requests.Response`.
        """
        return requests_spider.get(url, **kwargs)

    def get_html(self, url, **kwargs):
        """
        :return: str, html.
        """
        raise self.selenium_spider.get_html(url)

    def parse_html(self, html, **kwargs):  # pragma: no cover
        """
        :return: :class:`crawlib.ParseResult`.

        **中文文档**

        实现这个方法的一些限制：

        1. 当从html中获得了你想要的信息，换言之该url已经抓取完成，不需要再抓取时，
        不会抛出任何异常，直接正常返回。
        2. 其中如果数据不够完整，但你觉得数据已经够用了，暂时你并不想再进行抓取，
        可能很久以后会再次访问url进行抓取时，需要赋值
        ``ParseResult(status=Status.S60_ServerSideError.id)``，然后正常返回。
        3. 如果服务器上该Url目前无法访问，换言之此时此刻无论访问url多少次都不会有数据，
        那么可以直接抛出 exc.ServerSideError的异常。Scheduler会将其标记，不对其进行抓取。
        但可能以后会对该类错误进行再次尝试。
        """
        msg = ("You have to implement this method to parse useful data "
               "from html. The returns has to be ``crawlib.ParseResult``, "
               "having two attributes, ``.kwargs`` and ``.data``. ")
        raise NotImplementedError(msg)

    def create_finished_filter(self):
        """
        A mongodb query for no-need-to-crawl documents.
        """
        now = datetime.utcnow()
        n_sec_ago = now - timedelta(seconds=self.update_interval)
        filters = {
            self.status_key: {"$gte": self.duplicate_flag},
            self.edit_at_key: {"$gte": n_sec_ago},
        }
        return filters

    def create_unfinished_filter(self):
        """
        A mongodb query for need-to-crawl documents.
        """
        now = datetime.utcnow()
        n_sec_ago = now - timedelta(seconds=self.update_interval)
        filters = {
            "$and": [
                {
                    "$or": [
                        {self.status_key: {"$lt": self.duplicate_flag}},
                        {self.edit_at_key: {"$lt": n_sec_ago}},
                    ]
                }
            ]
        }
        return filters

    def query(self, filters=None, order_by=None, only=None, limit=None):
        """
        Execute mongoengine style query.

        :param filters: mongodb query.
        :param order_by: list of str, example: ``["-date",]``.
        :param only: list of str, example: ``["title", "author.name"]``.
        :param limit: only returns first N documents.
        """
        if filters is None:
            filters = self.create_unfinished_filter()
        query_set = self.model_klass.by_filter(filters)

        if order_by is not None:
            query_set = query_set.order_by(*order_by)

        if only is not None:
            query_set = query_set.only(*only)

        if limit is 0:
            limit = None

        return query_set.limit(limit)

    def get_input_data_queue(self,
                             filters=None,
                             order_by=None,
                             only=None,
                             limit=None,
                             request_kwargs=None,
                             get_html_kwargs=None,
                             parse_html_kwargs=None,
                             ignore_cache=False,
                             update_cache=True,
                             expire=None):
        """
        Get unfinished input data queue.

        :param filters: mongodb query.
        :param order_by: list of str, example: ``["-date",]``.
        :param only: list of str, example: ``["title", "author.name"]``.
        :param limit: only returns first N documents.
        :param request_kwargs: optional parameters will be used in
            ``request(url, **request_kwargs)``.
        :param get_html_kwargs: optional
        :param parse_html_kwargs: optional
        :param ignore_cache: if True, then make http requests anyway.
        :param update_cache: if False, then will not update cache when success.
        :param expire: cache expire time in seconds.
        """

        if request_kwargs is None:
            request_kwargs = {}
        if get_html_kwargs is None:
            get_html_kwargs = {}
        if parse_html_kwargs is None:
            parse_html_kwargs = {}
        if expire is None:
            expire = self.update_interval

        input_data_queue = list()
        for model_data in self.query(
                filters=filters, order_by=order_by, only=only, limit=limit):
            input_data = InputData(
                data=model_data,
                request_kwargs=request_kwargs,
                get_html_kwargs=get_html_kwargs,
                parse_html_kwargs=parse_html_kwargs,
                ignore_cache=ignore_cache,
                update_cache=update_cache,
                expire=expire,
            )
            input_data_queue.append(input_data)
        return input_data_queue

    # --- Response OK / Restrict Access / 404 checker ---
    def is_status_ok(self, response, out, html):
        """
        Test if response is OK.
        """
        if 200 <= response.status_code < 300:
            return True

    def is_restrict_access(self, response, out, html):
        """
        Test if been banned, or encounter captcha.
        """
        if response.status_code == 403:
            msg = ("You reach the limit, "
                   "program will sleep for 1 hours, "
                   "please wait for a day to continue...")
            self.info(msg, 1)
            out.status = Status.S20_WrongPage.id
            time.sleep(24 * 3600)
            return True

    def is_404_error(self, response, out, html):
        """
        Test if it is 404 page.
        """
        if response.status_code == 404:  # page not exists
            msg = "page doesn't exists on server!"
            self.info(msg, 1)
            out.status = Status.S60_ServerSideError.id
            return True

    def identify_should_proceed(self, response, out, **kwargs):
        """
        Response OK / Restrict Access / 404 checker, decide if we should
        proceed to call `parse_html(html)` function.
        """
        # Get html in string first
        try:
            html = decoder.decode(
                binary=response.content,
                url=response.url,
                encoding=self.html_encoding,
                errors=self.decode_error_handling,
            )
            out.html = html
        except:
            out.html = None

        if self.is_404_error(response, out, out.html):
            return False
        elif self.is_restrict_access(response, out, out.html):
            return False
        elif self.is_status_ok(response, out, out.html):
            return True
        else:
            msg = ("Unknown page status!")
            self.info(msg, 1)
            out.status = Status.S10_HttpError
            return False

    def user_process(self, input_data):
        out = OutputData()
        doc = input_data.data
        url = self.build_url(doc)
        out.url = url

        self.info("Crawl %s ..." % url, 1)

        flag_do_request = True
        if input_data.ignore_cache is False:
            if url in self.cache:
                flag_do_request = False
                html = self.cache[url]

        if flag_do_request:
            self.info("Making real requests!", 1)
            if self.use_requests:
                try:
                    response = self.request(url, **input_data.request_kwargs)
                except:
                    msg = "Failed to make http request: %s" % format_exc()
                    self.info(msg, 1)
                    out.status = Status.S10_HttpError.id
                    return out

                # if it is not OK, we should not proceed
                # we should just record status and return
                continue_flag = self.identify_should_proceed(response, out)
                if continue_flag is False:
                    return out
            else:
                try:
                    html = self.chrome_spider.get_html(
                        url, **input_data.get_html_kwargs)
                    out.html = html
                except:
                    msg = "Failed to make http request: %s" % format_exc()
                    self.info(msg, 1)
                    out.status = Status.S10_HttpError.id
                    return out

        try:
            parse_result = self.parse_html(out.html,
                                           **input_data.parse_html_kwargs)
            out.data = parse_result
            msg = "Successfully extracted data!"
            self.info(msg, 1)
            if parse_result.status == Status.S60_ServerSideError:
                out.status = Status.S60_ServerSideError
            else:
                out.status = Status.S50_Finished.id
        except exc.ServerSideError:
            out.html = html
            msg = "Server side error!" % format_exc()
            self.info(msg, 1)
            out.status = Status.S60_ServerSideError.id
        except:
            msg = "Failed to parse html: %s" % format_exc()
            self.info(msg, 1)
            out.status = Status.S30_ParseError.id
        return out

    def to_dict_only_not_none_field(self, model_data):
        """
        Transform mongoengine.Document to dictionary, ignore None value fields.

        :param model_data: `mongoengine.Document` object.
        :return: dict.
        """
        d = model_data.to_dict()
        d.pop("_id")
        d.pop(self.status_key)
        d.pop(self.edit_at_key)

        true_false = [True, False]
        for key, value in d.items():
            if (value not in true_false) and (bool(value) is False):
                d.pop(key)
        return d

    def do(self,
           input_data_queue,
           pre_process=None,
           multiprocess=False,
           processes=None,
           ignore_error=True):
        if self.use_requests is False:
            with ChromeSpider(self.chrome_drive_path) as chrome_spider:
                self.chrome_spider = chrome_spider
                super(BaseScheduler, self).do(
                    input_data_queue=input_data_queue,
                    pre_process=pre_process,
                    multiprocess=False,
                    processes=None,
                    ignore_error=ignore_error,
                )
        else:
            super(BaseScheduler, self).do(
                input_data_queue=input_data_queue,
                pre_process=pre_process,
                multiprocess=multiprocess,
                processes=processes,
                ignore_error=ignore_error,
            )


class OneToMany(BaseScheduler):
    """
    For example, there's a USA, state, city, zipcode website. On state info
    webpage, it has state info and list of city. In this case, we need to visit
    52 state and get all cities. The State is the parent `model_klass`, and the
    `City` is the `child_klass`. They are One - to - Many relationship.

    :param model_klass: mongoengine.Document (Required)
        ``mongoengine_mate.ExtendedDocument`` object, represent the data model
        you are crawling with.

    :param duplicate_flag: int (Optional)
        A integer value represent its a duplicate item. Any value greater or equal
        than this will be a duplicate item, otherwise its not.
        You could define that when you initiate the scheduler.

    :param update_interval: int (Optional)
        If a item has been finished more than ``update_interval`` seconds, then
        it should be re-do, and it is NOT a duplicate item.
        You could define that when you initiate the scheduler.

    :param cache: `discache.Cache` (Required)
        html disk cache, :class:`diskcache.Cache` object.

    :param use_requests: bool. default True (Optional)
        if true, use ``requests`` library for crawler.

    :param chrome_drive_path: str, default None (Optional)
        if ``use_requests`` is False, then use selenium ChromeDriver for html
        retrieve, a chrome driver executable file has to be given.

    :param html_encoding: str, default None (Optional)
        site wide html charset. if None, then decoder will automatically detect it.

    :param decode_error_handling: str, default "strict" (Optional)
        parameters in ``bytes.decode(encoding, errors=decode_error_handling)``.

    :param child_klass: str, default None (Required)
        Child model class is the data model associated with the parent model.

        For example: a USA state information webpage could have list of city.
        in this case, State is `model_klass`, City is `child_class`.

    :param n_child_key: str, default None (Required)
        A field name to store how many child exists in this page.
    """
    child_klass = None
    """
    Child model class is the data model associated with the parent model.
    
    For example: a USA state information webpage could have list of city. 
    in this case, State is `model_klass`, City is `child_class`.
    """

    n_child_key = None
    """
    A field name to store how many child exists in this page.
    """

    def __init__(self, logger=None):
        super(OneToMany, self).__init__(logger=logger)

        if self.child_klass is None:
            raise NotImplementedError

        if not isinstance(self.n_child_key, six.string_types):
            raise TypeError
        n_child_field = getattr(self.model_klass, self.n_child_key)
        if not isinstance(n_child_field, mongoengine.IntField):
            raise TypeError

    def user_post_process(self, task):
        input_data = task.input_data
        output_data = task.output_data

        upd = {
            self.status_key: output_data.status,
            self.edit_at_key: datetime.utcnow(),
        }
        if output_data.status >= self.duplicate_flag:
            if input_data.update_cache:
                self.cache.set(
                    output_data.url, output_data.html,
                    expire=input_data.expire,
                )
            if output_data.data:
                parse_result = output_data.data
                n_child = len(parse_result.data)
                upd[self.n_child_key] = n_child
                if n_child:
                    self.child_klass.smart_insert(parse_result.data)

        self.col.update({"_id": task.id}, {"$set": upd})


class OneToOne(BaseScheduler):
    """
    :param model_klass: mongoengine.Document (Required)
        ``mongoengine_mate.ExtendedDocument`` object, represent the data model
        you are crawling with.

    :param duplicate_flag: int (Optional)
        A integer value represent its a duplicate item. Any value greater or equal
        than this will be a duplicate item, otherwise its not.
        You could define that when you initiate the scheduler.

    :param update_interval: int (Optional)
        If a item has been finished more than ``update_interval`` seconds, then
        it should be re-do, and it is NOT a duplicate item.
        You could define that when you initiate the scheduler.

    :param cache: `discache.Cache` (Required)
        html disk cache, :class:`diskcache.Cache` object.

    :param use_requests: bool. default True (Optional)
        if true, use ``requests`` library for crawler.

    :param chrome_drive_path: str, default None (Optional)
        if ``use_requests`` is False, then use selenium ChromeDriver for html
        retrieve, a chrome driver executable file has to be given.

    :param html_encoding: str, default None (Optional)
        site wide html charset. if None, then decoder will automatically detect it.

    :param decode_error_handling: str, default "strict" (Optional)
        parameters in ``bytes.decode(encoding, errors=decode_error_handling)``.
    """

    def user_post_process(self, task):
        input_data = task.input_data
        output_data = task.output_data

        upd = {
            self.status_key: output_data.status,
            self.edit_at_key: datetime.utcnow(),
        }
        if output_data.status >= self.duplicate_flag:
            if input_data.update_cache:
                self.cache.set(
                    output_data.url, output_data.html,
                    expire=input_data.expire,
                )

            if output_data.data:
                parse_result = output_data.data
                if parse_result.data:
                    model_data = parse_result.data
                    upd.update(self.to_dict_only_not_none_field(model_data))

        self.col.update({"_id": task.id}, {"$set": upd})
