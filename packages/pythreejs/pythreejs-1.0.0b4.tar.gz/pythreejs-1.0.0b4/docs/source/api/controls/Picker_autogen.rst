
.. py:currentmodule:: pythreejs

Picker
====================================================

.. Use autoclass to fill any memebers not manually specified.
   This ensures it picks up any members in overridden classes.

.. autohastraits:: Picker(controlling=None, )
    :members:
    :undoc-members:


    Inherits :py:class:`~pythreejs.Controls`.

    Three.js docs: https://threejs.org/docs/#api/controls/Picker


    .. py:attribute:: event

        .. sourcecode:: python

            Unicode("click", allow_none=False).tag(sync=True)

    .. py:attribute:: all

        .. sourcecode:: python

            Bool(False, allow_none=False).tag(sync=True)

    .. py:attribute:: distance

        .. sourcecode:: python

            CFloat(None, allow_none=True).tag(sync=True)

    .. py:attribute:: point

        .. sourcecode:: python

            Vector3(default_value=[0,0,0]).tag(sync=True)

    .. py:attribute:: face

        .. sourcecode:: python

            Vector3(default_value=[0,0,0]).tag(sync=True)

    .. py:attribute:: faceNormal

        .. sourcecode:: python

            Vector3(default_value=[0,0,0]).tag(sync=True)

    .. py:attribute:: faceVertices

        .. sourcecode:: python

            List(trait=List()).tag(sync=True)

    .. py:attribute:: faceIndex

        .. sourcecode:: python

            CInt(None, allow_none=True).tag(sync=True)

    .. py:attribute:: modifiers

        .. sourcecode:: python

            List().tag(sync=True)

    .. py:attribute:: object

        .. sourcecode:: python

            Instance(Object3D, allow_none=True).tag(sync=True, **widget_serialization)

    .. py:attribute:: picked

        .. sourcecode:: python

            List().tag(sync=True)

    .. py:attribute:: uv

        .. sourcecode:: python

            Vector2(default_value=[0,0]).tag(sync=True)

    .. py:attribute:: indices

        .. sourcecode:: python

            List().tag(sync=True)

