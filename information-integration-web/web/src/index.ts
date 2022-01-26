import * as bs from 'bootstrap';
import './style/base.css';

import $ from 'jquery';

import api from './api';
import bodyRender from './views/index.hbs';
import animeCard from './views/template/anime_title.hbs';

document.body.innerHTML = bodyRender({}, {});


let collapseElementList = [].slice.call(document.querySelectorAll('.collapse'))
collapseElementList.map((el: any) => new bs.Collapse(el))

api.allTitles()
    .then(titles => {
        const resultContainer = $('#results');
        resultContainer.children().remove();
        for (const t of titles) {
            resultContainer.append(animeCard(t, {}));
        }
    });
