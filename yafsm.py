#encoding=utf-8

version = 0.1

class StateException(Exception):

    def __init__(self, err, context):
        self.error = err
        self.context = context

class BaseStateMachine(object):
    """有限状态机
    子类须知：
    - 定义TRANSIT_MAP
    - 重写init_context函数作为状态机启动时的初始上下文。
    - 针对每个状态（除start外）编写shuld_enter, enter函数。
    - 两个结束状态不需显式定义(end, cancel)。

    enter函数；
    尝试进入新状态，返回新的状态名，及错误。

    execute函数：
    返回自定义数据。
    """
    TRANSIT_MAP = {'start': ('end', True)}

    @classmethod
    def process(cls, obj, state='start', context=None, **kwargs):
        """参数：
        - obj 业务参数对象
        - 当前的状态
        - 当前的上下文
        """
        return cls(obj, state, context, **kwargs).execute()

    def __init__(self, obj, state='start', context=None, **kwargs):
        self.obj = obj
        self.state = state
        self.error = None
        self.context = context or {}
        self.__dict__.update(kwargs)

    def init_context(self):
        return {}

    def validate_transit_map(self):
        pass

    def execute(self):
        assert self.TRANSIT_MAP, 'No TRANSIT_MAP define!'

        if not self.state:
            self.state = 'start'
            self.context = self.init_context()

        branches = self.TRANSIT_MAP.get(self.state, '')
        func = None
        for name, condition in branches:
            if self.should_transit(name, condition):
                func = 'enter_%s_from_%s' % (name, self.state)
                fo = getattr(self, func, None)
                if not fo:
                    func = 'enter_%s_state' % name
                    fo = getattr(self, func, None)
                if fo:
                    msg = fo()
                    return name, self.context, msg
                else:
                    raise StateException('not implement func : %s' % func)
        if not func:
            # 未能够进入下一状态，应该是出了错。
            if self.error:
                raise StateException(self.error, self.context)
            else:
                raise StateException('unknown state error', self.context)

    def should_transit(self, name, condition):
        if condition:
            collect_count = 0
            for k, v in condition.iteritems():
                if getattr(self.obj, k, '') == v or \
                        (self.context and self.context.get(k)):
                    collect_count += 1
            if collect_count == len(condition.keys()):
                return True
            return False
        else:
            # 检测有没有should_enter_xx_state_from_xxx方法
            func = 'should_enter_%s_from_%s' % (name, self.state)
            if getattr(self, func):
                return getattr(self, func)()
            else:
                return False

    def end(self):
        pass

    def cancel(self):
        pass

    def enter_end_state(self):
        return self.end()

    def enter_cancel_state(self):
        return self.cancel()
