#! /bin/bash

set -eou pipefail

cat <<EOF >key.priv
$CABQ_MINUTES_KEY
EOF
chmod 600 key.priv
export GIT_SSH_COMMAND="ssh -i $(realpath key.priv)"

CABQ_MINUTES_REMOTE="git@github.com:cwpearson/cabq-minutes.git"

set -x 


if [ -d "$CABQ_MINUTES_DIR" ]; then
    (cd "$CABQ_MINUTES_DIR"; git pull)
else
    git clone "$CABQ_MINUTES_REMOTE" "$CABQ_MINUTES_DIR"
fi

(
cd "$CABQ_MINUTES_DIR"
git pull
git config user.name "cabq-minutes-getter"
git config user.email "0-cwpearson@users.noreply.github.com"
git remote -v
)
