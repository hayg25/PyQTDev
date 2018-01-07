
EXTRA_TAURUS_PATHS="/usr/local/lib/python2.7/dist-packages/maxwidgets/input /usr/local/lib/python2.7/dist-packages/maxwidgets/panel /usr/local/lib/python2.7/dist-packages/maxwidgets/display /usr/local/lib/python2.7/dist-packages/maxwidgets/extra_guiqwt"

for path in $EXTRA_TAURUS_PATHS; do
    if ! echo $TAURUSQTDESIGNERPATH | grep -q $path; then
        TAURUSQTDESIGNERPATH=$path:$TAURUSQTDESIGNERPATH
    fi
done

export TAURUSQTDESIGNERPATH
