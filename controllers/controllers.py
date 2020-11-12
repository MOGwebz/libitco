# -*- coding: utf-8 -*-
from odoo import http

# class Libitco(http.Controller):
#     @http.route('/libitco/libitco/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/libitco/libitco/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('libitco.listing', {
#             'root': '/libitco/libitco',
#             'objects': http.request.env['libitco.libitco'].search([]),
#         })

#     @http.route('/libitco/libitco/objects/<model("libitco.libitco"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('libitco.object', {
#             'object': obj
#         })