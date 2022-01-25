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

    @GetMapping("/titles")
    public List<AnimeTitle> titles() {
        return repository.getAllTitles();
    }

    @GetMapping("/titles/ranked")
    public List<AnimeTitle> titlesRanked() {
        return repository.getTitlesRanked();
    }

    @GetMapping("/title/synopsis")
    public String titleSynopsis(@RequestParam int id) {
        return repository.getTitleSynopsis(id);
    }

    @GetMapping("/titles/by_year")
    public List<AnimeTitle> titlesByYears(
            @RequestParam(value = "from", defaultValue = "0") int from,
            @RequestParam(value = "to", defaultValue = "2022") int to
    ) {
        return repository.getTitlesByYear(from, to);
    }

    @GetMapping("/titles/warning")
    public List<AnimeTitleWithWarnings> titlesWithoutContentWarnings(@RequestParam String warning) {
        Set<String> warnings = Arrays.stream(warning.split(",")).collect(Collectors.toSet());
        return repository.getTitlesWithoutContentWarnings(warnings);
    }

    @GetMapping("/titles/by_genre")
    public List<AnimeTitleWithGenres> titlesByGenre(@RequestParam("genre") String genre) {
        return repository.getTitlesByGenre(genre);
    }

    @GetMapping("/titles/by_producer")
    public List<AnimeTitleWithProducers> titlesByProducer(@RequestParam("producer") String producer) {
        return repository.getTitlesByProducer(producer);
    }

    @GetMapping("/titles/by_studio")
    public List<AnimeTitleWithStudios> titlesByStudio(@RequestParam("studio") String studio) {
        return repository.getTitlesByStudio(studio);
    }
}
