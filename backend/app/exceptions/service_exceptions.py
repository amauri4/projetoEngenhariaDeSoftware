class ServiceError(Exception):
    """Erro genérico na camada de serviço."""
    pass


class ConflictError(ServiceError):
    """Erro de conflito, como dados duplicados."""
    pass


class AuthError(ServiceError):
    """Erro de autenticação."""
    pass
