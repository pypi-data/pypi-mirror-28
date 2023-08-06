# encoding: utf-8

import os
import logging_helper
from fdutil.path_tools import ensure_path_exists
from .._constants import ReportConstant
from .node import ReportNode

logging = logging_helper.setup_logging()


class ReportDirNode(ReportNode):

    """ The ReportDirNode object represents a single directory in the report structure.
        The represented directory can contain more ReportDirs or Report Files (i.e HTMLReport objects).
        A report directory should also contain an index file as this will be used as the primary access
        point to the report directory.

    """

    @property
    def node_type(self):
        return ReportConstant.types.dir

    @property
    def node_path(self):
        return os.path.join(self.parent_node.node_path,
                            self.name)

    @property
    def children(self):
        return self._child_nodes

    @property
    def child_dirs(self):
        return self.children.get(ReportConstant.types.dir, [])

    @property
    def child_files(self):
        return self.children.get(ReportConstant.types.file, [])

    def add_node(self,
                 key,
                 node_class,
                 *args,
                 **kwargs):

        # We create the node no matter what as we need it instantiated to check the type.
        obj = node_class(parent=self,
                         key=key,
                         *args,
                         **kwargs)

        matches = [node for node in self._child_nodes[obj.node_type] if node.node_key == obj.node_key]

        if bool(matches):
            raise KeyError(u'Node ({node}) already registered'.format(node=obj.node_key))

        else:
            self._child_nodes[obj.node_type].append(obj)

        return obj

    def get_node(self,
                 name):
        # TODO: Retrieve and return the requested report node object
        raise NotImplementedError(u'get_node method not written yet!')

    def generate_children(self):

        """ Invokes the generate methods on all children. """

        for d in self.child_dirs:
            d.generate()

        for f in self.child_files:
            f.generate()

    def generate(self):

        """ Generates the report node, creating the directory structure and files that make up the report.

        :return: path to reports main index file.
        """

        # Generate this directory
        ensure_path_exists(self.node_path)

        # TODO: Generate index

        # Generate Children
        self.generate_children()
