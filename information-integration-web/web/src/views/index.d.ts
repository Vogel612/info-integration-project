
declare module "*.hbs" {
    import { TemplateDelegate } from 'handlebars/runtime';

    const render: TemplateDelegate;
    export = render;
}
