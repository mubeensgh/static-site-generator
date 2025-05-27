REPO_NAME="static-site-generator"
echo "Building site for production with basepath: /${REPO_NAME}/"
python3 main.py "/${REPO_NAME}/"
echo "Production build completed for the 'docs/' directory."
