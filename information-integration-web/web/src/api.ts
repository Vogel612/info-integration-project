import { AnimeTitle } from "./model/anime_title";

export class Api {
    base: string;

    constructor(baseUrl: string = "api") {
        this.base = baseUrl;
    }

    async allTitles(this: Api): Promise<AnimeTitle[]> {
        return fetch(`${this.base}/titles/`, {
            method: 'GET',
        }).then(response => {
            if (response.ok) {
                return response.json() as unknown as AnimeTitle[];
            } else {
                throw "Response was not OK";
            }
        });
    }

    async ranked(this: Api): Promise<AnimeTitle[]> {
        return fetch(`${this.base}/titles/`, {
            method: 'GET',
        }).then(response => {
            if (response.ok) {
                return response.json() as unknown as AnimeTitle[];
            } else {
                throw "Response was not OK";
            }
        });
    }

    async titlesBetween(this: Api, startYear: number, endYear: number = 2030): Promise<AnimeTitle[]> {
        return fetch(`${this.base}/titles/by_year?from=${startYear}&to=${endYear}`, {
            method: 'GET',
        }).then(r => {
            if (!r.ok) {
                throw "Response was not OK";
            }
            return r.json() as unknown as AnimeTitle[];
        });
    }

    async withoutContentWarnings(this: Api, cws: string[]): Promise<AnimeTitle[]>  {
        return fetch(`${this.base}/titles/warning?warning=${cws.join(',')}`, {
            method: 'GET',
        }).then(r => {
            if (!r.ok) {
                throw "Response was not OK";
            }
            return r.json() as unknown as AnimeTitle[];
        });
    }

    async byGenre(this: Api, genre: string): Promise<AnimeTitle[]> {
        return fetch(`${this.base}/titles/by_genre?genre=${genre}`, {
            method: 'GET',
        }).then(r => {
            if (!r.ok) {
                throw "Response was not OK";
            }
            return r.json() as unknown as AnimeTitle[];
        });
    }

    async byProducer(this: Api, producer: string): Promise<AnimeTitle[]> {
        return fetch(`${this.base}/titles/by_producer?producer=${producer}`, {
            method: 'GET',
        }).then(r => {
            if (!r.ok) {
                throw "Response was not OK";
            }
            return r.json() as unknown as AnimeTitle[];
        });
    }

    async byStudio(this: Api, studio: string): Promise<AnimeTitle[]> {
        return fetch(`${this.base}/titles/by_studio?studio=${studio}`, {
            method: 'GET',
        }).then(r => {
            if (!r.ok) {
                throw "Response was not OK";
            }
            return r.json() as unknown as AnimeTitle[];
        });
    }

    async undiscovered(this: Api): Promise<AnimeTitle[]> {
        return fetch(`${this.base}/titles/undiscovered`, {
            method: 'GET',
        }).then(r => {
            if (!r.ok) {
                throw "Response was not OK";
            }
            return r.json() as unknown as AnimeTitle[];
        });
    }

    async duration(this: Api, duration: number, episodes: number): Promise<AnimeTitle[]> {
        return fetch(`${this.base}/titles/duration_not_more?duration=${duration}&episodes=${episodes}`, {
            method: 'GET',
        }).then(r => {
            if (!r.ok) {
                throw "Response was not OK";
            }
            return r.json() as unknown as AnimeTitle[];
        });
    }
}

export default new Api()
