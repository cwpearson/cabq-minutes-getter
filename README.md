# cabq-minutes-getter

A python script that uses a combination of the City of Albuquerque public calender RSS feed and a bit of HTML parsing to download the PDF of the minutes for each City Council Meeting.

## Github Action

The action is set to run periodically.
It clones https://github.com/cwpearson/cabq-minutes, downloads any new PDFs it discovers from the City of Albuquerque website, and then pushes the results back up.

Deployment is done to https://github.com/cwpearson/cabq-minutes.
An SSH keypair was generated - the public key was added to https://github.com/cwpearson, and the private key as a repository secret to https://github.com/cwpearson/cabq-minutes-getter.
This private key is used by the github action to authenticate with github to push the results to https://github.com/cwpearson/cabq-minutes.

