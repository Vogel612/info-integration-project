import * as bs from 'bootstrap';
import './style/base.css';

import * as d3 from 'd3';
import $ from 'jquery';

import api from './api';
import bodyRender from './views/index.hbs';
import animeCard from './views/template/anime_title.hbs';

function render() {
    let content = $(bodyRender({}, {}));
    $('body').children().remove();
    $('body').append(content);

    $('.collapse', content).each((_, el) => { new bs.Collapse(el) });

    api.allTitles()
        .then(titles => {
            const resultContainer = $('#results');
            resultContainer.children().remove();
            for (const t of titles) {
                resultContainer.append(animeCard(t, {}));
            }
        });
}

$(render)
