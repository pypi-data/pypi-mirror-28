# coding:utf-8

import functools
import io
import os
import re
import sys
import time
from abc import abstractmethod

import easyutils
import pandas as pd

from . import exceptions
from . import helpers
from .config import client
from .log import log

if not sys.platform.startswith('darwin'):
    import pywinauto
    import pywinauto.clipboard


class ClientTrader:
    def __init__(self):
        self._config = client.create(self.broker_type)
        self._app = None
        self._main = None

    def prepare(self, config_path=None, user=None, password=None, exe_path=None, comm_password=None,
                **kwargs):
        """
        登陆客户端
        :param config_path: 登陆配置文件，跟参数登陆方式二选一
        :param user: 账号
        :param password: 明文密码
        :param exe_path: 客户端路径类似 r'C:\\htzqzyb2\\xiadan.exe', 默认 r'C:\\htzqzyb2\\xiadan.exe'
        :param comm_password: 通讯密码
        :return:
        """
        if config_path is not None:
            account = helpers.file2dict(config_path)
            user = account['user']
            password = account['password']
        self.login(user, password, exe_path or self._config.DEFAULT_EXE_PATH, comm_password, **kwargs)

    @abstractmethod
    def login(self, user, password, exe_path, comm_password=None, **kwargs):
        pass

    def connect(self, exe_path=None, **kwargs):
        """
        直接连接登陆后的客户端
        :param exe_path: 客户端路径类似 r'C:\\htzqzyb2\\xiadan.exe', 默认 r'C:\\htzqzyb2\\xiadan.exe'
        :return:
        """
        connect_path = exe_path or self._config.DEFAULT_EXE_PATH
        if connect_path is None:
            raise ValueError('参数 exe_path 未设置，请设置客户端对应的 exe 地址,类似 C:\\客户端安装目录\\xiadan.exe')

        self._app = pywinauto.Application().connect(path=connect_path,
                                                    timeout=10)
        self._close_prompt_windows()
        self._main = self._app.top_window()

    @property
    def broker_type(self):
        return 'ths'

    @property
    def balance(self):
        self._switch_left_menus(['查询[F4]', '资金股票'])

        return self._get_balance_from_statics()

    def _get_balance_from_statics(self):
        result = {}
        for key, control_id in self._config.BALANCE_CONTROL_ID_GROUP.items():
            result[key] = float(
                self._main.window(
                    control_id=control_id,
                    class_name='Static',
                ).window_text()
            )
        return result

    @property
    def position(self):
        self._switch_left_menus(['查询[F4]', '资金股票'])

        return self._get_grid_data(self._config.COMMON_GRID_CONTROL_ID)

    @property
    def today_entrusts(self):
        self._switch_left_menus(['查询[F4]', '当日委托'])

        return self._get_grid_data(self._config.COMMON_GRID_CONTROL_ID)

    @property
    def today_trades(self):
        self._switch_left_menus(['查询[F4]', '当日成交'])

        return self._get_grid_data(self._config.COMMON_GRID_CONTROL_ID)

    @property
    def cancel_entrusts(self):
        self._refresh()
        self._switch_left_menus(['撤单[F3]'])

        return self._get_grid_data(self._config.COMMON_GRID_CONTROL_ID)

    def cancel_entrust(self, entrust_no):
        self._refresh()
        for i, entrust in enumerate(self.cancel_entrusts):
            if entrust[self._config.CANCEL_ENTRUST_ENTRUST_FIELD] == entrust_no:
                self._cancel_entrust_by_double_click(i)
                return self._handle_cancel_entrust_pop_dialog()
        else:
            return {'message': '委托单状态错误不能撤单, 该委托单可能已经成交或者已撤'}

    def buy(self, security, price, amount, **kwargs):
        self._switch_left_menus(['买入[F1]'])

        return self.trade(security, price, amount)

    def sell(self, security, price, amount, **kwargs):
        self._switch_left_menus(['卖出[F2]'])

        return self.trade(security, price, amount)

    def market_buy(self, security, amount, ttype=None, **kwargs):
        """
        市价买入
        :param security: 六位证券代码
        :param amount: 交易数量
        :param ttype: 市价委托类型，默认客户端默认选择，
                     深市可选 ['对手方最优价格', '本方最优价格', '即时成交剩余撤销', '最优五档即时成交剩余 '全额成交或撤销']
                     沪市可选 ['最优五档成交剩余撤销', '最优五档成交剩余转限价']

        :return: {'entrust_no': '委托单号'}
        """
        self._switch_left_menus(['市价委托', '买入'])

        return self.market_trade(security, amount, ttype)

    def market_sell(self, security, amount, ttype=None, **kwargs):
        """
        市价卖出
        :param security: 六位证券代码
        :param amount: 交易数量
        :param ttype: 市价委托类型，默认客户端默认选择，
                     深市可选 ['对手方最优价格', '本方最优价格', '即时成交剩余撤销', '最优五档即时成交剩余 '全额成交或撤销']
                     沪市可选 ['最优五档成交剩余撤销', '最优五档成交剩余转限价']

        :return: {'entrust_no': '委托单号'}
        """
        self._switch_left_menus(['市价委托', '卖出'])

        return self.market_trade(security, amount, ttype)

    def market_trade(self, security, amount, ttype=None, **kwargs):
        """
        市价交易
        :param security: 六位证券代码
        :param amount: 交易数量
        :param ttype: 市价委托类型，默认客户端默认选择，
                     深市可选 ['对手方最优价格', '本方最优价格', '即时成交剩余撤销', '最优五档即时成交剩余 '全额成交或撤销']
                     沪市可选 ['最优五档成交剩余撤销', '最优五档成交剩余转限价']

        :return: {'entrust_no': '委托单号'}
        """
        self._set_market_trade_params(security, amount)
        if ttype is not None:
            self._set_market_trade_type(ttype)
        self._submit_trade()

        return self._handle_trade_pop_dialog()

    def _set_market_trade_type(self, ttype):
        """根据选择的市价交易类型选择对应的下拉选项"""
        selects = self._main(
            control_id=self._config.TRADE_MARKET_TYPE_CONTROL_ID,
            class_name='ComboBox'
        )
        for i, text in selects.texts():
            # skip 0 index, because 0 index is current select index
            if i == 0:
                continue
            if ttype in text:
                selects.select(i - 1)
                break
        else:
            raise TypeError('不支持对应的市价类型: {}'.format(ttype))

    def auto_ipo(self):
        self._switch_left_menus(self._config.AUTO_IPO_MENU_PATH)

        stock_list = self._get_grid_data(self._config.COMMON_GRID_CONTROL_ID)
        valid_list_idx = [i for i, v in enumerate(stock_list) if v['申购数量'] <= 0]
        self._click(self._config.AUTO_IPO_SELECT_ALL_BUTTON_CONTROL_ID)
        self._wait(0.1)

        for row in valid_list_idx:
            self._click_grid_by_row(row)
        self._wait(0.1)

        self._click(self._config.AUTO_IPO_BUTTON_CONTROL_ID)
        self._wait(0.1)

        return self._handle_auto_ipo_pop_dialog()

    def _click_grid_by_row(self, row):
        x = self._config.COMMON_GRID_LEFT_MARGIN
        y = self._config.COMMON_GRID_FIRST_ROW_HEIGHT + self._config.COMMON_GRID_ROW_HEIGHT * row
        self._app.top_window().window(
            control_id=self._config.COMMON_GRID_CONTROL_ID,
            class_name='CVirtualGridCtrl'
        ).click(coords=(x, y))

    def _handle_auto_ipo_pop_dialog(self):
        while self._main.wrapper_object() != self._app.top_window().wrapper_object():
            title = self._get_pop_dialog_title()
            if '提示信息' in title or '委托确认' in title or '网上交易用户协议' in title:
                self._app.top_window().type_keys('%Y')
            elif '提示' in title:
                data = self._app.top_window().Static.window_text()
                self._app.top_window()['确定'].click()
                return {'message': data}
            else:
                data = self._app.top_window().Static.window_text()
                self._app.top_window().close()
                return {'message': 'unkown message: {}'.find(data)}
            self._wait(0.1)
        return {'message': 'success'}

    def _run_exe_path(self, exe_path):
        return os.path.join(
            os.path.dirname(exe_path), 'xiadan.exe'
        )

    def _wait(self, seconds):
        time.sleep(seconds)

    def exit(self):
        self._app.kill()

    def _close_prompt_windows(self):
        self._wait(1)
        for w in self._app.windows(class_name='#32770'):
            if w.window_text() != self._config.TITLE:
                w.close()
        self._wait(1)

    def trade(self, security, price, amount):
        self._set_trade_params(security, price, amount)

        self._submit_trade()

        return self._handle_trade_pop_dialog()

    def _handle_trade_pop_dialog(self):
        self._wait(0.2)  # wait dialog display
        while self._main.wrapper_object() != self._app.top_window().wrapper_object():
            pop_title = self._get_pop_dialog_title()
            if pop_title == '委托确认':
                self._app.top_window().type_keys('%Y')
            elif pop_title == '提示信息':
                if '超出涨跌停' in self._app.top_window().Static.window_text():
                    self._app.top_window().type_keys('%Y')
            elif pop_title == '提示':
                content = self._app.top_window().Static.window_text()
                if '成功' in content:
                    entrust_no = self._extract_entrust_id(content)
                    self._app.top_window()['确定'].click()
                    return {'entrust_no': entrust_no}
                else:
                    self._app.top_window()['确定'].click()
                    self._wait(0.05)
                    raise exceptions.TradeError(content)
            else:
                self._app.top_window().close()
            self._wait(0.3)  # wait next dialog display

    def _click(self, control_id):
        self._app.top_window().window(
            control_id=control_id,
            class_name='Button'
        ).click()

    def _extract_entrust_id(self, content):
        return re.search(r'\d+', content).group()

    def _submit_trade(self):
        time.sleep(0.05)
        self._app.top_window().window(
            control_id=self._config.TRADE_SUBMIT_CONTROL_ID,
            class_name='Button'
        ).click()

    def _get_pop_dialog_title(self):
        return self._app.top_window().window(
            control_id=self._config.POP_DIALOD_TITLE_CONTROL_ID
        ).window_text()

    def _set_trade_params(self, security, price, amount):
        code = security[-6:]

        self._type_keys(
            self._config.TRADE_SECURITY_CONTROL_ID,
            code
        )

        # wait security input finish
        self._wait(0.1)

        self._type_keys(
            self._config.TRADE_PRICE_CONTROL_ID,
            easyutils.round_price_by_code(price, code)
        )
        self._type_keys(
            self._config.TRADE_AMOUNT_CONTROL_ID,
            str(int(amount))
        )

    def _set_market_trade_params(self, security, amount):
        code = security[-6:]

        self._type_keys(
            self._config.TRADE_SECURITY_CONTROL_ID,
            code
        )

        # wait security input finish
        self._wait(0.1)

        self._type_keys(
            self._config.TRADE_AMOUNT_CONTROL_ID,
            str(int(amount))
        )

    def _get_grid_data(self, control_id):
        grid = self._main.window(
            control_id=control_id,
            class_name='CVirtualGridCtrl'
        )
        grid.type_keys('^A^C')
        return self._format_grid_data(
            self._get_clipboard_data()
        )

    def _type_keys(self, control_id, text):
        self._main.window(
            control_id=control_id,
            class_name='Edit'
        ).type_keys(text)

    def _get_clipboard_data(self):
        while True:
            try:
                return pywinauto.clipboard.GetData()
            except Exception as e:
                log.warning('{}, retry ......'.format(e))

    def _switch_left_menus(self, path, sleep=0.2):
        self._get_left_menus_handle().get_item(path).click()
        self._wait(sleep)

    def _switch_left_menus_by_shortcut(self, shortcut, sleep=0.5):
        self._app.top_window().type_keys(shortcut)
        self._wait(sleep)

    @functools.lru_cache()
    def _get_left_menus_handle(self):
        while True:
            try:
                handle = self._main.window(
                    control_id=129,
                    class_name='SysTreeView32'
                )
                # sometime can't find handle ready, must retry
                handle.wait('ready', 2)
                return handle
            except:
                pass

    def _format_grid_data(self, data):
        df = pd.read_csv(io.StringIO(data),
                         delimiter='\t',
                         dtype=self._config.GRID_DTYPE,
                         na_filter=False,
                         )
        return df.to_dict('records')

    def _handle_cancel_entrust_pop_dialog(self):
        while self._main.wrapper_object() != self._app.top_window().wrapper_object():
            title = self._get_pop_dialog_title()
            if '提示信息' in title:
                self._app.top_window().type_keys('%Y')
            elif '提示' in title:
                data = self._app.top_window().Static.window_text()
                self._app.top_window()['确定'].click()
                return {'message': data}
            else:
                data = self._app.top_window().Static.window_text()
                self._app.top_window().close()
                return {'message': 'unkown message: {}'.find(data)}
            self._wait(0.2)

    def _cancel_entrust_by_double_click(self, row):
        x = self._config.CANCEL_ENTRUST_GRID_LEFT_MARGIN
        y = self._config.CANCEL_ENTRUST_GRID_FIRST_ROW_HEIGHT + self._config.CANCEL_ENTRUST_GRID_ROW_HEIGHT * row
        self._app.top_window().window(
            control_id=self._config.COMMON_GRID_CONTROL_ID,
            class_name='CVirtualGridCtrl'
        ).double_click(coords=(x, y))

    def _refresh(self):
        self._switch_left_menus(['买入[F1]'], sleep=0.05)
