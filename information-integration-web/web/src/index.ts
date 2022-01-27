import * as bs from 'bootstrap';
import './style/base.css';

import * as echarts from 'echarts';

import $ from 'jquery';

import api from './api';
import bodyRender from './views/index.hbs';
import animeCard from './views/template/anime_title.hbs';
import { histogram } from './visualization';

class DataProcess {
    data: AnimeTitle[];

    visContainer: HTMLElement;
    dataContainer: JQuery<HTMLElement>;
    chart;

    constructor(dataEl: JQuery<HTMLElement>, visEl: JQuery<HTMLElement>) {
        this.dataContainer = dataEl;
        this.visContainer = visEl.get()[0];

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

        // assume homogeneous data list
        const visualizationTarget = histogram<AnimeTitle, number>((t) => t.start_year)(this.data);
        const dataset = [];
        for (const [k, v] of Object.entries(visualizationTarget)) {
            dataset.push([k, v]);
        }

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
}

function render() {
    let content = $(bodyRender({}, {}));
    $('body').children().remove();
    $('body').append(content);


    let dataHolder = new DataProcess($('#results', content), $('#vis-canvas', content));
    // api.allTitles().then(d => dataHolder.update(d));
    api.titlesBetween(1990, 1995).then(d => dataHolder.update(d));

    $(window).on('resize', () => {
        dataHolder.resize();
    });
    $('.collapse', content).each((_, el) => { let c = new bs.Collapse(el); });
    $('.collapse', content).on('shown.bs.collapse', () => dataHolder.resize());
}

$(render)
