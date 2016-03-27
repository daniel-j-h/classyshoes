from flask import Flask, request, render_template

from classyshoes.utils import mkQueryable


# Creates an endpoint closure over both model and queryable for dispatching user requests
def mkIndex(model, queryable):
    def index():
        matches = None
        articles = None

        if request.method == 'POST':
            positiveQuery = queryable(request.form.get('query-positive', ''))
            negativeQuery = queryable(request.form.get('query-negative', ''))

            if not positiveQuery and not negativeQuery:
                return render_template('index.html')

            matches = model.most_similar(positiveQuery, negativeQuery, topn=10)

            positiveDocVec = model.infer_vector(positiveQuery)
            negativeDocVec = model.infer_vector(negativeQuery)

            articles = model.docvecs.most_similar([positiveDocVec], [negativeDocVec], topn=10)

        return render_template('index.html', **locals())

    return index


# Simple local HTTP server for querying results more easily
def mkHttpd(model, language):
    httpd = Flask(__name__)

    index = mkIndex(model, mkQueryable(language))
    httpd.add_url_rule('/', view_func=index, methods=['GET', 'POST'])

    return httpd
