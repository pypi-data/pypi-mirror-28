# Copyright 2016 The Cebes Authors. All Rights Reserved.
#
# Licensed under the Apache License, version 2.0 (the "License").
# You may not use this work except in compliance with the License,
# which is available at www.apache.org/licenses/LICENSE-2.0
#
# This software is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied, as more fully set forth in the License.
#
# See the NOTICE file distributed with this work for information regarding copyright ownership.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import threading
import contextlib


class DefaultStack(threading.local):
    """A thread-local stack of objects for providing implicit defaults."""

    def __init__(self):
        super(DefaultStack, self).__init__()
        self._enforce_nesting = True
        self.stack = []

    def get_default(self):
        return self.stack[-1] if len(self.stack) >= 1 else None

    def reset(self):
        self.stack = []

    @property
    def enforce_nesting(self):
        return self._enforce_nesting

    @enforce_nesting.setter
    def enforce_nesting(self, value):
        self._enforce_nesting = value

    @contextlib.contextmanager
    def get_controller(self, default):
        """A context manager for manipulating a default stack."""
        try:
            self.stack.append(default)
            yield default
        finally:
            if self._enforce_nesting:
                if self.stack[-1] is not default:
                    raise AssertionError('Nesting violated for default stack of {} objects'.format(type(default)))
                self.stack.pop()
            else:
                self.stack.remove(default)
