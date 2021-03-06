from app.common import boilerplate


from flask import current_app, request

from flask_restful import abort
from flask_restful import reqparse, Resource
from app.common.response_templates import CTTVResponse
from app.common.utils import fix_empty_strings
import time
from flask_restful.inputs import boolean

__author__ = 'andreap'




class Expression(Resource):

    def get(self):
        """
        Get expression data for a gene
        Test with ENSG00000136997
        """
        start_time = time.time()
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str, action='append', required=False, help="gene identifier")
        parser.add_argument('aggregate', type=boolean, required=False)


        args = parser.parse_args()
        genes = args.pop('gene',[]) or []
        aggregate = args.pop('aggregate', False)

        if not (genes ):
            abort(400, message='Please provide at least one gene')
        expression_data = self.get_expression(genes, aggregate, params=args)
        return CTTVResponse.OK(expression_data, took=time.time() - start_time)

    def post(self ):
        """
        Get expression data for a gene
        test with: {"gene":["ENSG00000136997"]},
        """
        start_time = time.time()
        args = request.get_json()
        genes = fix_empty_strings(args.pop('gene',[]) or [])
        aggregate = args.pop('aggregate', False)

        if not genes:
            abort(400, message='Please provide at least one gene')
        expression_data = self.get_expression(genes, aggregate, params=args)
        return CTTVResponse.OK(expression_data, took=time.time() - start_time)

    def get_expression(self,
                     genes,
                     aggregate,
                     params ={}):

        es = current_app.extensions['esquery']
        res = es.get_expression(genes=genes, aggregate=aggregate,
                                        **params)
        # if not res:
        #     abort(404, message='Cannot find tissue expression data for  %s'%', '.join(genes))
        return res

