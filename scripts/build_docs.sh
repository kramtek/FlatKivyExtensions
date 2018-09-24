

package=$1
version=$2


# TODO: have to copy garden packages locally because running under
#       sphinx does not handle importing from kivy.garden....
if [ -z "$version" ]; then
    version="source"
fi

if [ -z "${package}" ]; then
    echo "You must specify the package name as the first argument"
    exit 
fi

echo "version: " $version

sphinx_src="sphinxsrc"
sphinx_tmp="sphinxsrc_outupt"
sphinx_output="doc"

rm -rf ${sphinx_output}
rm -rf ${sphinx_tmp}

cp -r ${sphinx_src} ${sphinx_tmp}

cp ${sphinx_tmp}/index_base ${sphinx_tmp}/index.rst

# 
# Modify base rst files
#
cd ${sphinx_tmp}
# clear out previously generated rst files
rm ${package}.*

# Apply date and version to rst file
DATE=`date +%Y-%m-%d`
sed -i ".bak" "s/__ver__/${version}/g" index.rst
sed -i ".bak" "s/__date__/${DATE}/g" index.rst

cd ..

export KIVY_DOC=1
export KIVY_DOC_INCLUDE=1

#
# Run apidoc and apply modifications to the generated
# rst files
#
sphinx-apidoc -f -e -o ${sphinx_tmp} ${package}  ${package}/tests ${package}/third_party
# ${package}/screens ${package}/uix

python ${sphinx_tmp}/modify_rst.py ${sphinx_tmp}/${package}.rst
mv ${sphinx_tmp}/${package}.rst.new ${sphinx_tmp}/${package}.rst

sphinx-build -b html ${sphinx_tmp} ${sphinx_output}/ 

# Clean out temporary files
rm -rf ${sphinx_tmp}

