# bourrase-odoo

## Clone Repository in local directory

* create a new directory for the proyect
* cd into the directory with the terminal
* execute the following command:

    ~~~Bash
    git clone --recurse-submodules https://github.com/Addval-Connect/bourrasse-odoo.git
    ~~~

## Push changes to staging

* checkout to the staging branch Altiplano-Staging

    ~~~Bash
    git checkout Altiplano-Staging
    ~~~

* Make the necesary changes
* Commit the changes to the submoduels, if any:

    ~~~Bash
    cd <submodule/path>
    git add .
    git commit -m "Commit message"
    ~~~

* Push the changes from the submodules:

    ~~~Bash
    cd <submodule/path>
    git push
    ~~~

* Comit the version change and other changes to the staging branch:

    ~~~Bash
    git add .
    git commit -m "Commit message"
    ~~~

* Push the changes to the staging branch:

    ~~~Bash
    git push
    ~~~

## Merge changes to production

### Drag and drop the staging branch to the production branch

* go to <https://www.odoo.sh/project/{PROJECT_NAME}/branches/{BRANCH_NAME}/history>
* drag and drop the staging branch to the production branch:

    ![Image Not Found](documentation\resources\OdooDragMerge.png?raw=true "Optional Title")

* select merge:
    ![Image Not Found](documentation\resources\OdooDragMergeSelect.png?raw=true "Optional Title")

### Manual Git commands

If the previous steps did not work, you can use the following commands to merge the changes to the production branch:

* checkout to the production branch main

    ~~~Bash
    git checkout main
    ~~~

* make sure the commit of the submodules in the main branch is the same as in the staging branch:

* merge the changes from the staging branch to the main branch:

    ~~~Bash
    git merge Altiplano-Staging
    ~~~

* Push the changes to the production branch:

    ~~~Bash
    git push
    ~~~

## Reflect module changes in odoo.sh

* go to <https://www.odoo.sh/project/{PROJECT_NAME}/branches/{BRANCH_NAME}/history>

* Connect to the database:

    ![Image Not Found](documentation\resources\ConnectOdooDatabase.png?raw=true "Optional Title")

* Go to the applications module:

    ![Image Not Found](documentation\resources\OdooApps.png?raw=true "Optional Title")

* Search for your desired application and update it:

    ![Image Not Found](documentation\resources\OdooUpdateModule.png?raw=true "Optional Title")
