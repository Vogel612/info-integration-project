import * as handlebars from 'handlebars/runtime';

let pc = require('./views/index.hbs');

document.body.append(pc({}));
