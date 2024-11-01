from sqlmodel import SQLModel

from app.models import omdb_movie, user

#明确指定哪些名称在使用 from package import * 时被导出。只有在 __all__ 列表中的名称才会被导出，其他的名称不会被导入。
__all__ = ["SQLModel", "user", "omdb_movie"]

#如果__init__.py 为空，表示该模块虽然被标识为一个python包，但是所有模块的导入都需要显式地在其他模块中进行.