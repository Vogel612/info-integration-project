import * as bs from 'bootstrap';
import './style/base.css';

import api from './api';
import bodyRender from './views/index.hbs';

document.body.innerHTML = bodyRender({}, {});


let collapseElementList = [].slice.call(document.querySelectorAll('.collapse'))
collapseElementList.map((el: any) => new bs.Collapse(el))

api.allTitles()
    .then(titles => {
        for (const t of titles) {
            console.log(t['title']);
        }
    });
