cd "${INSTALLDIR}/${NAME}/iogt/"
manage="${VENV}/bin/python ${INSTALLDIR}/${NAME}/iogt/manage.py"

$manage migrate --settings=iogt.settings.production

# process static files
$manage compress --settings=iogt.settings.production
$manage collectstatic --noinput --settings=iogt.settings.production

# compile i18n strings
$manage compilemessages --settings=iogt.settings.production
