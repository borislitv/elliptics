# =============================================================================
# 2013+ Copyright (c) Kirill Smorodinnikov <shaitkir@gmail.com>
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# =============================================================================

from elliptics.core import Session
from elliptics.core import monitor_stat_categories
from elliptics.log import logged_class
from elliptics.route import Address
from elliptics.route import RouteList


@logged_class
class Session(Session):
    __forward = Session.forward

    def __init__(self, node):
        '''
        Initializes session by the node"

        session = elliptics.Session(node)"
        '''
        super(Session, self).__init__(node)
        self._node = node

    def clone(self):
        '''
        Creates and returns session which is equal to current"
        but completely independent from it."

        cloned_session = session.clone()
        '''
        session = super(Session, self).clone()
        session.__class__ = self.__class__
        session._node = self._node
        return session

    @property
    def routes(self):
        """
        Returns current routes table\n
        routes = session.routes
        """
        return RouteList.from_routes(super(Session, self).routes)

    def lookup_address(self, key, group_id):
        """
        Returns address of node from specified group_id which is responsible for the key\n
        address = session.lookup_address('looking up key')
        print '\'looking up key\' should lives on node:', address
        """
        return Address.from_host_port(super(Session, self).lookup_address(key, group_id))

    def bulk_write(self, datas):
        """
        Writes several objects at once.
        @datas - can be dict: {key:value} or iterable container of tuples (elliptics.IoAttr, data)
        """
        if type(datas) is dict:
            return super(Session, self).bulk_write(datas.items())
        else:
            return super(Session, self).bulk_write(datas)

    def set_direct_id(self, address, backend_id=None):
        """
        Makes session sends all request directly to @address without forwarding.
        If @backend_id is not None all requests sent by session will be handled at specified backend
        """
        if backend_id is None:
            super(Session, self).set_direct_id(host=address.host,
                                               port=address.port,
                                               family=address.family)
        else:
            super(Session, self).set_direct_id(host=address.host,
                                               port=address.port,
                                               family=address.family,
                                               backend_id=backend_id)

    @property
    def forward(self):
        """
        If is set stick session to particular remote address.
        This remote won't handle request but will resend it to proper server node.
        If proper server node isn't available on forward node, forward node will fail request with -ENOTSUP error.
        """
        if self.__forward is None:
            return None
        return Address.from_host_port_family(self.__forward)

    @forward.setter
    def forward(self, remote):
        self.__forward = None if remote is None else str(remote)

    @forward.deleter
    def forward(self):
        self.__forward = None

    def update_status(self, address, status):
        """
        Updates status of @address to @status.
        If address is elliptics.Address then status of this node will be updated.
        """
        super(Session, self).update_status(host=address.host,
                                           port=address.port,
                                           family=address.family,
                                           status=status)

    def enable_backend(self, address, backend_id):
        """
        Enables backend @backend_id on @address.
        Return elliptics.AsyncResult that provides new status of backend
        """
        return super(Session, self).enable_backend(host=address.host,
                                                   port=address.port,
                                                   family=address.family,
                                                   backend_id=backend_id)

    def disable_backend(self, address, backend_id):
        """
        Disables backend @backend_id on @address.
        Return elliptics.AsyncResult that provides new status of backend
        """
        return super(Session, self).disable_backend(host=address.host,
                                                    port=address.port,
                                                    family=address.family,
                                                    backend_id=backend_id)

    def remove_backend(self, address, backend_id):
        """
        Removes backend @backend_id on @address.
        Return elliptics.AsyncResult that provides new status of backend.
        """
        return super(Session, self).remove_backend(host=address.host,
                                                   port=address.port,
                                                   family=address.family,
                                                   backend_id=backend_id)

    def start_defrag(self, address, backend_id, chunks_dir=None):
        """
        Starts defragmentation of backend @backend_id on @address with using chunks_dir for temporary chunks.

        Args:
            address(elliptics.Address): address of the node where backend should be defraged
            backend_id(int): id of the backend which should be defraged
            chunks_dir(str or None): optional directory which should be used for temporary chunks

        Returns:
            elliptics.AsyncResult that provides new status of backend
        """
        return super(Session, self).start_defrag(host=address.host,
                                                 port=address.port,
                                                 family=address.family,
                                                 backend_id=backend_id,
                                                 chunks_dir=chunks_dir)

    def start_compact(self, address, backend_id, chunks_dir=None):
        """
        Starts compaction of backend @backend_id on @address with using chunks_dir for temporary chunks.

        Args:
            address(elliptics.Address): address of the node where backend should be compacted
            backend_id(int): id of the backend which should be compacted
            chunks_dir(str or None): optional directory which should be used for temporary chunks

        Returns:
            elliptics.AsyncResult that provides new status of backend
        """
        return super(Session, self).start_compact(host=address.host,
                                                  port=address.port,
                                                  family=address.family,
                                                  backend_id=backend_id,
                                                  chunks_dir=chunks_dir)

    def stop_defrag(self, address, backend_id):
        """
        Stops defragmentation of backend @backend_id on @address.
        Return elliptics.AsyncResult that provides new status of backend
        """
        return super(Session, self).stop_defrag(host=address.host,
                                                port=address.port,
                                                family=address.family,
                                                backend_id=backend_id)

    def start_inspect(self, address, backend_id):
        """
        Start inspection of backend @backend_id on @address.
        Return elliptics.AsyncResult that provides new status of backend
        """
        return super(Session, self).start_inspect(host=address.host,
                                                  port=address.port,
                                                  family=address.family,
                                                  backend_id=backend_id)

    def stop_inspect(self, address, backend_id):
        """
        Stop inspection of backend @backend_id on @address.
        Return elliptics.AsyncResult that provides new status of backend
        """
        return super(Session, self).stop_inspect(host=address.host,
                                                 port=address.port,
                                                 family=address.family,
                                                 backend_id=backend_id)

    def request_backends_status(self, address):
        """
        Request statuses of all backends from @address.
        Return elliptics.AsyncResult that provides statuses of all presented backend
        """
        return super(Session, self).request_backends_status(host=address.host,
                                                            port=address.port,
                                                            family=address.family)

    def make_readonly(self, address, backend_id):
        '''
        Makes read-only backend @backend_id on @address
        '''
        return super(Session, self).make_readonly(host=address.host,
                                                  port=address.port,
                                                  family=address.family,
                                                  backend_id=backend_id)

    def make_writable(self, address, backend_id):
        '''
        Makes read-write-able backend @backend_id on @address
        '''
        return super(Session, self).make_writable(host=address.host,
                                                  port=address.port,
                                                  family=address.family,
                                                  backend_id=backend_id)

    def set_backend_ids(self, address, backend_id, ids):
        '''
        Sets new ids to backend with @backend_id at node addressed by @host, @port, @family.
        '''
        return super(Session, self).set_backend_ids(host=address.host,
                                                    port=address.port,
                                                    family=address.family,
                                                    backend_id=backend_id,
                                                    ids=ids)

    def set_delay(self, address, backend_id, delay):
        '''
        Sets @delay in milliseconds for backend with @backend_id at node @address
        '''
        return super(Session, self).set_delay(host=address.host,
                                              port=address.port,
                                              family=address.family,
                                              backend_id=backend_id,
                                              delay=delay)

    def monitor_stat(self, address=None, categories=monitor_stat_categories.all, backends=None):
        '''
        Gather monitor statistics of specified categories from @address.
        If @address is None monitoring statistics will be gathered from all nodes.\n
        If @backends isn't None statistics will be requested for backends with id
        specified by backends. If @backends is None statistics will be requested for all backends.\n
        result = session.monitor_stat(elliptics.Address.from_host_port('host.com:1025'), categories, [1,2,3])
        stats = result.get()
        '''
        if not address:
            address = ()
        else:
            address = tuple(address)
        if not backends:
            backends = []
        else:
            backends = list(backends)
        return super(Session, self).monitor_stat(address, categories, backends)
