
// defining archive and unurchive button view

odoo.define('hr_idc.BasicView', function (require) {
    "use strict";
    var session = require('web.session');
    var BasicView = require('web.BasicView');
    BasicView.include({
        init: function(viewInfo, params) {
            var self = this;
            this._super.apply(this, arguments);
            var model = ['hr.employee'].includes(self.controllerParams.modelName) ? 'True' : 'False';
            if(model) {
                session.user_has_group('hr_idc.group_hr_itadmin').then(function(has_group) {
                    if(!has_group) {
                        self.controllerParams.archiveEnabled = 'False' in viewInfo.fields;
                    }
                });
            }
        },
    });
});