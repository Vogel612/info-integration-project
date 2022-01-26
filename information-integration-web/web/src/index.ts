import 'bootstrap';
import './style/base.css';

import api from './api';
import bodyRender from './views/index.hbs';

document.body.innerHTML = bodyRender({}, {});

api.allTitles()
    .then(titles => {
        for (const t of titles) {
            console.log(t['title']);
        }
    });
