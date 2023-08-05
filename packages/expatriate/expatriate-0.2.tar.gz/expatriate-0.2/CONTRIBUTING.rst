Introduction
============

First off, thank you for considering contributing to expatriate. It's
people like you that make expatriate such a great tool.

Following these guidelines helps to communicate that you respect the
time of the developers managing and developing this open source project.
In return, they should reciprocate that respect in addressing your
issue, assessing changes, and helping you finalize your pull requests.

Expatriate is an open source project and we love to receive
contributions from our community — you! There are many ways to
contribute, from writing tutorials or blog posts, improving the
documentation, submitting bug reports and feature requests or writing
code which can be incorporated into expatriate itself.

Please, don't use the issue tracker for support questions; please keep
it to issues with the code.

Ground Rules
============

Responsibilities \* Ensure cross-platform compatibility for every change
that's accepted. \* Ensure that code that goes into core meets all
requirements in the `Pull Request
Checklist <https://github.com/cjaymes/expatriate/wiki/Pull-Request-Checklist>`__
\* Create issues for any major changes and enhancements that you wish to
make. Discuss things transparently and get community feedback. \* Don't
add any classes to the codebase unless absolutely needed. Err on the
side of using functions. \* Keep feature versions as small as possible,
preferably one new feature per version. \* Be welcoming to newcomers and
encourage diverse new contributors from all backgrounds. See the `Code
of
Conduct <https://github.com/cjaymes/expatriate/tree/master/CODE_OF_CONDUCT.md>`__.

1. Where do I go from here?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you've noticed a bug `search the issue
tracker <https://github.com/cjaymes/expatriate/issues>`__ to see if
someone else in the community has already created a ticket. If not, go
ahead and `make
one <https://github.com/cjaymes/expatriate/issues/new>`__!

2. Fork & create a branch
~~~~~~~~~~~~~~~~~~~~~~~~~

If this is something you think you can fix, then
`fork <https://help.github.com/articles/fork-a-repo>`__ and create a
branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're
working on):

.. code:: sh

    git checkout -b 325-add-japanese-translations

3. Get the test suite running
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure you're using a recent python (3.5+) and have the requirements
from requirements.txt installed.

.. code:: sh

    pip install -r requirements.txt

Now you should be able to run the test suite using:

.. code:: sh

    pytest -vv

If the tests are failing, you might want to clean your environment:

.. code:: sh

    find tests -name '*.pyc' -delete

4. Did you find a bug?
~~~~~~~~~~~~~~~~~~~~~~

-  **Ensure the bug was not already reported** by `searching all
   issues <https://github.com/cjaymes/expatriate/issues?q=>`__.

-  If you're unable to find an open issue addressing the problem, `open
   a new one <https://github.com/cjaymes/expatriate/issues/new>`__. Be
   sure to include a **title and clear description**, as much relevant
   information as possible, and a **code sample** or an **the failing
   test case** demonstrating the expected behavior that is not
   occurring.

5. Implement your fix or feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At this point, you're ready to make your changes! Feel free to ask for
help; everyone is a beginner at first :smile\_cat:

6. Re-run the tests
~~~~~~~~~~~~~~~~~~~

Wash and repeat.

7. Make a Pull Request
~~~~~~~~~~~~~~~~~~~~~~

At this point, you should switch back to your master branch and make
sure it's up to date with expatriate's master branch:

.. code:: sh

    git remote add upstream git@github.com:cjaymes/expatriate.git
    git checkout master
    git pull upstream master

Then update your feature branch from your local copy of master, and push
it!

.. code:: sh

    git checkout 325-add-japanese-translations
    git rebase master
    git push --set-upstream origin 325-add-japanese-translations

Finally, go to GitHub and `make a Pull
Request <https://help.github.com/articles/creating-a-pull-request>`__ :D

8. Keeping your Pull Request updated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a maintainer asks you to "rebase" your PR, they're saying that a lot
of code has changed, and that you need to update your branch so it's
easier to merge.

To learn more about rebasing in Git, there are a lot of
`good <http://git-scm.com/book/en/Git-Branching-Rebasing>`__
`resources <https://help.github.com/articles/interactive-rebase>`__, but
here's the suggested workflow:

.. code:: sh

    git checkout 325-add-japanese-translations
    git pull --rebase upstream master
    git push --force-with-lease 325-add-japanese-translations

9. Merging a PR (maintainers only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A PR should only be merged into master by a maintainer by following the
`Pull Request
Checklist <https://github.com/cjaymes/expatriate/wiki/Pull-Request-Checklist>`__

Any maintainer is allowed to merge a PR if all of these conditions are
met.
