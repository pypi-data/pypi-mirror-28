.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


|




Install
```````


.. code:: bash

	`[sudo] pip install gitmsg`






Examples
````````


.. code:: bash

	$ cd /path/to/repo/
	$ touch new_file
	$ rm deleted_file
	$ echo "new" > modified_file
	$ git add -A
	$ gitmsg
	'+new_file; -deleted_file; ^modified_file'





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/russianidiot/gitmsg.sh.cli.svg
	:target: https://github.com/russianidiot/gitmsg.sh.cli/issues

