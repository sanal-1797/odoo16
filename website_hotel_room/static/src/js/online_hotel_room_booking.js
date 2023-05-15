
odoo.define('website_hotel_room..website', function (require) {
"use strict";

const publicWidget = require('web.public.widget')
publicWidget.registry.websiteEvents = publicWidget.Widget.extend({
selector: '.hotel_form',
start: function () {
$('#facilities_select').select2();
}

})

});