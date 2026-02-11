# dsd-scalingo

A plugin for deploying Django projects to Scalingo, using django-simple-deploy.

For full documentation, see the documentation for [django-simple-deploy](https://django-simple-deploy.readthedocs.io/en/latest/).

Current status
---

This plugin is in a pre-1.0 development phase. Scalingo has one of the best free trial plans in the industry, so this plugin will be prioritized and should move forward quickly.

Fully automated deployment
---

- Install the Scalingo CLI.
- Upload your SSH public key to Scalingo.
- Run the following commands:
```sh
$ scalingo login
$ pip install dsd-scalingo
# Add django_simple_deploy to INSTALLED_APPS.
$ python manage.yp deploy --automate-all
```

Your deployed project should appear in a new browser tab.

Destroying a project
---

If you're doing a test deployment and want to destroy your project:

```sh
$ scalingo --app <app-name> destroy
```
