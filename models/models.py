# -*- coding: utf-8 -*-

from odoo import models, fields, api
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    label = fields.Char("Label")
    part_id = fields.One2many('part.number','fleetguard','Part Number')
    
    

    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    label = fields.Char(related='product_id.label')
    avail = fields.Boolean('Available?')
    yrprtno = fields.Many2one('part.number','Your P/N')
    #number = fields.Integer(compute='_compute_get_number',store=True)
    
        
    @api.onchange('yrprtno')
    def onchange_yrtprtno(self):
        for rec in self:
            rec.product_id = []
            res = []
            res = {}
            res['domain'] = {'product_id':[('part_id','=',rec.yrprtno.id)]}
        return res    
    
    #@api.depends('sequence', 'order_id')
    #def _compute_get_number(self):
    #    for order in self.mapped('order_id'):
    #        number = 1
    #        for line in order.order_line:
    #            line.number = number
    #            number += 1
    
class AccountMove(models.Model):
    _inherit = 'account.move'

    tax_box = fields.Boolean('Tax Available?',compute='check_tax_box')
    banking_details = fields.Char(related="company_id.bank_name_details")
    account_number = fields.Char(related="company_id.account_number")
    usd_numb = fields.Char(related="company_id.usd_numb")
    account_name = fields.Char(related="company_id.account_name")
    swft_code = fields.Char(related="company_id.swft_code")
    currency = fields.Char(related="company_id.currency")
    branch = fields.Char(related="company_id.branch")
    
    prepared_by = fields.Many2one('hr.employee','Prepared By')
    
    @api.depends('amount_by_group')
    def check_tax_box(self):
        for rec in self:
            if rec.amount_by_group != 0:
                rec.tax_box = True
            else:
                rec.tax_box = False


    #@api.depends('invoice_user_id')
    #def prepped_by(self):
        #for rec in self:
            #if rec.invoice_user_id:
                #rec.prepared_by = rec.invoice_user_id
            #else:
                #rec.prepared_by = ""
                
#class AccountInvoiceLine(models.Model):
#    _inherit = 'account.move.line'

#    number = fields.Integer(compute='_compute_number', store=True)

#    @api.depends('sequence', 'move_id')
#    def _compute_number(self):
#        for invoice in self.mapped('move_id'):
#            number = 1
#            for line in invoice.invoice_line_ids:
#                line.number = number
#                number += 1

                
class ResCompany(models.Model):
    _inherit = 'res.company'

    bank_name_details = fields.Char("Bank Name")
    account_number = fields.Char('Account Number')
    account_name = fields.Char('Account Name')
    swft_code = fields.Char('Code')
    currency = fields.Char('Currency',default='UGX')
    branch = fields.Char('Branch')
    usd_numb = fields.Char('USD Acc No.')



class PartNumber(models.Model):
    _name = 'part.number'
    _rec_name = 'part_number'
    
    part_number = fields.Char('Part Number')
    fleetguard = fields.Many2one('product.template','FleetGuard #')
    
class ResUsers(models.Model):
    _inherit = 'res.users'
    jil_signature = fields.Binary('Signature')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    jil_signature = fields.Binary(related='user_id.jil_signature')                               

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    exclude_fleetguard = fields.Boolean('Not a Fleetuard Product?')
    exclude_part_no = fields.Boolean('Exclude Your P/N?')
    note1 = fields.Html('NOTE:', default="""
                <ul>  
                    <li>Items indicated being in stock are available in our warehouse/showroom on the above address</li>
                    <li>Items Indicated as not being in stock are available from the Cummins/ Fleetguard warehouse in Belgium</li>
                    <li>Prices are in UGX, excl VAT, ex works our Kampala warehouse. UGX prices for items not being in stock are valid for future deliveries by sea container. For airfreight solutions we need to quote separate prices.</li>

                </ul>
                <p>We trust to have been of good service with the above and look forward to your favourable reply.</p>
                """)

class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    customer = fields.Many2one(related='stock_move_id.partner_id', string="Customer")
    vendor = fields.Many2one(related='stock_move_id.picking_partner_id', string="Vendor")