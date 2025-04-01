import imp
import MinhThu_curve_tool
import MinhThu_curve_tool.core.curve_presets
import MinhThu_curve_tool.ui.dialogs.css_stylesheet
import MinhThu_curve_tool.core.curve_maker_tool
import MinhThu_curve_tool.ui.dialogs.curve_maker_dialog
import MinhThu_curve_tool.ui.dialogs
import MinhThu_curve_tool.ui.curve_maker_controller
import MinhThu_curve_tool.ui

imp.reload(MinhThu_curve_tool.core.curve_presets)
imp.reload(MinhThu_curve_tool.ui.dialogs.css_stylesheet)
imp.reload(MinhThu_curve_tool.core.curve_maker_tool)
imp.reload(MinhThu_curve_tool.ui.dialogs.curve_maker_dialog)
imp.reload(MinhThu_curve_tool.ui.dialogs)
imp.reload(MinhThu_curve_tool.ui.curve_maker_controller)
imp.reload(MinhThu_curve_tool.ui)

MinhThu_curve_tool.ui.launchUI()
