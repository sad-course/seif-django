from social_core.backends.oauth import BaseOAuth2


class SuapOAuth2(BaseOAuth2):
    name = "suap"
    AUTHORIZATION_URL = "https://suap.ifrn.edu.br/o/authorize/"
    ACCESS_TOKEN_METHOD = "POST"
    ACCESS_TOKEN_URL = "https://suap.ifrn.edu.br/o/token/"
    ID_KEY = "identificacao"
    RESPONSE_TYPE = "code"
    REDIRECT_STATE = True
    STATE_PARAMETER = True
    USER_DATA_URL = "https://suap.ifrn.edu.br/api/eu/"
    EXTRA_USER_DATA_URL = (
        "https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/"
    )

    def user_data(self, access_token, *args, **kwargs):
        """
        Loads user data from SUAP service
        """
        method = "GET"
        data = {"scope": kwargs.get("response").get("scope")}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.request(
            url=self.USER_DATA_URL, method=method, data=data, headers=headers
        ).json()

        # extra_response = self.request(
        #     url=self.EXTRA_USER_DATA_URL, method=method, headers=headers
        # ).json()

        # with open(
        #     f"user_data_{response.get('identificacao')}.json", "w"
        # ) as user_data_suap:
        #     user_data_suap.write(json.dumps(response))

        return response

    def get_user_details(self, response):
        """
        Retorna um dicionário mapeando os fields do settings.AUTH_USER_MODEL.
        """

        splitted_name = response["nome"].split()
        first_name, last_name = splitted_name[0], ""
        if len(splitted_name) > 1:
            last_name = splitted_name[-1]

        username = f"{first_name}_{response[self.ID_KEY]}"
        return {
            "username": username,
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "email": response["email"],
        }

    def auth_html(self):
        """Implementação do método abstrato."""
        return "<html><body>Auth HTML not implemented</body></html>"
