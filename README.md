# Kickbase-Daily-Collector


This repository contains python code for collecting the Daily bonus using the Kickbase API.

Follow the guides below if you want to set everything up.

# How to setup

### Before you start

## Fork, GitHub workflow and GitHub pages

GitHub offers free execution of CI/CD workflows and publishing of pages for public repositories. This allows us to execute both the data collection code and the build process of the react web app on runners hosted by GitHub and also publish the website files free of charge. Below is a guide on how to set it up for yourself.

- **Create a fork of this repository:**
- **Setup repository secrets:** Those are needed for the execution of the workflows. The values will be masked in workflow logs, so no sensible data will get leaked at any time.
    - On the page of the forked repo go to 'Settings' -> 'Secrets and variables' -> 'Actions' and add the following secrets with their respective values by clicking on 'New repository secret':
        - **KB_MAIL** - The mail you use for logging into your Kickbase account
        - **KB_PW** - The password you use for logging into your Kickbase account
        
- **Enable workflows:** For new forks containing workflow definitions, workflows are disabled by default.
    - On the page of the forked repo go to 'Actions' and enable them by clicking on 'I understand my workflows, go ahead and enable them'.
    - Again under 'Action' select 'combined workflow' on the left side and click on 'Enable workflow' near the top right.
- **Run the workflow for the first time:**
    - On the page of the forked repo go to 'Actions' and select 'combined workflow' on the left side.
    - Click on 'Run workflow' -> 'Run workflow' to start the run.
    - Wait for the workflow to finish.
- **Scheduled runs:**
    - By default the collection is scheduled to run every day at 00:10.
    - This can be changed by adapting the value under 'cron' in the `./github/workflow.yml` file (https://crontab.guru/).


