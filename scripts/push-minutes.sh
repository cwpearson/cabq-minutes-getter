#! /bin/bash

set -eou pipefail

cat <<EOF >key.priv
$CABQ_MINUTES_KEY
EOF
chmod 600 key.priv
export GIT_SSH_COMMAND="ssh -i $(realpath key.priv)"

set -x 

cd $CABQ_MINUTES_DIR
git add *
git commit -m "$(date)" || echo "No updates"
git remote -v
git push
