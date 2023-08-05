import {escapeText} from "../common"

export let searchApiTemplate = () =>
`<div id="bibimport-api-search" title="${gettext("Search bibliography databases")}">
        <p>
            <input id="bibimport-search-text" class="linktitle" type="text" value=""
                    placeholder="${gettext("Title, Author, DOI, etc.")}"/>
            <button id="bibimport-search-button" class="fw-button fw-dark" type="button">
                ${gettext("search")}
            </button>
        </p>
        <div id="bibimport-search-header"></div>
        <div id="bibimport-search-result-gesis" class="bibimport-search-result"></div>
        <div id="bibimport-search-result-datacite" class="bibimport-search-result"></div>
        <div id="bibimport-search-result-crossref" class="bibimport-search-result"></div>
</div>`

export let searchApiResultGesisTemplate = ({items}) => {
    return '<h3>GESIS Search</h3>' +
        items.map(item =>
            `<div class="item">
                <button type="button"
                        class="api-import fw-button fw-orange fw-small"
                        data-id="${item.id}"
                        data-type="${item.type}"
                >
                    ${gettext('Import')}
                </button>
                ${
                    item.title ?
                    `<h3>
                        ${escapeText(item.title)}
                    </h3>` :
                    ''
                }
                ${
                    item.person && item.person.length ?
                    `<p>
                        <b>${gettext('Author(s)')}:</b>
                        ${item.person.join("; ")}
                    </p>` :
                    ''
                }
                ${
                    item.date ?
                    `<p><b>${gettext('Published')}:</b> ${item.date}</p>` :
                    ''
                }
                ${
                    item.abstract ?
                    `<p>
                        ${
                            item.abstract.length < 200 ?
                            escapeText(item.abstract) :
                            escapeText(item.abstract.substring(0, 200)) + "..."
                        }
                    </p>` :
                    ''
                }
            </div>`
        ).join('')
}

export let searchApiResultDataciteTemplate = ({items}) => {
    return '<h3>Datacite</h3>' +
        items.map(item =>
            `<div class="item">
                <button type="button" class="api-import fw-button fw-orange fw-small"
                        data-doi="${item.doi}">
                    ${gettext('Import')}
                </button>
                <h3>
                    ${escapeText(item.title)}
                </h3>
                ${
                    item.author ?
                    `<p>
                        <b>${gettext('Author(s)')}:</b>
                        ${
                            item.author.map(author =>
                                 author.literal ?
                                 author.literal :
                                 `${author.family} ${author.given}`
                             ).join(", ")
                         }
                    </p>` :
                    ''
                }
                ${
                    item.published ?
                    `<p><b>${gettext('Published')}:</b> ${item.published}</p>` :
                    ''
                }
                ${
                    item.doi ?
                    `<p><b>DOI:</b> ${item.doi}</p>` :
                    ''
                }
                ${
                    item.description ?
                    `<p>
                        ${
                            item.description.length < 200 ?
                            escapeText(item.description) :
                            escapeText(item.description.substring(0, 200)) + "..."
                        }
                    </p>` :
                    ''
                }
            </div>`
        ).join('')
    }


export let searchApiResultCrossrefTemplate = ({items}) => {
    return '<h3>Crossref</h3>' +
        items.map(item =>
            `<div class="item">
                <button type="button" class="api-import fw-button fw-orange fw-small"
                        data-doi="${item.doi.replace('https://dx.doi.org/','')}">
                    ${gettext('Import')}
                </button>
                <h3>
                    ${
                        item.fullCitation ?
                        item.fullCitation :
                        `${item.title} ${item.year}`
                    }
                </h3>
                ${
                    item.doi ?
                    `<p><b>DOI:</b> ${item.doi}</p>` :
                    ''
                }
                ${
                    item.description ?
                    `<p>
                        ${
                            item.description.length < 200 ?
                            escapeText(item.description) :
                            escapeText(item.description.substring(0, 200)) + "..."
                        }
                    </p>` :
                    ''
                }
            </div>`
        ).join('')

}
