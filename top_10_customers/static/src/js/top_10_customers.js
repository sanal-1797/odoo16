
odoo.define('top_10_customers.dynamic', function (require) {
   var PublicWidget = require('web.public.widget');
   var rpc = require('web.rpc');
   var Dynamic = PublicWidget.Widget.extend({
       selector: '.dynamic_snippet_blog',
       start: function () {
           var self = this;
           rpc.query({
               route: '/top_customers',
               params: {},
           }).then(function (result) {
           self.$("#customers").empty()
               $.each(result , function(index, val) {
                    self.$("#customers").append('<tr><td><a href="/partner/'+val['partner_id']+'">' + val['partner_name'] +
                    '<a></td><td>'+val['order_count']+'</td></tr>');
                });
           });
       },
   });
   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});