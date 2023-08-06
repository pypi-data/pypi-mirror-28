#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2018/1/17
 """
from __future__ import unicode_literals, absolute_import


class RuleExecutor(object):
    """
    规则执行器
    """
    def __init__(self, rule_loader_cls, rule_context_maker_cls, performer_cls, logger, *args, **kwargs):
        self.rule_loader_cls = rule_loader_cls
        self.rule_loader = None
        self.rule_context_maker_cls = rule_context_maker_cls
        self.rule_context_maker = None
        self.performer_cls = performer_cls
        self.performer = None
        self.logger = logger
        self.args = args
        self.kwargs = kwargs

    def execute(self, event):
        """
        执行规则
        :param event: 规则的执行由事件触发
        :return:
        """
        self.logger.info('execute rules from event {}'.format(event))
        rules = self.load_rules(event)
        contexts = self.make_context(rules, event)
        valid_ctxs = self.validate(contexts)
        results = self.perform(valid_ctxs)
        return results

    def load_rules(self, event, *args, **kwargs):
        self.rule_loader = self.rule_loader_cls(self, event)
        return self.rule_loader.load(*args, **kwargs)

    def make_context(self, rules, event, *args, **kwargs):
        self.rule_context_maker = self.rule_context_maker_cls(self, rules, event)
        return self.rule_context_maker.make(*args, **kwargs)

    def validate(self, contexts, *args, **kwargs):
        ctxs = []
        for c in contexts:
            try:
                if c.is_valid(*args, **kwargs):
                    ctxs.append(c)
            except Exception as e:
                self.logger.exception(e.message)
        return ctxs

    def perform(self, contexts, *args, **kwargs):
        self.performer = self.performer_cls(self, contexts)
        return self.performer.perform(*args, **kwargs)


class Rule(object):
    """
    规则
    """
    def __init__(self, conditions):
        self.conditions = conditions
        self.satisfy_condition = None

    def meet_condition(self, context):
        """
        过滤满足的条件，返回满足的条件
        :param context:
        :return:
        """
        self.satisfy_condition = None
        return False


class RuleLoader(object):
    """
    规则加载器
    """
    def __init__(self, executor, event):
        self.executor = executor
        self.event = event
        self.rule_objs = []

    def load(self, *args, **kwargs):
        self.rule_objs = self.load_rules(*args, **kwargs)
        return self.filter(*args, **kwargs)

    def load_rules(self, *args, **kwargs):
        return []

    def filter(self, *args, **kwargs):
        return self.rule_objs


class RuleContextMaker(object):
    """
    规则上下文创建器
    """
    def __init__(self, executor, rules, event):
        self.executor = executor
        self.rules = rules
        self.event = event

    def make(self, *args, **kwargs):
        pass


class RuleContext(object):
    """
    规则上下文，负责与event的匹配，加载规则所需的数据
    """
    def __init__(self, executor, rule, event):
        self.executor = executor
        self.rule = rule
        self.event = event
        self._context = {}
        self.evaluated = False

    def match(self, *args, **kwargs):
        return self.event['condition_type'] == self.rule['condition_type']

    @property
    def context(self):
        if self.evaluated:
            return self._context
        self.make_context()
        self.evaluated = True
        return self._context

    def make_context(self):
        self._context = {}

    def is_valid(self, *args, **kwargs):
        return self.rule.meet_condition(self)


class RulePerformer(object):
    """
    规则结果执行者
    """

    def __init__(self, executor, contexts):
        self.executor = executor
        self.contexts = contexts

    def perform(self):
        pass
