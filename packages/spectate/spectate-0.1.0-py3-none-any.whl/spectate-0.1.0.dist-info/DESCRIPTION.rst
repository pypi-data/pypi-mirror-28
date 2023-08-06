
Spectate
========
Create classes whose instances have tracked methods

``spectate`` is useful for remotely tracking how an instance is modified. This means that protocols
for managing updates, don't need to be the outward responsibility of a user, and can instead be
done automagically in the background.

For example, if it were desirable to keep track of element changes in a list, ``spectate`` could be
used to observe ``list.__setitiem__`` in order to be notified when a user sets the value of an element
in the list. To do this, we would first create an ``elist`` type using ``expose_as``, construct an
instance of that type, and then store callback pairs to that instance's spectator. To access a spectator,
register one with ``watch`` (e.g. ``spectator = watch(the_elist)``), retrieve a preexisting one with the
``watcher`` function. Callback pairs are stored by calling the ``watcher(the_list).callback`` method. You
can then specify, with keywords, whether the callback should be triggered ``before``, and/or or ``after``
a given method is called - hereafter refered to as "beforebacks" and "afterbacks" respectively.


