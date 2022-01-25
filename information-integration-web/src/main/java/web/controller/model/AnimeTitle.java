package web.controller.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AnimeTitle {
    @JsonProperty
    private int id;
    @JsonProperty
    private String title;
    @JsonProperty
    private int duration;
    @JsonProperty("number_of_episodes")
    private int numberOfEpisodes;
    @JsonProperty("media_type")
    private String mediaType;
    @JsonProperty
    private float score;
    @JsonProperty
    private String source;
    @JsonProperty("start_year")
    private int startYear;
    @JsonProperty("finish_year")
    private int finishYear;
    @JsonProperty("season_of_release")
    private String seasonOfRelease;
    @JsonProperty("content_warnings")
    private String[] contentWarnings;
    @JsonProperty("genres")
    private String[] genres;
    @JsonProperty("producers")
    private String[] producers;
    @JsonProperty("studios")
    private String[] studios;

    public AnimeTitle(
            int id, String title, int duration, int numberOfEpisodes,
            String mediaType, float score, String source,
            int startYear, int finishYear, String seasonOfRelease,
            String[] contentWarnings, String[] genres, String[] producers, String[] studios) {
        this.id = id;
        this.title = title;
        this.duration = duration;
        this.numberOfEpisodes = numberOfEpisodes;
        this.mediaType = mediaType;
        this.score = score;
        this.source = source;
        this.startYear = startYear;
        this.finishYear = finishYear;
        this.seasonOfRelease = seasonOfRelease;
        this.contentWarnings = contentWarnings;
        this.genres = genres;
        this.producers = producers;
        this.studios = studios;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public int getDuration() {
        return duration;
    }

    public void setDuration(int duration) {
        this.duration = duration;
    }

    public int getNumberOfEpisodes() {
        return numberOfEpisodes;
    }

    public void setNumberOfEpisodes(int numberOfEpisodes) {
        this.numberOfEpisodes = numberOfEpisodes;
    }

    public String getMediaType() {
        return mediaType;
    }

    public void setMediaType(String mediaType) {
        this.mediaType = mediaType;
    }

    public float getScore() {
        return score;
    }

    public void setScore(float score) {
        this.score = score;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public int getStartYear() {
        return startYear;
    }

    public void setStartYear(int startYear) {
        this.startYear = startYear;
    }

    public int getFinishYear() {
        return finishYear;
    }

    public void setFinishYear(int finishYear) {
        this.finishYear = finishYear;
    }

    public String getSeasonOfRelease() {
        return seasonOfRelease;
    }

    public void setSeasonOfRelease(String seasonOfRelease) {
        this.seasonOfRelease = seasonOfRelease;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String[] getGenres() {
        return genres;
    }

    public void setGenres(String[] genres) {
        this.genres = genres;
    }

    public String[] getContentWarnings() {
        return contentWarnings;
    }

    public void setContentWarnings(String[] contentWarnings) {
        this.contentWarnings = contentWarnings;
    }

    public String[] getProducers() {
        return producers;
    }

    public void setProducers(String[] producers) {
        this.producers = producers;
    }

    public String[] getStudios() {
        return studios;
    }

    public void setStudios(String[] studios) {
        this.studios = studios;
    }
}
