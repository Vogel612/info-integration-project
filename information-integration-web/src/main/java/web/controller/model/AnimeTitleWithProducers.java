package web.controller.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class AnimeTitleWithProducers extends AnimeTitle {
    @JsonProperty("producers")
    private List<String> producers;

    public AnimeTitleWithProducers(int id, String title, int duration, int numberOfEpisodes, String mediaType, float score, String source, int startYear, int finishYear, String seasonOfRelease, List<String> producers) {
        super(id, title, duration, numberOfEpisodes, mediaType, score, source, startYear, finishYear, seasonOfRelease);
        this.producers = producers;
    }

    public List<String> getProducers() {
        return producers;
    }

    public void setProducers(List<String> producers) {
        this.producers = producers;
    }
}
