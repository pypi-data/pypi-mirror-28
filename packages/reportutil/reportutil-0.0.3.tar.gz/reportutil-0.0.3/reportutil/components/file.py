# encoding: utf-8

import os
import logging_helper
from abc import abstractmethod
from .._constants import ReportConstant
from .node import ReportNode

logging = logging_helper.setup_logging()


class ReportFileNode(ReportNode):

    """ The ReportFileNode object represents a single file in the report structure. """

    ADD_METHOD = u'write'

    def __init__(self,
                 *args,
                 **kwargs):

        super(ReportFileNode, self).__init__(*args, **kwargs)

        self._report_objects = []

    @property
    def node_type(self):
        return ReportConstant.types.file

    @property
    def node_path(self):
        return os.path.join(self.parent_node.node_path,
                            self.filename)

    @property
    def filename(self):
        return self.name

    @abstractmethod
    def generate(self):

        """
        Generate this report node writing it to file.

        For example:
            if len(self._report_objects) > 0:

                filepath = os.path.join(self.parent.node_path,
                                        self.filename)

                with open(filepath, u'wb') as f:
                    for obj in self._report_objects:
                        method = getattr(obj, self.ADD_METHOD)
                        data = method()
                        f.write(data)
        """
        pass

    def add(self,
            obj):

        """
        Add an object to be written into this file node.

        """

        # Ensure object has a write method
        method = getattr(obj, self.ADD_METHOD)  # Raises AttributeError if no attribute exists

        # Ensure attribute is a callable method
        if not callable(method):
            raise TypeError(u'Object being added to report does not '
                            u'have a callable {method} method!'.format(method=self.ADD_METHOD))

        # Add object to list of objects to be drawn in the report
        self._report_objects.append(obj)
