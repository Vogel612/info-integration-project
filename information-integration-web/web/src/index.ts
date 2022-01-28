import * as bs from 'bootstrap';
import './style/base.css';

import * as echarts from 'echarts';

import $ from 'jquery';

import api from './api';
import bodyRender from './views/index.hbs';
import animeCard from './views/template/anime_title.hbs';

import { histogram } from './visualization';
import { AnimeTitle } from './model/anime_title';

class DataProcess {
    data: AnimeTitle[];

    visContainer: HTMLElement;
    dataContainer: JQuery<HTMLElement>;

    dataTransform: (data: AnimeTitle[]) => [any, number][];
    chart;

    constructor(dataEl: JQuery<HTMLElement>, visEl: JQuery<HTMLElement>) {
        this.dataContainer = dataEl;
        this.visContainer = visEl.get()[0];

        this.dataTransform = DataProcess.byYear;
        this.chart = echarts.init(this.visContainer);
        this.resize();
    }

    public async update(this: DataProcess, data: AnimeTitle[]): Promise<void> {
        this.data = data;

        await Promise.all([
            this.render(),
            this.renderVis(),
        ]);
    }

    public async visualize(this: DataProcess, transform: (data: AnimeTitle[]) => [any, number][]): Promise<void> {
        this.dataTransform = transform;
        return this.renderVis();
    }

    public resize(this: DataProcess): void {
        this.chart.resize({
            width: this.visContainer.parentElement.clientWidth,
            height: 600,
        });
    }

    private async render(this: DataProcess): Promise<void> {
        this.dataContainer.children().remove();
        for (const t of this.data) {
            this.dataContainer.append(animeCard(t, {}));
        }
    }

    private async renderVis(this: DataProcess): Promise<void> {
        if (!this.data.length) {
            // FIXME clear chart
            return;
        }

        const dataset = this.dataTransform(this.data);
        let chartOptions = {
            dataset: [
                {
                    source: dataset,
                    sourceHeader: false,
                }],
            tooltip: {},
            xAxis: [{ type: 'category' }],
            yAxis: [{ type: 'value', scale: false }],
            series: {
                name: 'Number of Titles by Year',
                type: 'bar',
                barWidth: '98%',
                label: {
                    show: true,
                    position: 'top',
                }
            }
        };

        // @ts-ignore
        this.chart.setOption(chartOptions);
    }
    
    public static byYear(data: AnimeTitle[]): [number, number][] {
        // assume homogeneous data list
        const visualizationTarget = histogram<AnimeTitle, number>((t) => t.start_year)(data);
        return DataProcess.flattenObject(visualizationTarget);
    }

    public static byScore(data: AnimeTitle[]): [number, number][] {
        const visTarget = histogram<AnimeTitle, number>((t) => { return Math.ceil(t.score); })(data);
        return DataProcess.flattenObject(visTarget);
    }

    private static flattenObject(obj: {}): [any, number][] {
        const dataset: [any, number][]  = [];
        for (const [k, v] of Object.entries(obj)) {
            dataset.push([k as any, v as unknown as number]);
        }
        return dataset;
    }
}

function render() {
    let content = $(bodyRender({}, {}));
    $('body').children().remove();
    $('body').append(content);


    let dataHolder = new DataProcess($('#results', content), $('#vis-canvas', content));

    $(window).on('resize', () => {
        dataHolder.resize();
    });
    $('.collapse', content).each((_, el) => { let c = new bs.Collapse(el); });
    $('.collapse', content).on('shown.bs.collapse', () => dataHolder.resize());


    const namedVisualizations = [
        { name: "Score", title: "By Score", fn: DataProcess.byScore },
        { name: "Year", title: "By Year", fn: DataProcess.byYear },
    ];

    const visualizationNav = $('#vis-nav');
    for (const visNavItem of namedVisualizations) {
        const navItem = $(`<li class="nav-item"><a class="nav-link" href="#">${visNavItem.title}</a></li>`);
        navItem.on('click', async (evt) => {
            $(evt.currentTarget).siblings(".active").removeClass("active");
            $(evt.currentTarget).addClass("active");
            await dataHolder.visualize(visNavItem.fn);
        });
        visualizationNav.append(navItem);
    }
    visualizationNav.children().first().trigger("click");

    // default to a titles-between query for 1990 and 1995 to have a small-ish dataset for the initial load
    api.titlesBetween(1990, 1995).then(d => dataHolder.update(d));

    const interact: any = {};
    for (const key in api) {
        interact[key] = (...args: any) => {
            // @ts-ignore
            api[key].apply(api, args).then(d => dataHolder.update(d));
        }
    }
    // @ts-ignore
    window['interact'] = interact;
}

$(render)
