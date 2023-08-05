def logmod(*modules):
    import structlog
    import inspect
    import types
    import functools
    logger = structlog.get_logger('logmod')

    def wrapper(func):
        log = logger.bind(func=func.__name__, mod=func.__module__)
        fname = func.__module__+'.'+func.__name__ if func.__module__ else func.__name__

        def _shim(*args, **kwargs):
            f = inspect.stack()[1]
            log.info(
                f'{f.function} -> {fname} at {f.filename}:{f.lineno}',
                caller=f.function,
                callsite={'filename': f.filename, 'lineno': f.lineno},
                args=args,
                kwargs=kwargs)
            return func(*args, **kwargs)
        return _shim

    for module in modules:
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, (types.FunctionType, types.MethodType, types.BuiltinFunctionType)):
                setattr(module, name, functools.wraps(obj)(wrapper)(obj))
