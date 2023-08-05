import enum
import inspect
from uqbar.apis.MemberDocumenter import MemberDocumenter


class ClassDocumenter(MemberDocumenter):
    """
    A basic class documenter.

    ::

        >>> import uqbar.apis
        >>> path = 'uqbar.apis.ClassDocumenter.ClassDocumenter'
        >>> documenter = uqbar.apis.ClassDocumenter(path)
        >>> documentation = str(documenter)
        >>> print(documentation)
        .. autoclass:: ClassDocumenter
           :members:
           :undoc-members:

    .. tip::

       Subclass :py:class:`~uqbar.apis.ClassDocumenter` to
       implement your own custom class documentation output. You'll
       need to provide your desired reStructuredText output via an
       overridden
       :py:meth:`~uqbar.apis.ClassDocumenter.ClassDocumenter.__str__`
       implementation.

       See :py:class:`~uqbar.apis.SummarizingClassDocumenter` for an example.

    :param package_path: the module path and name of the member to document
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Documenters'

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        return '\n'.join([
            '.. autoclass:: {}'.format(
                self.client.__name__,
                ),
            '   :members:',
            '   :undoc-members:',
            ])

    ### PUBLIC METHODS ###

    @classmethod
    def validate_client(cls, client: object, module_path: str) -> bool:
        return (
            isinstance(client, type) and
            client.__module__ == module_path
            )

    ### PUBLIC PROPERTIES ###

    @property
    def documentation_section(self) -> str:
        if hasattr(self.client, '__documentation_section__'):
            return self.client.__documentation_section__
        elif inspect.isabstract(self.client):
            return 'Abstract Classes'
        elif issubclass(self.client, enum.Enum):
            return 'Enumerations'
        elif issubclass(self.client, Exception):
            return 'Exceptions'
        return 'Classes'
