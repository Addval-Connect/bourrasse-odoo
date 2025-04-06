# odoo-addval-modules

Modules with improovements and base configurations for Odoo implementations by Addval Connect

go to <https://www.odoo.sh/project/{PROJECT_NAME}/settings>

go to the submodules secction
    copy git@github.com:Addval-Connect/odoo-addval-modules.git
    paste it and click add

![Image Not Found](documentation/resources/SubmoduleOdooPermissions.png?raw=true "Optional Title")

copy the puclic key generated

go to Github.com: Settings ‣ Deploy keys ‣ Add deploy key

add the copied key

![Image Not Found](documentation/resources/GithubDeployKey.png?raw=true "Optional Title")

go to <https://www.odoo.sh/project/{PROJECT_NAME}/branches/{branch_name}/history>

click the submodules button on the top right

click the Run on Odoo.sh
![Image Not Found](documentation/resources/AddSubmoduleToBranch.png?raw=true "Optional Title")

Input the submodule information.

![Image Not Found](documentation/resources/InputSubmoduleData.png?raw=true "Optional Title")

click add submodule

update submodule in Odoo.sh

go the project git directory

run:

git submodule update --remote --merge

push changes

to initialize the submodule and clone it to the local repository

git submodule update --init --recursive

## Generación de factura a partir de xml

<https://github.com/odoo/enterprise/blob/bbc68dd2e73615711fe325c57dfaaaa4fbf0cca7/l10n_cl_edi/models/fetchmail_server.py>

### seleccion de diaro a partir de correo

    _get_dte_purchase_journal

    Selecciona el primer diaro de ventas de la empresa.

### Creación de factura a partir de xml

    _get_invoice_form

### Agregar l10n_cl_sii_regional_office and barcode

1. agregar campos al modelo l10n_cl_edi.account.move:
    * partner_sii_regional_office
    * partner_dte_resolution_number
    * partner_dte_resolution_date
2. modificar _get_invoice_form para que complete el campo del paso anterior y l10n_cl_sii_barcode, a partir de xml.
3. modificar addval_accounting.report_invoice para que use los campos del paso anterior.

***partner_dte_resolution_number and partner_dte_resolution_date are not in incoming xml!!!***
