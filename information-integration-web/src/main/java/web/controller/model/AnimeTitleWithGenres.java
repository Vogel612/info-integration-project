package web.controller.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class AnimeTitleWithGenres extends AnimeTitle {
    @JsonProperty("genres")
    private List<String> genres;

    public AnimeTitleWithGenres(int id, String title, int duration, int numberOfEpisodes, String mediaType, float score, String source, int startYear, int finishYear, String seasonOfRelease, List<String> genres) {
        super(id, title, duration, numberOfEpisodes, mediaType, score, source, startYear, finishYear, seasonOfRelease);
        this.genres = genres;
    }

    public List<String> getGenres() {
        return genres;
    }

    public void setGenres(List<String> genres) {
        this.genres = genres;
    }
}
