from django.contrib.auth.mixins import UserPassesTestMixin


class OrganizadorPermission(UserPassesTestMixin):
    """Mixin que verifica se o usuário é do grupo 'Organizador'"""

    def test_func(self):
        # pylint: disable=no-member
        return self.request.user.groups.filter(name="Organizers").exists()


class AdministradorPermission(UserPassesTestMixin):
    """Mixin que verifica se o usuário é do grupo 'Administrador'"""

    def test_func(self):
        # pylint: disable=no-member
        return self.request.user.groups.filter(name="Administrators").exists()
