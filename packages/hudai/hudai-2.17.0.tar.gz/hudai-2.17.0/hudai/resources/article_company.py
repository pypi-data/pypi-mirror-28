"""
hudai.resources.article_key_term
"""
from ..helpers.resource import Resource


class ArticleCompanyResource(Resource):
    def __init__(self, client):
        Resource.__init__(self, client, base_path='/articles/companies')
        self.resource_name = 'ArticleCompany'

    def list(self, article_id=None, company_id=None, page=None):
        query_params = self._set_limit_offset({'page': page})

        return self.http_get('/',
                             query_params={
                                 'article_id': article_id,
                                 'company_id': company_id
                             })

    def create(self, article_id, company_id):
        return self.http_post('/',
                              query_params={
                                  'article_id': article_id,
                                  'company_id': company_id
                              })

    def delete(self, article_id, company_id):
        return self.http_delete('/',
                                query_params={
                                    'article_id': article_id,
                                    'company_id': company_id
                                })
