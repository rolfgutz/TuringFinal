from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
import enum

class TipoUserEnum (enum.Enum):
    Adminstrador = 1
    Funcionario = 2
    Cliente = 3