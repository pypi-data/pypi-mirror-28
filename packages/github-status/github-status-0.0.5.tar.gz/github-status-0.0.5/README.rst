``github-status``
-----------------
A simple interface for updating SHA1s for PRs with statuses. Made for Jenkins
initially, altough a command line tool, it mostly consumes environment
variables to set states on commits.

Github Environment Variables:

*  ``GITHUB_REPOSITORY``       The url part of the repo, like ceph/ceph
*  ``GITHUB_SHA``              A commit SHA that will receive the update
*  ``GITHUB_OAUTH_TOKEN``      Generated TOKEN to authenticate to Github
*  ``GITHUB_STATUS_CONTEXT``   The "title" part of the status, like "docs"
*  ``GITHUB_STATUS_STARTED``   The 'started' text that will change next to the 'title' (context)
*  ``GITHUB_STATUS_SUCCESS``   The 'success' text that will change next to the 'title' (context)
*  ``GITHUB_STATUS_FAILURE``   The 'failure' text that will change next to the 'title' (context)
*  ``GITHUB_STATUS_ERROR``     The 'error' text that will change next to the 'title' (context)
*  ``GITHUB_STATUS_STATE``     The state for the sha1, one of: 'success', 'error', 'failure', or 'pending'

Build Environment Variables:

* ``BUILD_URL``               A url that points to the actual full url for the build
* ``PARENT_BUILD_URL``        Optional parent url where actual build happened
