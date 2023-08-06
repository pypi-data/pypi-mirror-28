# -*- coding: utf-8 -*-
# Description: Implements an Observable class that can be added
#              simply to another class.
#              https://en.wikipedia.org/wiki/Observer_pattern
# Author: Hywel Thomas

import logging_helper
from pprint import pformat

logging = logging_helper.setup_logging()


class ObserverError(Exception):
    pass


class Observable(object):

    def __initialise_if_required(self):

        try:
            self.observers

        except AttributeError:
            # First observer, initialise the list
            self.observers = []
            self.notified_kwargs = {}

    def register_observer(self,
                          observer):
        logging.debug(u'Register: {o} to {n}'.format(o=observer.__class__,
                                                     n=self.__class__))
        self.__initialise_if_required()

        try:
            observer.notify

        except AttributeError:
            raise ObserverError(u'{observer} does not have a notify method.'.format(observer=observer))

        self._initial_notify(observer)
        self.observers.append(observer)

    def unregister_observer(self,
                            observer):
        logging.debug(u'Unregister: {o} from {n}'.format(o=observer.__class__,
                                                         n=self.__class__))
        self.__initialise_if_required()
        self.observers.remove(observer)

    def _initial_notify(self,
                        observer):

        """ Override to perform a custom initial notify.

        If not overridden this will pass previous status of all params passed
        for this object.

        :return:
        """

        kwargs = self.notified_kwargs

        logging.debug(u'Initial Notify kwargs:\n'
                      u'{kwargs}'.format(kwargs=pformat(kwargs)))

        observer.notify(notifier=self,
                        **kwargs)

    def notify_observers(self,
                         **kwargs):
        self.__initialise_if_required()

        self.notified_kwargs.update(kwargs)

        logging.debug(u'Notify kwargs:\n'
                      u'{kwargs}'.format(kwargs=pformat(kwargs)))

        for observer in self.observers:
            observer.notify(notifier=self,
                            **kwargs)


class Observer(object):

    # TODO: Change this to 'notification' to read better in observers
    #       (Better to have single case of confusing observer.notification
    #        hidden in notify_observers)
    def notify(self,
               notifier,
               **kwargs):
        pass


class ObservableMixIn(Observable):
    pass


class ObserverMixIn(Observer):
    pass


class ObservableObserverMixIn(ObservableMixIn,
                              ObserverMixIn):
    pass
