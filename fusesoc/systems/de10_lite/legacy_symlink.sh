LEGACY_DIR=$BUILD_ROOT/src/de10_lite
DIR=$BUILD_ROOT/src/de10_lite_0
echo $LEGACY_DIR
echo $DIR
[ -d $LEGACY_DIR ] && ln -s $LEGACY_DIR $DIR
