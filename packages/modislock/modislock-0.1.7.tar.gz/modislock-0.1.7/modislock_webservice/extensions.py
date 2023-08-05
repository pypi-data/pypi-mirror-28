# coding: utf-8

from flask_security import Security
from flask_cache import Cache
from flask_mail import Mail
from flask_celery import Celery
from flask_htmlmin import HTMLMIN
from flask_assets import Environment, Bundle
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf.csrf import CSRFProtect
from flask_marshmallow import Marshmallow
from flask_restful import Api

"""Extensions used by Modis Lock application

"""


security = Security()
marshmallow = Marshmallow()
csrf_protect = CSRFProtect()
html_min = HTMLMIN()
cache = Cache()
mail = Mail()
celery = Celery()
assets = Environment()
debug_toolbar = DebugToolbarExtension()
rest_api = Api()

# These represent the CSS and JS libraries used by each controller. They are compiled at installation for faster access
asset_bundles = {
    'welcome_js': Bundle('js/libs/jquery.bootstrap.wizard.js',
                         '../pages/welcome/welcome.js',
                         filters='jsmin',
                         output='js/welcome_js.js'),
    'layout_css': Bundle('css/libs/bootstrap.css',
                         'css/libs/font-awesome.css',
                         'css/animate.css',
                         'css/style.css',
                         'css/libs/toastr.css',
                         filters='cssmin',
                         output='css/layout_css.css'),
    'layout_js': Bundle('js/libs/jquery-3.2.1.js',
                        'js/libs/bootstrap.js',
                        'js/libs/metisMenu.js',
                        'js/libs/jquery.slimscroll.js',
                        'js/libs/moment.js',
                        'js/inspinia.js',
                        'js/libs/toastr.js',
                        Bundle('js/libs/pace.min.js'),
                        filters='jsmin',
                        output='js/layout_js.js'),
    'tables_css': Bundle('DataTables-1.10.15/media/css/dataTables.bootstrap.css',
                         'DataTables-1.10.15/extensions/Responsive/css/responsive.bootstrap.css',
                         'DataTables-1.10.15/extensions/Buttons/css/buttons.bootstrap.css',
                         'DataTables-1.10.15/extensions/Select/css/select.bootstrap.css',
                         'Editor-1.6.2/css/editor.bootstrap.css',
                         filters='cssmin',
                         output='css/tables_css.css'),
    'tables_js': Bundle('DataTables-1.10.15/media/js/jquery.dataTables.js',
                        'DataTables-1.10.15/media/js/dataTables.bootstrap.js',
                        'DataTables-1.10.15/extensions/Buttons/js/dataTables.buttons.js',
                        'DataTables-1.10.15/extensions/Buttons/js/buttons.bootstrap.js',
                        'DataTables-1.10.15/extensions/Responsive/js/dataTables.responsive.js',
                        'DataTables-1.10.15/extensions/Responsive/js/responsive.bootstrap.js',
                        'DataTables-1.10.15/extensions/Select/js/dataTables.select.js',
                        'Editor-1.6.2/js/dataTables.editor.js',
                        'Editor-1.6.2/js/editor.bootstrap.js',
                        filters='jsmin',
                        output='js/tables_js.js'),
    'users_css': Bundle('css/libs/bootstrap-toggle.css',
                        'css/libs/jquery.steps.css',
                        'css/libs/jquery-ui-1.10.3.custom.css',
                        'css/libs/funkyradio.css',
                        '../pages/users/users.css',
                        filters='cssmin',
                        output='css/users_css.css'),
    'users_js': Bundle('js/libs/jquery.steps.js',
                       'js/libs/u2f-api.js',
                       'js/libs/bootstrap-toggle.js',
                       'js/libs/bootstrap-confirmation.js',
                       Bundle('js/libs/jquery-ui-1.10.3.custom.min.js'),
                       '../pages/users/user_edit.js',
                       '../pages/users/common.js',
                       filters='jsmin',
                       output='js/users_js.js'),
    'logs_css': Bundle(Bundle('css/libs/vis-timeline-graph2d.min.css'),
                       'css/libs/bootstrap-datetimepicker.css',
                       'css/libs/daterangepicker.css',
                       '../pages/logs/logs.css',
                       filters='cssmin',
                       output='css/logs_css.css'),
    'logs_js': Bundle('js/libs/vis.js',
                      Bundle('js/libs/vis-timeline-graph2d.min.js',
                             'js/libs/bootstrap-datetimepicker.min.js'),
                      'js/libs/daterangepicker.js',
                      '../pages/logs/logs.js',
                      filters='jsmin',
                      output='js/logs_js.js'),
    'select_css': Bundle('css/libs/select2.css',
                         'css/libs/select2-bootstrap.css',
                         filters='cssmin',
                         output='css/select_css.css'),
    'select_js': Bundle('js/libs/select2.full.js',
                        filters='jsmin',
                        output='js/select_js.js'),
    'system_css': Bundle('css/libs/jquery.bootstrap-touchspin.css',
                         'css/libs/jquery.highlight-within-textarea.css',
                         '../pages/system/system.css',
                         filters='cssmin',
                         output='css/system_css.css'),
    'system_js': Bundle('js/libs/jquery.bootstrap-touchspin.min.js',
                        'js/libs/jquery.highlight-within-textarea.js',
                        '../pages/system/system.js',
                        filters='jsmin',
                        output='js/system_js.js'),
    'settings_reader_css': Bundle('css/libs/bootstrap-toggle.css',
                                  'css/libs/jquery.bootstrap-touchspin.css',
                                  '../pages/settings_reader/settings_reader.css',
                                  filters='cssmin',
                                  output='css/settings_reader_css.css'),
    'settings_reader_js': Bundle('js/libs/bootstrap-toggle.js',
                                 'js/libs/jquery.bootstrap-touchspin.js',
                                 '../pages/settings_reader/settings_reader.js',
                                 filters='jsmin',
                                 output='js/settings_reader_js.js'),
    'settings_rules_css': Bundle('css/libs/bootstrap-toggle.css',
                                 '../pages/settings_rules/settings_rules.css',
                                 filters='cssmin',
                                 output='css/settings_rules_css.css'),
    'settings_rules_js': Bundle('js/libs/bootstrap-toggle.js',
                                '../pages/settings_rules/settings_rules.js',
                                filters='jsmin',
                                output='js/settings_rules_js.js'),
    'settings_network_css': Bundle('css/libs/bootstrap-toggle.css',
                                   '../pages/settings_network/settings_network.css',
                                   filters='cssmin',
                                   output='css/settings_network_css.css'),
    'settings_network_js': Bundle('js/libs/bootstrap-toggle.js',
                                  '../pages/settings_network/settings_network.js',
                                  filters='jsmin',
                                  output='js/settings_network_js.js'),
    'settings_backup_css': Bundle('css/libs/bootstrap-toggle.css',
                                  'css/libs/jquery.bootstrap-touchspin.css',
                                  '../pages/settings_backup/settings_backup.css',
                                  filters='cssmin',
                                  output='css/settings_backup_css.css'),
    'settings_backup_js': Bundle('js/libs/bootstrap-filestyle.js',
                                 'js/libs/bootstrap-confirmation.js',
                                 '../pages/settings_backup/settings_backup.js',
                                 filters='jsmin',
                                 output='js/settings_backup_js.js'),
    'settings_api_css': Bundle('css/libs/bootstrap-toggle.css',
                               '../pages/settings_api/settings_api.js',
                               filters='cssmin',
                               output='css/settings_api_css.css'),
    'settings_api_js': Bundle('js/libs/bootstrap-confirmation.js',
                              '../pages/settings_api/settings_api.js',
                              filters='jsmin',
                              output='js/settings_api_js.js'),
    'settings_security_css': Bundle('css/libs/bootstrap-toggle.css',
                                    '../pages/settings_security/settings_security.css',
                                    filters='cssmin',
                                    output='css/settings_security_css.css'),
    'settings_security_js': Bundle('js/libs/bootstrap-confirmation.js',
                                   '../pages/settings_security/settings_security.js',
                                   filters='jsmin',
                                   output='js/settings_security_js.js')
}
