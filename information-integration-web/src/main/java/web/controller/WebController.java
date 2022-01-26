package web.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import web.controller.model.*;
import web.repository.AnimeRepository;

import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@RestController
public class WebController {

    @Autowired
    private AnimeRepository repository;

    @GetMapping("api/titles")
    public List<AnimeTitle> titles() {
        return repository.getAllTitles();
    }

    @GetMapping("api/titles/ranked")
    public List<AnimeTitle> titlesRanked() {
        return repository.getTitlesRanked();
    }

    @GetMapping("api/title/synopsis")
    public String titleSynopsis(@RequestParam int id) {
        return repository.getTitleSynopsis(id);
    }

    @GetMapping("api/titles/by_year")
    public List<AnimeTitle> titlesByYears(
            @RequestParam(value = "from", defaultValue = "0") int from,
            @RequestParam(value = "to", defaultValue = "2030") int to
    ) {
        return repository.getTitlesByYear(from, to);
    }

    @GetMapping("api/titles/warning")
    public List<AnimeTitle> titlesWithoutContentWarnings(@RequestParam String warning) {
        Set<String> warnings = Arrays.stream(warning.split(",")).collect(Collectors.toSet());
        return repository.getTitlesWithoutContentWarnings(warnings);
    }

    @GetMapping("api/titles/by_genre")
    public List<AnimeTitle> titlesByGenre(@RequestParam("genre") String genre) {
        return repository.getTitlesByGenre(genre);
    }

    @GetMapping("api/titles/by_producer")
    public List<AnimeTitle> titlesByProducer(@RequestParam("producer") String producer) {
        return repository.getTitlesByProducer(producer);
    }

    @GetMapping("api/titles/by_studio")
    public List<AnimeTitle> titlesByStudio(@RequestParam("studio") String studio) {
        return repository.getTitlesByStudio(studio);
    }

    @GetMapping("api/titles/duration_not_more")
    public List<AnimeTitle> titlesByStudio(@RequestParam int duration, @RequestParam int episodes) {
        return repository.getTitlesWithSpecificDuration(duration, episodes);
    }

    @GetMapping("api/titles/undiscovered")
    public List<AnimeTitle> titlesUndiscovered() {
        return repository.getUndiscoveredTitles();
    }
}
