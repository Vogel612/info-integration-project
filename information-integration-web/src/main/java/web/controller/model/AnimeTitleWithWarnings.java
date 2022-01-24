package web.controller.model;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public class AnimeTitleWithWarnings extends AnimeTitle {
    @JsonProperty("warning")
    private List<String> warnings;

    public AnimeTitleWithWarnings(int id, String title, int duration, int numberOfEpisodes, String mediaType, float score, String source, int startYear, int finishYear, String seasonOfRelease, List<String> warnings) {
        super(id, title, duration, numberOfEpisodes, mediaType, score, source, startYear, finishYear, seasonOfRelease);
        this.warnings = warnings;
    }

    public List<String> getWarnings() {
        return warnings;
    }

    public void setWarnings(List<String> warnings) {
        this.warnings = warnings;
    }
}
