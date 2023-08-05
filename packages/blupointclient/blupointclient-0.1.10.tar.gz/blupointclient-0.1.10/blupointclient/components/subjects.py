from blupointclient.components import components_base

class QuarkSubjects(components_base):

    def __init__(self, settings):
        super(QuarkSubjects, self).__init__(settings)
        self.settings = settings

    async def get(self, id, **kwargs):
        params = self.prepare_query(kwargs)

        self.set_token(kwargs.get("token", None))
        url = self.prepare_endpoint("subjects", "_query",
                                    skip=params.get("skip"),
                                    limit=params.get("limit"),
                                    sort=params.get("sort"))

        return await self._post(url, params['document'])

