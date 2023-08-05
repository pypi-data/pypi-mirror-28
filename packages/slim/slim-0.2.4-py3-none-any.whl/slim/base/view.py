import asyncio
import logging
import time
from abc import abstractmethod
from types import FunctionType
from typing import Tuple, Union, Dict, Iterable, Type, List, Set
from aiohttp import web

from slim.base.query import ParamsQueryInfo
from .app import Application
from .helper import create_signed_value, decode_signed_value
from .permission import Permissions, Ability, BaseUser, A
from .sqlfuncs import AbstractSQLFunctions
from ..retcode import RETCODE
from ..utils import MetaClassForInit
from ..exception import ValueHandleException

logger = logging.getLogger(__name__)


class BaseView(metaclass=MetaClassForInit):
    """
    应在 cls_init 时完成全部接口的扫描与wrap函数创建
    并在wrapper函数中进行实例化，传入 request 对象
    """
    _interface = {}
    # permission: Permissions  # 3.6

    @classmethod
    def use(cls, name, method: [str, Set, List], url=None):
        """ interface helper function"""
        if not isinstance(method, (str, list, set, tuple)):
            raise BaseException('Invalid type of method: %s' % type(method).__name__)

        if isinstance(method, str):
            method = {method}

        # TODO: check methods available
        cls._interface[name] = [{'method': method, 'url': url}]

    @classmethod
    def use_lst(cls, name):
        cls._interface[name] = [
            {'method': {'GET'}, 'url': '%s/{page}' % name},
            {'method': {'GET'}, 'url': '%s/{page}/{size}' % name},
        ]

    @classmethod
    def discard(cls, name):
        """ interface helper function"""
        cls._interface.pop(name, None)

    @classmethod
    def interface(cls):
        cls.use('get', 'GET')
        cls.use_lst('list')
        cls.use('set', 'POST')
        cls.use('new', 'POST')
        cls.use('delete', 'POST')

    @classmethod
    def permission_init(cls):
        """ Override it """
        cls.permission.add(Ability(None, {'*': '*'}))

    @classmethod
    def cls_init(cls):
        cls._interface = {}
        cls.interface()
        for k, v in vars(cls).items():
            if isinstance(v, FunctionType):
                if getattr(v, '_interface', None):
                    cls.use(k, *v._interface)
        if getattr(cls, 'permission', None):
            cls.permission = cls.permission.copy()
        else:
            cls.permission = Permissions()
        cls.permission_init()

    def __init__(self, app: Application, aiohttp_request: web.web_request.Request):
        self.app = app
        self._request = aiohttp_request

        self.ret_val = None
        self.response = None
        self.session = None
        self._cookie_set = None
        self._params_cache = None
        self._post_data_cache = None
        self._post_json_cache = None
        self._current_user = None

    @property
    def is_finished(self):
        return self.response

    async def _prepare(self):
        session_cls = self.app.options.session_cls
        self.session = await session_cls.get_session(self)

    async def prepare(self):
        pass

    @property
    def current_user(self) -> BaseUser:
        if not self._current_user:
            self._current_user = self.get_current_user()
        return self._current_user

    @property
    def current_user_roles(self):
        u = self.current_user
        if u is None:
            return {None}
        return u.roles

    def get_current_user(self):
        """Override to determine the current user from, e.g., a cookie.
        """
        return None

    def finish(self, code, data=NotImplemented):
        if data is NotImplemented:
            data = RETCODE.txt_cn.get(code)
        self.ret_val = {'code': code, 'data': data}  # for access in inhreads method
        self.response = web.json_response(self.ret_val)
        logger.debug('finish: %s' % self.ret_val)
        for i in self._cookie_set or ():
            if i[0] == 'set':
                self.response.set_cookie(i[1], i[2], **i[3])
            else:
                self.response.del_cookie(i[1])

    def del_cookie(self, key):
        if self._cookie_set is None:
            self._cookie_set = []
        self._cookie_set.append(('del', key))

    def params(self) -> dict:
        if self._params_cache is None:
            self._params_cache = dict(self._request.query)
        return self._params_cache

    async def _post_json(self) -> dict:
        # post body: raw(text) json
        if self._post_json_cache is None:
            self._post_json_cache = dict(await self._request.json())
        return self._post_json_cache

    async def post_data(self) -> dict:
        # post body: form data
        if self._post_data_cache is None:
            self._post_data_cache = dict(await self._request.post())
            logger.debug('raw post data: %s', self._post_data_cache)
        return self._post_data_cache

    def set_cookie(self, key, value, *, path='/', expires=None, domain=None, max_age=None, secure=None,
                   httponly=None, version=None):
        if self._cookie_set is None:
            self._cookie_set = []
        kwargs = {'path': path, 'expires': expires, 'domain': domain, 'max_age': max_age, 'secure': secure,
                  'httponly': httponly, 'version': version}
        self._cookie_set.append(('set', key, value, kwargs))

    def get_cookie(self, name, default=None):
        if self._request.cookies is not None and name in self._request.cookies:
            return self._request.cookies.get(name)
        return default

    def set_secure_cookie(self, name, value: bytes, *, max_age=30):
        #  一般来说是 UTC
        # https://stackoverflow.com/questions/16554887/does-pythons-time-time-return-a-timestamp-in-utc
        timestamp = int(time.time())
        # version, utctime, name, value
        # assert isinatance(value, (str, list, tuple, bytes, int))
        to_sign = [1, timestamp, name, value]
        secret = self.app.options.cookies_secret
        self.set_cookie(name, create_signed_value(secret, to_sign), max_age=max_age)

    def get_secure_cookie(self, name, default=None, max_age_days=31):
        secret = self.app.options.cookies_secret
        value = self.get_cookie(name)
        if value:
            data = decode_signed_value(secret, value)
            # TODO: max_age_days 过期计算
            if data and data[2] == name:
                return data[3]
        return default


