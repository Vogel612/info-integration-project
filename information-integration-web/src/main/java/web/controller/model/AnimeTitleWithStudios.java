package web.controller.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class AnimeTitleWithStudios extends AnimeTitle {
    @JsonProperty("producers")
    private List<String> studios;

    public AnimeTitleWithStudios(int id, String title, int duration, int numberOfEpisodes, String mediaType, float score, String source, int startYear, int finishYear, String seasonOfRelease, List<String> studios) {
        super(id, title, duration, numberOfEpisodes, mediaType, score, source, startYear, finishYear, seasonOfRelease);
        this.studios = studios;
    }

    public List<String> getStudios() {
        return studios;
    }

    public void setStudios(List<String> studios) {
        this.studios = studios;
    }
}
