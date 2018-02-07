
EXTRA_TAURUS_PATHS="/home/guler/.local/lib/python2.7/site-packages/maxwidgets/input /home/guler/.local/lib/python2.7/site-packages/maxwidgets/panel /home/guler/.local/lib/python2.7/site-packages/maxwidgets/display /home/guler/.local/lib/python2.7/site-packages/maxwidgets/extra_guiqwt"

for path in $EXTRA_TAURUS_PATHS; do
    if ! echo $TAURUSQTDESIGNERPATH | grep -q $path; then
        TAURUSQTDESIGNERPATH=$path:$TAURUSQTDESIGNERPATH
    fi
done

export TAURUSQTDESIGNERPATH
