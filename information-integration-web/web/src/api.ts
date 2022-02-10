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
}

export default new Api()
