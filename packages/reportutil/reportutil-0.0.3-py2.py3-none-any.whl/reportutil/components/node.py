# encoding: utf-8

import logging_helper
from copy import deepcopy
from abc import ABCMeta, abstractmethod, abstractproperty
from .._config import register_report_config
from .._constants import ReportConstant

logging = logging_helper.setup_logging()


class ReportNode(object):

    """ This is the base class for all report nodes. """

    __metaclass__ = ABCMeta

    def __init__(self,
                 parent=None,
                 key=None,  # None for root node
                 *args,
                 **kwargs):

        self._parent = parent
        self._name = key
        self._cfg = register_report_config()

        # Setup structure for this node
        try:
            # Check whether node registered
            node = self._cfg[self.node_key]
            assert self.node_type == node[ReportConstant.node_type]

        except KeyError:
            # If not registered register node
            self._cfg[self.node_key] = {
                ReportConstant.node_type: self.node_type
            }

        except AssertionError:
            raise TypeError(u'Existing definition does not match node definition! '
                            u'{exist} != {new}'.format(exist=self.node_type,
                                                       new=self._cfg[self.node_key][ReportConstant.node_type]))

        # Initialise child tracking object
        self._child_nodes = deepcopy(ReportConstant.node_template)

    @property
    def parent_node(self):
        return self._parent

    @property
    def node_key(self):
        node_key = u'{cfg}.{key}'.format(cfg=ReportConstant.config.key,
                                         key=ReportConstant.config_properties.structure)

        if self.name is not None:
            if self.parent_node is not None:
                node_key = self.parent_node.node_key

            node_key = u'{root}.{node}'.format(root=node_key,
                                               node=self.name)

        return node_key

    @abstractproperty
    def node_type(self):

        """ Return one of ReportConstant.types """

        pass

    @abstractproperty
    def node_path(self):

        """ Fully qualified path to this node """

        pass

    @abstractmethod
    def generate(self):

        """ Generates the report, creating the directory structure and files that make up this report node.

        :return: path to report node index file.
        """

        pass

    @property
    def name(self):
        return self._name
