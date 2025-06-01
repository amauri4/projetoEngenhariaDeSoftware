from app.exceptions.base_exceptions import AppBaseError

class RepositoryError(AppBaseError):
    """Erro genérico no repositório."""
    pass

class NotFoundError(RepositoryError):
    """Recurso não encontrado no repositório."""
    pass
