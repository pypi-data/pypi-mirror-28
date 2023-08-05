##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Grok interfaces
"""
import grokcore.component.interfaces
import grokcore.security.interfaces
import grokcore.view.interfaces

from zope import interface
from zope.publisher.interfaces.http import IHTTPRequest


class IBaseClasses(
        grokcore.component.interfaces.IBaseClasses,
        grokcore.security.interfaces.IBaseClasses,
        grokcore.view.interfaces.IBaseClasses):

    Traverser = interface.Attribute("Base class for custom traversers.")


class IGrokTraverser(
        grokcore.component.interfaces.IGrokcoreComponentAPI,
        grokcore.security.interfaces.IGrokcoreSecurityAPI,
        grokcore.view.interfaces.IGrokcoreViewAPI,
        IBaseClasses):
    pass


class IRESTLayer(IHTTPRequest):
    """REST-specific Request functionality.

    Base Interfaces for defining REST-layers.
    """
