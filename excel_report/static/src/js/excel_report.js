/** @odoo-module **/
import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";

registry.category("ir.actions.report handlers").add("custom_xlsx", async (action, options, env) => {
    const userService = env.services.user;
    const context = userService ? userService.context : (env.services.company ? env.services.company.currentCompany.context : {});
    
    function _getReportUrl(action, type) {
        let url = `/report/${type}/${action.report_name}`;
        const actionContext = action.context || {};
        
        if (action.data && JSON.stringify(action.data) !== "{}") {
            // build a query string with `action.data` (it's the place where reports
            // using a wizard to customize the output traditionally put their options)
            const options = encodeURIComponent(JSON.stringify(action.data));
            const contextParam = encodeURIComponent(JSON.stringify(actionContext));
            url += `?options=${options}&context=${contextParam}`;
        } else {
            if (actionContext.active_ids) {
                url += `/${actionContext.active_ids.join(",")}`;
            }
            if (type === "html") {
                const contextParam = encodeURIComponent(JSON.stringify(context));
                url += `?context=${contextParam}`;
            }
        }
        return url;
    }
    
    async function _triggerDownload(action, options, type) {
        const url = _getReportUrl(action, type);
        env.services.ui.block();
        try {
            await download({
                url: "/report/download",
                data: {
                    data: JSON.stringify([url, action.report_type]),
                    context: JSON.stringify(context),
                },
            });
        } catch (error) {
            console.error("Error downloading Excel report:", error);
            // Show user-friendly error message
            if (env.services.notification) {
                env.services.notification.add(
                    "Failed to generate Excel report. Please check the report configuration and try again.",
                    { type: "danger" }
                );
            }
        } finally {
            env.services.ui.unblock();
        }
        
        const onClose = options.onClose;
        if (action.close_on_report_download) {
            return env.services.action.doAction({ type: "ir.actions.act_window_close" }, { onClose });
        } else if (onClose) {
            onClose();
        }
    }
    
    if (action.report_type === 'excel') {
        return _triggerDownload(action, options, 'excel');
    }
});