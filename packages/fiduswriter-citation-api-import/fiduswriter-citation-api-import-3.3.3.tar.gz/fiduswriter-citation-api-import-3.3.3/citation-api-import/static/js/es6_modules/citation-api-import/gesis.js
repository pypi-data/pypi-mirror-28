import {
    searchApiResultGesisTemplate
} from "./templates"

export class GesisSearcher {

    constructor(importer) {
        this.importer = importer
    }

    bind() {
        [].slice.call(
            document.querySelectorAll('#bibimport-search-result-gesis .api-import')
        ).forEach(resultEl => {
            let id = resultEl.dataset.id,
                type = resultEl.dataset.type
            resultEl.addEventListener('click', () => this.getBibtex(id, type))
        })
    }

    lookup(searchTerm) {

        let searchQuery = {
            "query": {
                "bool": {
                    "must": [{
                        "query_string": {
                            "query": searchTerm
                        }
                    }],
                    "should": [ // We only search types which make sense to cite.
                        {
                            "term": {
                                "type": "publication"
                            }
                        },
                        {
                            "term": {
                                "type": "research_data"
                            }
                        },
                        {
                            "term": {
                                "type": "instruments_tools"
                            }
                        },
                        {
                            "term": {
                                "type": "gesis_bib"
                            }
                        }
                    ],
                    "minimum_should_match": 1
                }
            }
        }

        return fetch(`https://search.gesis.org/searchengine?source=${encodeURI(JSON.stringify(searchQuery))}`, {
            method: "GET"
        }).then(
        response => response.json()
    ).then(json => {
        let items = json.hits && json.hits.hits ? json.hits.hits.map(hit => hit._source) : []
        let searchEl = document.getElementById('bibimport-search-result-gesis')
        if (!searchEl) {
            // window was closed before result was ready.
            return
        }
        if (items.length) {
            searchEl.innerHTML = searchApiResultGesisTemplate({
                items
            })
        } else {
            searchEl.innerHTML = ''
        }
        this.bind()
    })
}

getBibtex(id, type) {
    fetch(`/proxy/citation-api-import/https://search.gesis.org/ajax/bibtex.php?type=${type}&docid=${id}&download=true`, {
        method: "GET",
        credentials: "same-origin"
    }).then(
        response => response.text()
    ).then(
        bibtex => this.importer.importBibtex(bibtex)
    )
}

}