class ViewOptions:
    def __init__(self, *, list_page_size=20, list_accept_size_from_client=False, permission: Permissions=None):
        self.list_page_size = list_page_size
        self.list_accept_size_from_client = list_accept_size_from_client
        self.permission = permission

    def assign(self, obj: Type['AbstractSQLView']):
        obj.LIST_PAGE_SIZE = self.list_page_size
        obj.LIST_ACCEPT_SIZE_FROM_CLIENT = self.list_accept_size_from_client
        if self.permission:
            obj.permission = self.permission


# noinspection PyMethodMayBeStatic
class AbstractSQLView(BaseView):
    _sql_cls = AbstractSQLFunctions
    options_cls = ViewOptions
    LIST_PAGE_SIZE = 20  # list 单次取出的默认大小
    LIST_ACCEPT_SIZE_FROM_CLIENT = False

    fields = {} # :[str, object], key is column, value can be everything
    foreign_keys = {} # :[str, str], key is column, value is table name
    table_name = ''

    @classmethod
    def add_soft_foreign_key(cls, column, table):
        """
        the column stores foreign table's primary key but isn't a foreign key (to avoid constraint)
        warning: if the table not exists, will crash when query with loadfk
        :param column: table's column
        :param table: foreign table name
        :return: True, None
        """
        if column in cls.fields:
            cls.foreign_keys[column] = table
            return True

    @classmethod
    def _check_view_options(cls):
        options = getattr(cls, 'options', None)
        if options and isinstance(options, ViewOptions):
            options.assign(cls)

    @classmethod
    def cls_init(cls, check_options=True):
        if check_options:
            cls._check_view_options()

        # because of BaseView.cls_init is a bound method (@classmethod)
        # so we can only route BaseView._interface, not cls._interface defined by user
        BaseView.cls_init.__func__(cls)
        # super().cls_init()  # fixed in 3.6

        async def func():
            await cls._fetch_fields(cls)
            cls._sql = cls._sql_cls(cls)

        asyncio.get_event_loop().run_until_complete(func())

    def load_role(self, role_val):
        role = int(role_val) if role_val and role_val.isdigit() else role_val
        self.ability = self.permission.request_role(self.current_user, role)
        return self.ability

    async def _prepare(self):
        await super()._prepare()
        value = self._request.headers.get('Role')
        if not self.load_role(value):
            self.finish(RETCODE.INVALID_ROLE)

    async def load_fk(self, info, items):
        """
        :param info:
        :param items: the data got from database and filtered from permission
        :return:
        """
        if not items: return
        # first: get tables' instances
        table_map = {}
        for column in info['loadfk'].keys():
            tbl_name = self.foreign_keys[column]
            table_map[column] = self.app.tables[tbl_name]

        # second: get query parameters
        for column, role in info['loadfk'].items():
            pks = []
            for i in items:
                pks.append(i.get(column, NotImplemented))

            # third: query foreign keys
            vcls = table_map[column]
            ability = vcls.permission.request_role(self.current_user, role)
            info2 = ParamsQueryInfo(vcls)

            info2.add_condition(info.PRIMARY_KEY, 'in', pks)
            info2.set_select(None)
            info2.check_permission(ability)

            code, data = await vcls._sql.select_paginated_list(info2, -1, 1)
            pk_values = vcls._sql.convert_list_result(info2['format'], data)

            # TODO: 别忘了！这里还少一个对结果的权限检查！

            pk_dict = {}
            for i in pk_values:
                pk_dict[i[vcls.primary_key]] = i

            for _, item in enumerate(items):
                k = item.get(column, NotImplemented)
                if k in pk_dict:
                    item[column] = pk_dict[k]

        return items

    def _filter_record_by_ability(self, record) -> Union[Dict, None]:
        available_columns = self.ability.filter_record(self.current_user, A.READ, record)
        if not available_columns: return
        return record.to_dict(available_columns)

    def _check_handle_result(self, ret):
        """ check result of handle_query/read/insert/update """
        if ret is None:
            return

        if isinstance(ret, Iterable):
            return self.finish(*ret)

        raise ValueHandleException('Invalid result type of handle function.')

    async def get(self):
        info = ParamsQueryInfo.new(self, self.params(), self.ability)
        self._check_handle_result(self.handle_query(info))
        if self.is_finished: return
        code, data = await self._sql.select_one(info)

        if code == RETCODE.SUCCESS:
            data = self._filter_record_by_ability(data)
            if not data: return self.finish(RETCODE.NOT_FOUND)
            self._check_handle_result(self.handle_read(data))
            if self.is_finished: return

        self.finish(code, data)

    def _get_list_page_and_size(self) -> Tuple[Union[int, None], Union[int, None]]:
        page = self._request.match_info.get('page', '1')

        if not page.isdigit():
            self.finish(RETCODE.INVALID_HTTP_PARAMS)
            return None, None
        page = int(page)

        size = self._request.match_info.get('size', None)
        if self.LIST_ACCEPT_SIZE_FROM_CLIENT:
            if size:
                if size == '-1':  # size is infinite
                    size = -1
                elif size.isdigit():
                    size = int(size or self.LIST_PAGE_SIZE)
                else:
                    self.finish(RETCODE.INVALID_HTTP_PARAMS)
                    return None, None
            else:
                size = self.LIST_PAGE_SIZE
        else:
            size = self.LIST_PAGE_SIZE

        return page, size

    async def _convert_list_result(self, info, data):
        lst = []
        get_values = lambda x: list(x.values())
        for i in data['items']:
            item = self._filter_record_by_ability(i)
            if not data: return self.finish(RETCODE.NOT_FOUND)

            if info['format'] == 'array':
                item = get_values(item)

            self._check_handle_result(self.handle_read(data))
            if self.is_finished: return
            lst.append(item)
        return lst

    async def list(self):
        page, size = self._get_list_page_and_size()
        if self.is_finished: return
        info = ParamsQueryInfo.new(self, self.params(), self.ability)
        self._check_handle_result(self.handle_query(info))
        if self.is_finished: return

        code, data = await self._sql.select_paginated_list(info, size, page)

        if code == RETCODE.SUCCESS:
            lst = await self._convert_list_result(info, data)
            data['items'] = await self.load_fk(info, lst)
            self.finish(RETCODE.SUCCESS, data)
        else:
            self.finish(code, data)

    def _data_convert(self, data: Dict[str, object], action=A.WRITE):
        # 写入/插入权限检查
        columns = []
        for k, v in data.items():
            columns.append((self.table_name, k))

        if len(columns) == 0:
            return self.finish(RETCODE.INVALID_HTTP_POSTDATA)

        if all(self.ability.cannot(self.current_user, action, *columns)):
            return self.finish(RETCODE.PERMISSION_DENIED)

        return data

    async def set(self):
        info = ParamsQueryInfo.new(self, self.params(), self.ability)
        self._check_handle_result(self.handle_query(info))
        if self.is_finished: return

        post_data = self._data_convert(await self.post_data())
        if self.is_finished: return
        self._check_handle_result(self.handle_update(post_data))
        if self.is_finished: return

        logger.debug('data: %s' % post_data)
        code, data = await self._sql.update(info, post_data)
        self.finish(code, data)

    async def new(self):
        post_data = self._data_convert(await self.post_data(), action=A.CREATE)
        logger.debug('data: %s' % post_data)
        if self.is_finished: return
        self._check_handle_result(self.handle_insert(post_data))
        if self.is_finished: return

        code, data = await self._sql.insert(post_data)
        if code == RETCODE.SUCCESS:
            data = self._filter_record_by_ability(data)
            if not data: return self.finish(RETCODE.NOT_FOUND)

            self._check_handle_result(self.handle_read(data))
            if self.is_finished: return
        self.finish(code, data)

    @staticmethod
    @abstractmethod
    async def _fetch_fields(cls_or_self):
        """
        4 values must be set up in this function:
        1. cls_or_self.table_name: str
        2. cls_or_self.fields: Dict['column', Any]
        3. cls_or_self.primary_key: str
        4. cls_or_self.foreign_keys: Dict['column', 'foreign table name']

        :param cls_or_self:
        :return:
        """
        pass

    def handle_query(self, info: ParamsQueryInfo) -> Union[None, tuple]:
        pass

    def handle_read(self, values: Dict) -> Union[None, tuple]:
        pass

    def handle_insert(self, values: Dict) -> Union[None, tuple]:
        pass

    def handle_update(self, values: Dict) -> Union[None, tuple]:
        pass
